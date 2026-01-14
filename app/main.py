import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Set
import ssl
import aiohttp
import certifi

import discord
from discord import Intents
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# SSL cert
try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except Exception:
    pass

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


app = FastAPI(title="Discord Stream Viewer")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class Broadcaster:
    def __init__(self) -> None:
        self._clients: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def add_client(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._clients.add(q)
        return q

    async def remove_client(self, q: asyncio.Queue) -> None:
        async with self._lock:
            self._clients.discard(q)

    async def publish(self, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False)
        async with self._lock:
            clients = list(self._clients)

        for q in clients:
            try:
                q.put_nowait(data)
            except asyncio.QueueFull:
                pass


broadcaster = Broadcaster()


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/events")
async def sse_events(request: Request) -> StreamingResponse:
    client_q = await broadcaster.add_client()

    async def event_generator():
        try:
            yield "event: status\ndata: connected\n\n"

            while True:
                if await request.is_disconnected():
                    break

                try:
                    data = await asyncio.wait_for(client_q.get(), timeout=15)
                    yield f"event: message\ndata: {data}\n\n"
                except asyncio.TimeoutError:
                    yield "event: ping\ndata: {}\n\n"
        finally:
            await broadcaster.remove_client(client_q)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ---------------- Discord bot ----------------
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0") or "0")

intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

INSECURE_SSL = os.getenv("DISCORD_INSECURE_SSL", "").lower() in ("1", "true", "yes")

if INSECURE_SSL:
    # Dev-only fallback; do NOT use in production
    connector = aiohttp.TCPConnector(ssl=False)
else:
    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_ctx)

client = discord.Client(intents=intents, connector=connector)

@client.event
async def on_ready():
    print(f"[discord] Logged in as {client.user} (id={client.user.id})")
    if DISCORD_CHANNEL_ID:
        print(f"[discord] Watching channel id={DISCORD_CHANNEL_ID}")
    else:
        print("[discord] DISCORD_CHANNEL_ID not set")


@client.event
async def on_message(message: discord.Message):
    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # Filter to the configured channel
    if DISCORD_CHANNEL_ID and message.channel.id != DISCORD_CHANNEL_ID:
        return

    payload = {
        "author": message.author.display_name,
        "content": message.content,
        "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    await broadcaster.publish(payload)


@app.on_event("startup")
async def start_discord_bot():
    if not DISCORD_TOKEN:
        print("[discord] DISCORD_TOKEN not set; bot will not start.")
        return

    # Run discord client in background on the same event loop
    asyncio.create_task(client.start(DISCORD_TOKEN))

@app.get("/health")
async def health():
    return {"ok": True}