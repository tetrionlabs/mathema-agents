#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Tetrion Ltd
"""Check every skill against the conventions this repository relies on.

Run it locally the same way CI does:

    python3 scripts/check_skills.py

Each check exists because breaking it ships something wrong to a reader
rather than merely untidy: a name that does not match its directory is a
skill an agent cannot invoke, a missing version pin is a skill that claims
to describe a surface it may not, and a stale dist/ serves every non-Claude
tool an adapter for a skill set that has moved on.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
# the mathema line these skills describe; bump it with the skills, not
# independently, since the pin is what tells a reader which surface they got
LINE = "0.6"

problems: list[str] = []


def fail(where: str, msg: str) -> None:
    problems.append(f"{where}: {msg}")


def frontmatter(text: str) -> dict:
    """The YAML frontmatter as a dict, without a yaml dependency: these
    files carry only `name` and a folded `description`."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    out, key = {}, None
    for line in text[4:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = m.group(2).strip()
        elif key and line.strip():
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def check_skill(d: pathlib.Path) -> None:
    md = d / "SKILL.md"
    if not md.exists():
        return fail(d.name, "no SKILL.md")
    text = md.read_text()
    rel = f"skills/{d.name}/SKILL.md"

    fm = frontmatter(text)
    if not fm:
        return fail(rel, "no parseable YAML frontmatter")
    if fm.get("name") != d.name:
        fail(rel, f"frontmatter name {fm.get('name')!r} != directory {d.name!r}")
    desc = fm.get("description", "").lstrip(">-").strip()
    if len(desc) < 80:
        fail(rel, "description too short to route on; say when to use it")

    # house prose style: no em-dash, and no double-hyphen standing in for one
    for n, line in enumerate(text.splitlines(), 1):
        if "—" in line or "–" in line:
            fail(f"{rel}:{n}", "em/en dash; use a comma, colon or parentheses")
        if re.search(r"\s--\s", line):
            fail(f"{rel}:{n}", "double-hyphen standing in for a dash")

    if f">={LINE},<" not in text:
        fail(rel, f"no mathema {LINE} version pin; a reader cannot tell "
                  "which surface this describes")


def check_adapters_current() -> None:
    """dist/ is generated from skills/. A stale adapter is invisible to
    everyone editing skills and wrong for everyone vendoring one."""
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_adapters.py")],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        return fail("dist/", f"render_adapters.py failed: {r.stderr.strip()}")
    # porcelain status, not diff: a new adapter is untracked and a removed
    # one is deleted, and both are as stale as an edited one
    d = subprocess.run(["git", "status", "--porcelain", "--", "dist"],
                       capture_output=True, text=True, cwd=ROOT)
    changed = [ln for ln in d.stdout.splitlines() if ln.strip()]
    if changed:
        fail("dist/", "out of date, run `python3 scripts/render_adapters.py` "
                      "and commit:\n    " + "\n    ".join(changed))


def main() -> int:
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not dirs:
        fail("skills/", "no skills found")
    for d in dirs:
        check_skill(d)
    check_adapters_current()

    if problems:
        print(f"{len(problems)} problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"{len(dirs)} skill(s) ok, dist/ current, pinned to mathema {LINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
