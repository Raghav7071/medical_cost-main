"""Conversational health-assistant chatbot powered by Groq.

The assistant is Maya — a warm, plain-language healthcare companion modelled
after the helpful pharmacist behind a counter rather than a doctor. The
conversation is multi-turn: the call site passes the running message history
on every call so Maya can reference earlier turns naturally.

Falls back to a static message if no API key is configured.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


SYSTEM_PROMPT = (
    "You are Maya, a friendly healthcare companion for MediGuide. "
    "Think of yourself as the helpful pharmacist behind the counter — not a doctor. "
    "Speak conversationally and warmly, like you are talking to a friend or family member "
    "who has walked in with a worry. Use short, plain sentences. Avoid clinical jargon "
    "unless the person asks for it.\n\n"
    "If something sounds serious — chest pain, shortness of breath, sudden weakness, "
    "heavy bleeding, a head injury, signs of a stroke, severe allergic reactions — say so "
    "directly and tell the person to call emergency services or see a doctor today.\n\n"
    "For non-urgent questions, give practical guidance: rest, hydration, when an "
    "over-the-counter medicine is reasonable, what to track, when to book a doctor's "
    "visit, and how to prepare for that visit. Always remind, briefly, that you cannot "
    "diagnose — only point in the right direction.\n\n"
    "Keep replies under 4 sentences unless the person asks for more detail. "
    "Match their tone: if they sound worried, be reassuring; if they sound casual, be casual. "
    "If they ask a follow-up, build on what they already told you instead of starting from scratch."
)

_MODEL = "llama-3.3-70b-versatile"

# Cap context window. Groq tolerates much more but capping keeps latency and
# token spend predictable for long sessions.
_HISTORY_TURNS = 20


def get_chatbot_response(
    messages: list[dict],
    api_key: Optional[str] = None,
) -> str:
    """Run a multi-turn chat completion. `messages` is the running chat_history
    in `[{"role": "user"|"assistant", "content": "..."}]` shape."""
    api_key = api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        return (
            "I can't connect right now — set your Groq API key in the sidebar and "
            "I'll be ready to chat."
        )

    history = messages[-_HISTORY_TURNS:] if messages else []
    payload = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=_MODEL,
            messages=payload,
            temperature=0.6,
            max_tokens=400,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Sorry, I hit a snag reaching the AI service: {e}"
