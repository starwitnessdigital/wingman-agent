"""
Wingman FastAPI server.

Privacy: Sessions are server-side ephemeral — stored in memory only,
cleared when the session expires or the server restarts. No database.
No persistent logs of conversation content.
"""

import os
import uuid
import time
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from main import run_wingman

load_dotenv()

app = FastAPI(
    title="Wingman API",
    description="AI dating coach & safety companion for gay men. Zero data stored.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ephemeral session storage — memory only, no persistence
# Sessions expire after SESSION_TTL_SECONDS of inactivity
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "1800"))  # 30 min default

_sessions: dict[str, dict] = {}  # {session_id: {history: [...], last_active: float}}


def _cleanup_expired_sessions():
    """Remove sessions that have been inactive beyond TTL."""
    now = time.time()
    expired = [
        sid for sid, data in _sessions.items()
        if now - data["last_active"] > SESSION_TTL_SECONDS
    ]
    for sid in expired:
        del _sessions[sid]


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    created_note: str = "Session is ephemeral — not stored or logged."


@app.get("/")
async def root():
    web_dir = Path(__file__).parent / "web"
    if (web_dir / "index.html").exists():
        return FileResponse(web_dir / "index.html")
    return {"message": "Wingman API — /docs for API docs, /chat to start chatting"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to Wingman and get a response.

    Session management:
    - If session_id is provided and valid, continues that session
    - If session_id is omitted or invalid, creates a new session
    - Sessions live in memory only — cleared on server restart or TTL expiry
    """
    _cleanup_expired_sessions()

    # Resolve or create session
    session_id = request.session_id
    if session_id and session_id in _sessions:
        history = _sessions[session_id]["history"]
    else:
        session_id = str(uuid.uuid4())
        history = []

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        response_text, updated_history = run_wingman(request.message, history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    # Update session (memory only)
    _sessions[session_id] = {
        "history": updated_history,
        "last_active": time.time(),
    }

    return ChatResponse(response=response_text, session_id=session_id)


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Explicitly clear a session. Also happens automatically on TTL expiry."""
    if session_id in _sessions:
        del _sessions[session_id]
    return {"cleared": True, "session_id": session_id}


@app.get("/session/{session_id}", response_model=SessionInfo)
async def session_info(session_id: str):
    """Get info about a session (no conversation content returned)."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found or expired.")
    data = _sessions[session_id]
    msg_count = len([m for m in data["history"] if m["role"] == "user"])
    return SessionInfo(session_id=session_id, message_count=msg_count)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "privacy": "zero-storage",
        "active_sessions": len(_sessions),
        "note": "Session count only — no conversation content accessible via API.",
    }


@app.get("/privacy")
async def privacy_info():
    """Quick privacy summary."""
    return {
        "data_stored": False,
        "conversation_logs": False,
        "user_profiles": False,
        "analytics": False,
        "session_type": "ephemeral_memory_only",
        "session_ttl_seconds": SESSION_TTL_SECONDS,
        "full_policy": "See privacy_policy.md in the repository",
    }


# Serve static web files
web_dir = Path(__file__).parent / "web"
if web_dir.exists():
    app.mount("/web", StaticFiles(directory=str(web_dir)), name="web")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
