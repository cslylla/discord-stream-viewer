# 🤖 Discord Stream Viewer

## Project Overview
**Discord Stream Viewer** is a small real-time web application that reads messages from a Discord channel to a browser-based frontend.
It was built as part of a technical interview exercise to demonstrate backend–frontend integration, real-time communication, and deployment on Railway.

The system consists of a Discord bot, a lightweight Python backend, and a minimal web UI.

## How It Works
	1.	A Discord bot listens for new messages in a configured Discord channel.
	2.	When a message is posted, the bot forwards it to an in-memory broadcaster.
	3.	The backend exposes a Server-Sent Events (SSE) endpoint.
	4.	The web frontend subscribes to this SSE stream and displays messages in real time as they arrive.

**Data flow:**
Discord → Bot → Backend (FastAPI) → SSE → Browser
---

## Tech Stack

- **Backend:** Python, FastAPI  
- **Discord integration:** `discord.py`  
- **Real-time transport:** Server-Sent Events (SSE)  
- **Frontend:** Vanilla HTML, CSS, minimal JavaScript  
- **Deployment:** Railway (single service)  
- **Runtime config:** Environment variables  

---

## Live Demo

👉 **Live URL:**  
https://discord-stream-viewer.up.railway.app/

To see messages appear:
- Open the URL
- During review, messages can be posted in the configured Discord test channel to verify real-time streaming.
- The message appears instantly in the browser

---

## Why Server-Sent Events (SSE)

SSE was chosen because:
- The data flow is one-way (server → client)
- It is simpler than WebSockets for this use case
- It has native browser support
- It reduces backend complexity while still being real-time

---

## Alternatives Considered

- **WebSockets**  
  More flexible, but unnecessary for one-way streaming.

- **Separate worker service for the bot**  
  Cleaner separation, but adds operational complexity for a small demo.

- **Persistent storage (Redis / database)**  
  Useful for message history and replay, intentionally omitted for simplicity.

---

## Known Limitations

- Messages are stored **in memory only** (no persistence).
- The app listens to **a single Discord channel**.
- No authentication or access control.
- No rate limiting or reconnect backoff logic.

These were conscious trade-offs to keep the solution minimal and focused.

---

## Possible Improvements

- Split the bot and web server into separate services.
- Add Redis or a database for message persistence.
- Support multiple channels or servers.
- Add basic authentication and configuration UI.
- Improve error handling and observability.

---

## Notes

This project prioritizes clarity, simplicity, and correctness over scale.  
It is designed to be easy to reason about, easy to deploy, and easy to extend.