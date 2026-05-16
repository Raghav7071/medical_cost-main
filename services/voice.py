"""Voice helpers for the Health Assistant.

STT  → Groq Whisper (reuses GROQ_API_KEY; same SDK as the chat client).
TTS  → Microsoft Edge neural voices via the free `edge-tts` package — no key.

Both functions never raise. STT failures surface as an empty string; TTS
failures surface as empty bytes. Call sites should treat empty results as
"skip the audio, keep the conversation moving."
"""

from __future__ import annotations

import asyncio
import io
import os
from typing import Optional

import edge_tts
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


# Default voice: warm, soft female cadence with bedside-manner energy.
DEFAULT_VOICE = "en-US-JennyNeural"
# Groq's fast Whisper variant. Sub-second on short clips.
WHISPER_MODEL = "whisper-large-v3-turbo"
# Cap TTS input length so a long reply doesn't make the user wait 10s.
_TTS_TEXT_CAP = 1500


def _resolve_key(api_key: Optional[str]) -> Optional[str]:
    return api_key or os.getenv("GROQ_API_KEY")


def transcribe_audio(
    audio_bytes: bytes,
    mime: str = "audio/wav",
    api_key: Optional[str] = None,
) -> str:
    """Return the transcript for `audio_bytes`. Empty string on failure."""
    if not audio_bytes:
        return ""
    key = _resolve_key(api_key)
    if not key:
        return ""
    try:
        client = Groq(api_key=key)
        result = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=("input.wav", audio_bytes, mime),
            response_format="text",
        )
        # The SDK returns either a plain string (response_format="text") or an
        # object with .text. Handle both.
        if isinstance(result, str):
            return result.strip()
        text = getattr(result, "text", "") or ""
        return text.strip()
    except Exception:
        return ""


async def _edge_tts_to_bytes(text: str, voice: str) -> bytes:
    communicate = edge_tts.Communicate(text, voice)
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return buf.getvalue()


def synthesize_speech(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """Return MP3 bytes for `text`. Empty bytes on failure."""
    if not text:
        return b""
    payload = text[:_TTS_TEXT_CAP].strip()
    try:
        return asyncio.run(_edge_tts_to_bytes(payload, voice))
    except RuntimeError:
        # Already inside an event loop (rare under Streamlit, but defensive).
        # Run the coroutine on a fresh loop in a thread-safe way.
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(_edge_tts_to_bytes(payload, voice))
            finally:
                loop.close()
        except Exception:
            return b""
    except Exception:
        return b""
