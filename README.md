# Photo Point — Notifications Service (Email · SMS · Telegram)

A tiny FastAPI + Celery service that sends notifications via **Email**, **SMS (Twilio)**, and **Telegram**.  
If one channel fails, the worker **falls back** to the next (configurable order).

---

## Features
- Simple web UI (form) + REST endpoints
- Channels: Email (dev via MailHog), SMS (Twilio), Telegram (Bot API)
- Fallback delivery: try channels in order until one succeeds
- Dockerized: API, Celery worker, Redis, MailHog

---

## Quick Start

### 1) Clone
```bash
git clone https://github.com/ReptiloidAnunak/photo_point
cd photo_point
```
### 3) Run app
Put .env file with your evrinonment into the project`s root (see env-ex)

```
./run_app.sh
# or, if you prefer:
# docker compose up -d --build
```

### 3) Open

App UI: http://localhost:8000

MailHog (dev inbox): http://localhost:8025

Follow instructions and send your notifiction

Сheck SMS in your phone, MailHog and chat with @photo_point_first_bot