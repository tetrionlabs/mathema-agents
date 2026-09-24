# Security

This repository holds configuration only: agent skills and the adapters
generated from them. It runs no code in your project and makes no network
calls. The one script that ships, `scripts/render_adapters.py`, is a local
build step for this repository.

The skills tell an agent how to drive mathema. A vulnerability in mathema
itself, or a way a skill here could lead an agent to bypass a human-only
decision (accepting a verdict, unlocking a function), is best reported
privately under mathema's security policy:
<https://github.com/tetrionlabs/mathema/blob/main/SECURITY.md>.
