# Anza: ship an AI SaaS in a day

The open-source AI SaaS starter in plain Python and HTML. No React, no build step, no node_modules. The entire kit is 559 lines. Read every file before lunch.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app
```

Then open http://localhost:8000, sign up, and chat.

## What's inside

- **Auth**: email/password, PBKDF2-hashed, signed HTTP-only session cookies. Standard library only.
- **AI chat**: OpenAI-compatible client. One env variable points it at OpenAI, Fikra, or any compatible provider.
- **PWA**: installable, offline shell. A manifest and a service worker, nothing more.
- **SQLite**: single file, created on first run. No ORM, no migrations framework.
- **Frontend**: one HTML page, Tailwind via CDN, vanilla JS. No build step.
- **Nothing else**: that is the point.

## What we left out

- No React, no TypeScript, no node_modules
- No ORM, no Docker Compose, no Redis, no Celery, no CI YAML
- No linter config forest

Every file in this repo exists because your SaaS needs it.

## Free vs Pro

| | Free (MIT) | Pro ($59 one-time) |
|---|---|---|
| Auth, chat, PWA, SQLite | Yes | Yes |
| Payments wiring (Paystack + Stripe) | No | Yes |
| Email sequences and admin dashboard | No | Yes |
| Lifetime updates | No | Yes |

Pro launches October 13. The free core is MIT with no nagware and no crippled features.

## Who made this

A solo developer in Kenya who runs Fikra, an OpenAI-compatible AI inference API. Anza ships pointed at Fikra with free credits included. Change one line in .env to use OpenAI or any other compatible provider.

## License

MIT. Use it for anything, including commercial products.

## Links

- Landing page: https://anza.fikra.live
- Fikra API: https://fikraapi.co.ke
