#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Tetrion Ltd
"""Render the canonical skills into the config formats other agents read.

The source of truth is skills/<name>/SKILL.md. This emits, into dist/, a
LEAN adapter per tool: the skill's own description, the two rules that
govern all of mathema, and a pointer to the vendored SKILL.md for the full
procedure. Pointer rather than inline keeps every tool's config file small
and keeps one source of depth; a consuming repo vendors the skills/ dir and
copies the adapter its tool reads.

Stdlib only, no dependencies. Run from the repo root:

    python3 scripts/render_adapters.py
"""
from __future__ import annotations

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

# The rules are true of mathema whatever tool drives it, so every adapter
# states them even when it only points at the full skill.
RULES = (
    "Two rules are non-negotiable, whatever tool you drive mathema with:\n"
    "1. You never adjudicate your own claims. Every verdict you report "
    "comes from a mathema call you actually made.\n"
    "2. You never close your own diagnosis. A falsification says a claim "
    "and the code disagree, not which is wrong; that is a human's call "
    "(`mathema accept` is deliberately not an agent surface). The same "
    "goes for `mathema unlock`: you may lock a function you finished, "
    "and only a person unlocks one."
)


def parse_skill(path: pathlib.Path) -> tuple[str, str]:
    """`(name, description)` from a SKILL.md's YAML frontmatter, parsed by
    hand so nothing outside the stdlib is needed. `description` is the
    folded (`>-`) block joined into one line."""
    text = path.read_text()
    if not text.startswith("---"):
        raise ValueError(f"{path}: no frontmatter")
    front = text.split("---", 2)[1].splitlines()
    name = ""
    desc: list[str] = []
    collecting = False
    for line in front:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
            collecting = False
        elif line.startswith("description:"):
            rest = line.split(":", 1)[1].strip()
            collecting = rest in (">-", ">", "|", "|-", "")
            if not collecting and rest:
                desc.append(rest)
        elif collecting and (line.startswith(("  ", "\t")) or not line.strip()):
            if line.strip():
                desc.append(line.strip())
        elif line and not line[0].isspace():
            collecting = False
    return name, " ".join(desc).strip()


def write(rel: str, body: str) -> None:
    path = DIST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n")
    print(f"  wrote dist/{rel}")


def body_for(name: str, desc: str) -> str:
    """The shared adapter body: what the skill is, the rules, the pointer."""
    return (f"{desc}\n\n{RULES}\n\n"
            f"The full procedure is in `skills/{name}/SKILL.md` (vendor the "
            f"`skills/` directory from mathema-agents into this repo). Read it "
            f"before proposing or adjudicating claims, and fetch mathema's own "
            f"grammar, verdict and reason-code references (served by its MCP "
            f"server, or `mathema` on the CLI) just in time rather than "
            f"working from memory.")


def render() -> None:
    skills = []
    for skill_dir in sorted(SKILLS.iterdir()):
        md = skill_dir / "SKILL.md"
        if md.is_file():
            name, desc = parse_skill(md)
            skills.append((name, desc, body_for(name, desc)))
    print(f"rendering {len(skills)} skill(s) into dist/")

    banner = ("<!-- SPDX-License-Identifier: Apache-2.0. Generated from "
              "skills/*/SKILL.md by scripts/render_adapters.py. Edit the "
              "SKILL.md, not this file, then re-run the script. -->")

    # dist/ is entirely generated, so it is rebuilt from nothing: an
    # adapter for a skill that no longer exists must not survive
    if DIST.exists():
        shutil.rmtree(DIST)

    # AGENTS.md: the cross-tool standard (Codex, Zed, Aider, Jules, Gemini,
    # and increasingly Cursor/Copilot read it). One file, a section each.
    agents = [banner, "", "# Working with mathema in this repository", ""]
    for name, _desc, body in skills:
        agents += [f"## {name}", "", body, ""]
    write("AGENTS.md", "\n".join(agents))
    # Gemini CLI reads GEMINI.md; same content.
    write("GEMINI.md", "\n".join(agents))

    # Cursor: one .mdc rule per skill, its own frontmatter.
    for name, desc, body in skills:
        write(f".cursor/rules/{name}.mdc",
              f"---\ndescription: {desc}\nalwaysApply: false\n---\n\n"
              f"{banner}\n\n{body}")

    # Windsurf: one rule per skill under .windsurf/rules/.
    for name, desc, body in skills:
        write(f".windsurf/rules/{name}.md",
              f"---\ntrigger: model_decision\ndescription: {desc}\n---\n\n"
              f"{banner}\n\n{body}")

    # Cline / Roo: plain markdown under .clinerules/.
    for name, _desc, body in skills:
        write(f".clinerules/{name}.md", f"{banner}\n\n# {name}\n\n{body}")

    # GitHub Copilot: one repo-wide instructions file, a section each.
    copilot = [banner, "", "# mathema", ""]
    for name, _desc, body in skills:
        copilot += [f"## {name}", "", body, ""]
    write(".github/copilot-instructions.md", "\n".join(copilot))

    print("done. Claude Code uses skills/*/SKILL.md directly (no adapter).")


if __name__ == "__main__":
    render()
