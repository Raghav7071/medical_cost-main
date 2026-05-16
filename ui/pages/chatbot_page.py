"""Health Assistant page — chat with Maya.

Two ways to talk to Maya:

  1. **Live voice mode** (top): a self-contained browser iframe that runs the
     entire mic → STT → Groq → TTS loop client-side. Press start once, then
     have a natural phone-call-style conversation. No clicks between turns.

  2. **Typed chat** (bottom): classic text input wired through Streamlit's
     Python flow. Useful for noisy environments or silent mode. Maya can
     speak typed replies aloud too if the voice toggle is on.
"""

from __future__ import annotations

import base64

import streamlit as st
import streamlit.components.v1 as components

from services.chatbot import get_chatbot_response
from services.symptom_analyzer import get_symptom_analysis
from services.voice import synthesize_speech
from services.voice_chat_html import render_voice_chat_html
from ui.components import leader_row, page_title, rule


# ---------- symptom analyser (unchanged behaviour, light copy edit) ----------

def _render_symptom_analyzer(api_key: str) -> None:
    st.markdown(rule("QUICK CHECK"), unsafe_allow_html=True)
    symptoms = st.text_area(
        "Describe what you're feeling",
        placeholder="e.g. sore throat for two days, mild headache, no fever",
    )
    if st.button("Analyze →", key="analyze_btn"):
        with st.spinner("Reading..."):
            result = get_symptom_analysis(symptoms, api_key)
            st.markdown(
                "<div class='hairline-card' style='padding:18px; margin-top:14px;'>"
                + leader_row("Likely condition", result.get("Disease", "—"))
                + leader_row("Who to see", result.get("Department", "—"))
                + leader_row("Severity", result.get("Severity", "—"), signal=True)
                + "</div>",
                unsafe_allow_html=True,
            )


# ---------- live voice conversation -----------------------------------------

def _render_live_voice(api_key: str) -> None:
    st.markdown(rule("LIVE VOICE"), unsafe_allow_html=True)
    html = render_voice_chat_html(api_key)
    components.html(html, height=620, scrolling=False)


# ---------- typed chat (fallback) -------------------------------------------

def _ensure_chat_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "voice_replies" not in st.session_state:
        st.session_state.voice_replies = False
    if "last_reply_audio" not in st.session_state:
        st.session_state.last_reply_audio = b""


def _render_transcript() -> None:
    history = st.session_state.chat_history
    if not history:
        st.caption("No typed messages yet.")
        return
    bubbles = []
    for msg in history:
        role = msg["role"]
        content = (
            msg["content"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        bubbles.append(
            f"<div class='chat-row {role}'>"
            f"<div class='chat-bubble {role}'>{content}</div>"
            f"</div>"
        )
    st.markdown("".join(bubbles), unsafe_allow_html=True)


def _render_audio_playback() -> None:
    audio_bytes = st.session_state.last_reply_audio
    if not audio_bytes:
        return
    b64 = base64.b64encode(audio_bytes).decode("ascii")
    st.markdown(
        f"<audio autoplay controls style='width:100%; margin: 8px 0;'>"
        f"<source src='data:audio/mp3;base64,{b64}' type='audio/mp3'>"
        f"</audio>",
        unsafe_allow_html=True,
    )


def _render_typed_chat(api_key: str) -> None:
    st.markdown(rule("TYPED CHAT"), unsafe_allow_html=True)
    st.session_state.voice_replies = st.checkbox(
        "🔊 Speak typed replies aloud",
        value=st.session_state.voice_replies,
        key="typed_voice_toggle",
    )
    _render_transcript()
    _render_audio_playback()

    typed = st.chat_input("Type a question...")
    if not typed:
        return
    st.session_state.chat_history.append({"role": "user", "content": typed})
    with st.spinner("Maya is thinking..."):
        reply = get_chatbot_response(st.session_state.chat_history, api_key)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    if st.session_state.voice_replies and reply:
        with st.spinner("Synthesizing voice..."):
            st.session_state.last_reply_audio = synthesize_speech(reply)
    else:
        st.session_state.last_reply_audio = b""
    st.rerun()


# ---------- entry point -----------------------------------------------------

def render() -> None:
    page_title("Ask Maya, your health companion.", eyebrow="05 / HEALTH ASSISTANT")
    st.markdown(
        "<p class='speako-sub'>Speak naturally with Maya in live voice mode, "
        "or type below. She answers in plain language and tells you when it's "
        "time to see a real doctor.</p>",
        unsafe_allow_html=True,
    )

    api_key = st.sidebar.text_input("GROQ KEY (optional)", type="password", key="groq_key")

    _ensure_chat_state()

    _render_symptom_analyzer(api_key)
    _render_live_voice(api_key)
    _render_typed_chat(api_key)
