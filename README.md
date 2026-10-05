# Anza — ship an AI SaaS in a day

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app
```

## What's inside

- **FastAPI Backend**: Clean and explicit endpoints with zero boilerplate.
- **SQLite Database**: Built-in stdlib SQLite user storage with auto-initialization.
- **PBKDF2 Authentication**: Secure stdlib password hashing with signed HTTP-only session cookies.
- **OpenAI-Compatible AI Integration**: Drop-in client configuration for OpenAI, Fikra, or any compatible provider.
- **Minimal Single-Page Frontend**: Vanilla ES6 JavaScript and Tailwind CSS via CDN without npm or build steps.
- **PWA Basics**: Installable web application with manifest and cache-first service worker.

## Free vs Pro

| Feature | Free (Open Source Core) | Pro (Coming Soon) |
|---|---|---|
| Tech Stack | FastAPI + SQLite + Vanilla JS | FastAPI + PostgreSQL + Modern UI |
| Authentication | Email/Password (PBKDF2) + Signed Cookies | Social OAuth (Google, GitHub) + Magic Links |
| AI Integration | OpenAI-compatible chat endpoint | Streaming completions, tool calling, prompt library |
| Database | SQLite (stdlib, zero configuration) | PostgreSQL + automated migrations |
| Payments & Billing | None | Stripe Checkout, Subscriptions & Webhooks |
| Usage & Quotas | None | Token tracking, rate limits & tier management |
| Deployment | Direct Uvicorn run | Production Docker, Fly.io, Railway templates |
| Support | Community / GitHub | Priority support & commercial license |
