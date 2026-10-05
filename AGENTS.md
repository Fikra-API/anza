# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

Anza: a minimal AI SaaS starter. FastAPI backend, single-page vanilla JS frontend, SQLite, OpenAI-compatible client. 559 lines total.

## Where things live

- app/main.py: routes, app setup, static file mount
- app/auth.py: signup, login, session tokens
- app/db.py: sqlite3 helpers, users table
- app/ai.py: OpenAI-compatible chat client, base URL from env
- static/: the entire frontend (index.html, app.js, sw.js, manifest.json)

## Rules for agents

- Keep it small. Every new line must justify itself.
- No new dependencies without asking first.
- No frameworks, no ORM, no build step, no npm. Standard library first, always.
- Prefer editing existing files over adding new ones.
- After any change, the 3-command quickstart in README.md must still work.
