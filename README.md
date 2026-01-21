# 🤖 Discord Stream Viewer

## Project Overview

**Discord Stream Viewer** is a small real-time web application that streams messages from a Discord channel to a browser-based frontend.

It was built as part of a technical interview exercise to demonstrate:
- backend–frontend integration
- real-time message delivery
scoping and trade-offs
- deployment on Railway

The system consists of a Discord bot, a lightweight Python backend, and a minimal web UI, all deployed as a single service.

### Deployment note

The original version of this app was deployed on Railway using the free plan, which expires after 30 days.  
To keep the project publicly accessible for demonstration purposes, it is now redeployed on Render.

**Current live URL:**  
https://discord-stream-viewer.onrender.com/

---

## How the Solution Works

### High-level flow

1. A **Discord bot** listens for messages in a configured Discord channel.
2. Messages are forwarded to an **in-memory broadcaster** in the backend.
3. The backend exposes:
   - a **history endpoint** (`/history`) for recent messages
   - a **Server-Sent Events (SSE)** endpoint (`/events`) for live updates
4. The web frontend:
   - loads the most recent messages on page load
   - subscribes to the SSE stream for new messages
   - prepends new messages at the top in real time

**Data flow:**
Discord → Bot → FastAPI backend → SSE → Browser

---

## Message History on Page Load

To avoid an empty UI for new visitors, the app displays recent messages when the page is opened.

- On bot startup, the last **10 messages** are fetched from the Discord channel via the Discord API.
- These messages are stored **in memory**.
- When a user opens the website, the frontend fetches `/history` and renders those messages.
- New messages are then streamed live via SSE and added to the top of the list.

This provides immediate context while keeping the implementation simple.

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Discord integration:** `discord.py`
- **Real-time transport:** Server-Sent Events (SSE)
- **Frontend:** Vanilla HTML, CSS, minimal JavaScript
- **Deployment:** Railway (single service)
- **Configuration:** Environment variables

---

## How to Use the App

1. Open the deployed URL: https://discord-stream-viewer.up.railway.app/
2. Recent messages from the Discord test channel are displayed immediately.
3. Post a new message in the configured Discord channel.
4. The message appears instantly at the top of the page.

---

## Design Decisions & Scope

### Technologies used
- Python + FastAPI were chosen due to familiarity and speed of implementation.
- Vanilla HTML/CSS/JS was used to keep the frontend simple and dependency-free.
- SSE was chosen over WebSockets for its simplicity and suitability for one-way streams.

### Goal and scope
- Build a **minimal, working, end-to-end solution**.
- Focus on correctness, clarity, and debuggability.
- Avoid premature optimization or overengineering.

### Railway usage
- The app is deployed as a **single service**.
- Runtime configuration is handled via environment variables.
- No Railway templates were used; the service was built from scratch to keep behavior explicit.

---

## Alternatives Considered

- **WebSockets**  
  More flexible, but unnecessary for one-way message streaming.

- **Using a Railway Discord bot template**  
  Faster initial setup, but building from scratch provided more control and clarity.

- **Separate worker service for the bot**  
  Cleaner separation of concerns, but adds operational complexity for a small demo.

- **Database-backed persistence**  
  Useful for long-term history and analytics, intentionally omitted for simplicity.

---

## Things Not Considered (by design)

- **Scalability**  
  The app is designed for a single channel and small audience.

- **Performance tuning**  
  The workload is minimal and does not warrant optimization.

- **Security beyond basics**  
  The Discord token is kept secret via environment variables, but no authentication or authorization is implemented.

- **Comprehensive error handling**  
  Edge cases (network issues, Discord outages, thread messages, etc.) are not fully covered.

---

## Known Limitations

- Message history is **in-memory only** and resets on service restart or redeploy.
- Only one Discord channel is supported.
- Thread messages are not handled.
- No authentication or access control.
- No rate limiting or retry backoff logic.

These limitations were accepted to keep the solution focused and easy to reason about.

---

## Possible Improvements

- Persist messages using Redis or a database.
- Split the bot into a separate worker service.
- Support multiple channels or servers.
- Improve error handling and reconnection logic.
- Add authentication and configuration UI.
- Resolve Discord mentions (channels, users) for display outside Discord.

---

## Notes

This project prioritizes clarity, simplicity, and explicit trade-offs over completeness or scale.  
It is intended as a small, inspectable example rather than a production-ready system.