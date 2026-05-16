"""Self-contained voice-chat iframe HTML. Renders a phone-call-style
conversation panel that runs entirely in the browser — no Streamlit reruns
between turns.

The browser handles:
  1. mic capture + continuous speech recognition (Web Speech API)
  2. fetch() to Groq's chat-completions endpoint
  3. speech synthesis playback (Web Speech API SpeechSynthesis)
  4. auto-restart of recognition after Maya finishes speaking

API key is injected at render time. The flow loops automatically until the
user clicks "Stop".
"""

from __future__ import annotations

import html as _html
import json
import os

from services.chatbot import SYSTEM_PROMPT


_VOICE_CHAT_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1E3A5F;
    background: #FFFFFF;
  }
  #shell {
    background: #FFFFFF;
    border: 1px solid #E4ECF3;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 1px 2px rgba(30,58,95,0.04), 0 1px 1px rgba(30,58,95,0.03);
  }
  #head { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
  .avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: #EAF4FF;
    color: #3B82F6;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 16px;
  }
  .name { font-weight: 700; font-size: 16px; color: #1E3A5F; }
  .tagline {
    font-size: 13.5px;
    color: #5B7185;
    margin: 0 0 16px 48px;
    line-height: 1.5;
  }
  #controls {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  #toggle, #skip {
    border-radius: 999px;
    padding: 11px 20px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.15s ease, border-color 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  #toggle {
    background: #3B82F6;
    color: #FFFFFF;
    border: 1px solid #3B82F6;
  }
  #toggle:hover { background: #2563EB; border-color: #2563EB; }
  #toggle.active {
    background: #FEF2F2;
    color: #DC2626;
    border-color: #FECACA;
  }
  #toggle.active:hover { background: #FEE2E2; }
  #toggle .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: currentColor;
  }
  #toggle.active .dot { animation: pulse 1.1s ease-in-out infinite; }
  #skip {
    background: #FFFFFF;
    color: #1E3A5F;
    border: 1px solid #E4ECF3;
    display: none;
  }
  #skip:hover { background: #F1F5F9; border-color: #C8D7E6; }
  #skip.visible { display: inline-flex; }
  @keyframes pulse {
    0%, 100% { opacity: 0.35; transform: scale(0.85); }
    50%      { opacity: 1;    transform: scale(1.15); }
  }
  #status {
    font-size: 13px;
    color: #5B7185;
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  #status .ind {
    width: 8px; height: 8px; border-radius: 50%;
    background: #5B7185;
  }
  #status.listening .ind { background: #0F9D7A; animation: pulse 1.1s ease-in-out infinite; }
  #status.thinking .ind  { background: #3B82F6; animation: pulse 1.1s ease-in-out infinite; }
  #status.speaking .ind  { background: #F59E0B; animation: pulse 1.1s ease-in-out infinite; }
  #status.error .ind     { background: #DC2626; }

  #transcript {
    border: 1px solid #E4ECF3;
    border-radius: 12px;
    padding: 14px;
    max-height: 340px;
    overflow-y: auto;
    background: #F7FAFC;
  }
  #transcript:empty::before {
    content: "Your conversation will appear here.";
    color: #8DA0B5;
    font-size: 13.5px;
  }
  .row { display: flex; margin-bottom: 8px; }
  .row.user { justify-content: flex-end; }
  .bubble {
    max-width: 80%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 14.5px;
    line-height: 1.55;
    word-wrap: break-word;
    white-space: pre-wrap;
  }
  .bubble.user {
    background: #EAF4FF;
    color: #1E3A5F;
    border-bottom-right-radius: 4px;
  }
  .bubble.assistant {
    background: #FFFFFF;
    color: #1E3A5F;
    border: 1px solid #E4ECF3;
    border-bottom-left-radius: 4px;
  }
  .interim {
    color: #8DA0B5;
    font-style: italic;
  }
  .small {
    font-size: 12px;
    color: #8DA0B5;
    margin-top: 10px;
  }
</style>
</head>
<body>
<div id="shell">
  <div id="head">
    <div class="avatar">M</div>
    <div class="name">Maya — live voice</div>
  </div>
  <p class="tagline">Tap start and just talk. Maya listens, replies, and starts listening again — no buttons between turns.</p>

  <div id="controls">
    <button id="toggle"><span class="dot"></span><span id="toggleLabel">Start conversation</span></button>
    <button id="skip" title="Stop Maya and listen for your reply">⏭ Skip</button>
    <span id="status"><span class="ind"></span><span id="statusLabel">Idle</span></span>
  </div>

  <div id="transcript"></div>
  <p class="small">Voice quality depends on your browser. Chrome/Edge work best. Mic access required.</p>
</div>

<script>
(function() {
  const API_KEY = __API_KEY__;
  const SYSTEM_PROMPT = __SYSTEM_PROMPT__;
  const MODEL = "llama-3.3-70b-versatile";
  const ENDPOINT = "https://api.groq.com/openai/v1/chat/completions";

  const toggle = document.getElementById('toggle');
  const toggleLabel = document.getElementById('toggleLabel');
  const skipBtn = document.getElementById('skip');
  const statusEl = document.getElementById('status');
  const statusLabel = document.getElementById('statusLabel');
  const transcript = document.getElementById('transcript');

  let messages = [{ role: 'system', content: SYSTEM_PROMPT }];
  let recognition = null;
  let active = false;
  let speaking = false;
  let restartTimer = null;
  let voicePref = null;
  let lastSpokenTail = '';      // last 60 chars Maya just said — used for echo filtering
  let speakEndedAt = 0;         // ms timestamp Maya finished speaking
  const ECHO_WINDOW_MS = 1200;  // ignore user input within this window if it overlaps lastSpokenTail
  const RESTART_DELAY_MS = 500; // delay before mic reopens after TTS

  // ---- voice barge-in (VAD while Maya is speaking) -----------------------
  let bargeStream = null;        // live MediaStream used only for VAD
  let bargeAudioCtx = null;      // shared AudioContext
  let bargeAnalyser = null;      // AnalyserNode reading mic levels
  let bargeRafId = null;         // requestAnimationFrame handle
  let bargeAboveSince = 0;       // first ms timestamp RMS went above threshold
  const VAD_RMS_THRESHOLD = 0.025;   // above ambient room noise w/ AEC on
  const VAD_SUSTAIN_MS = 220;        // sustained voice activity required to barge in

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  function setStatus(cls, text) {
    statusEl.className = cls;
    statusLabel.textContent = text;
  }

  function addBubble(role, text, interim) {
    const row = document.createElement('div');
    row.className = 'row ' + role;
    const b = document.createElement('div');
    b.className = 'bubble ' + role + (interim ? ' interim' : '');
    b.textContent = text;
    row.appendChild(b);
    transcript.appendChild(row);
    transcript.scrollTop = transcript.scrollHeight;
    return b;
  }

  function pickVoice() {
    const voices = window.speechSynthesis.getVoices();
    if (!voices.length) return null;
    const order = [
      v => /jenny/i.test(v.name) && /en-us/i.test(v.lang),
      v => /aria/i.test(v.name) && /en-us/i.test(v.lang),
      v => /samantha/i.test(v.name),
      v => /female/i.test(v.name),
      v => /en-us/i.test(v.lang),
      v => /^en/i.test(v.lang),
    ];
    for (const test of order) {
      const found = voices.find(test);
      if (found) return found;
    }
    return voices[0];
  }

  if (typeof window.speechSynthesis !== 'undefined') {
    window.speechSynthesis.onvoiceschanged = () => { voicePref = pickVoice(); };
    voicePref = pickVoice();
  }

  function startListening() {
    if (!active || speaking) return;
    if (!SR) {
      setStatus('error', 'This browser does not support speech recognition. Try Chrome or Edge.');
      return;
    }
    try {
      recognition = new SR();
    } catch (e) {
      setStatus('error', 'Could not start mic: ' + e.message);
      return;
    }
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.maxAlternatives = 1;

    setStatus('listening', 'Listening...');

    recognition.onresult = async (event) => {
      const text = event.results[event.results.length - 1][0].transcript.trim();
      if (!text) return;
      // Echo filter — if this fires right after Maya finished and the captured
      // text overlaps heavily with what she just said, treat it as the mic
      // hearing her own voice (or the speaker echo) and ignore.
      if (isLikelyEcho(text)) {
        if (active) restartLater(RESTART_DELAY_MS);
        return;
      }
      addBubble('user', text, false);
      messages.push({ role: 'user', content: text });
      await respond();
    };

    recognition.onerror = (e) => {
      // Quiet recovery on common transient errors — restart unless the user stopped.
      if (e.error === 'no-speech' || e.error === 'aborted') {
        if (active && !speaking) restartLater(400);
        return;
      }
      setStatus('error', 'Mic error: ' + e.error);
    };

    recognition.onend = () => {
      // If we're still in the convo and not speaking, restart listening.
      if (active && !speaking) restartLater(250);
    };

    try {
      recognition.start();
    } catch (e) {
      // start() can throw if called too quickly back-to-back; retry shortly.
      restartLater(500);
    }
  }

  function restartLater(ms) {
    clearTimeout(restartTimer);
    restartTimer = setTimeout(() => { if (active) startListening(); }, ms);
  }

  function normalize(s) {
    return (s || '').toLowerCase().replace(/[^a-z0-9 ]+/g, '').replace(/\s+/g, ' ').trim();
  }

  function isLikelyEcho(text) {
    if (!lastSpokenTail) return false;
    if (Date.now() - speakEndedAt > ECHO_WINDOW_MS) return false;
    const a = normalize(text);
    const b = normalize(lastSpokenTail);
    if (!a || !b) return false;
    // Echo if the captured text is short AND substantially appears inside Maya's tail.
    if (a.length < 4) return true;
    if (b.includes(a) || a.includes(b.slice(-Math.min(20, b.length)))) return true;
    // Word overlap heuristic — if >= 60% of words match, it's almost certainly an echo.
    const wa = a.split(' ').filter(Boolean);
    const wb = new Set(b.split(' '));
    const overlap = wa.filter(w => wb.has(w)).length;
    return wa.length > 0 && overlap / wa.length >= 0.6;
  }

  function abortRecognition() {
    if (!recognition) return;
    try { recognition.onresult = null; recognition.onerror = null; recognition.onend = null; } catch (e) {}
    try { recognition.abort(); } catch (e) {}
    recognition = null;
  }

  // Start monitoring mic levels for sustained voice activity. If the user
  // talks while Maya is speaking, we cancel her TTS and reopen recognition —
  // standard "barge-in" behaviour. Browser AEC on the getUserMedia stream
  // subtracts Maya's own audio so we don't bargein on her own voice.
  async function startBargeInWatch() {
    stopBargeInWatch();
    try {
      bargeStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      const AC = window.AudioContext || window.webkitAudioContext;
      bargeAudioCtx = new AC();
      const source = bargeAudioCtx.createMediaStreamSource(bargeStream);
      bargeAnalyser = bargeAudioCtx.createAnalyser();
      bargeAnalyser.fftSize = 1024;
      source.connect(bargeAnalyser);
      const buf = new Float32Array(bargeAnalyser.fftSize);
      bargeAboveSince = 0;

      const tick = () => {
        if (!speaking || !bargeAnalyser) return;
        bargeAnalyser.getFloatTimeDomainData(buf);
        let sumSq = 0;
        for (let i = 0; i < buf.length; i++) sumSq += buf[i] * buf[i];
        const rms = Math.sqrt(sumSq / buf.length);

        const now = Date.now();
        if (rms >= VAD_RMS_THRESHOLD) {
          if (!bargeAboveSince) bargeAboveSince = now;
          if (now - bargeAboveSince >= VAD_SUSTAIN_MS) {
            // The user has been talking long enough — cut Maya off.
            bargeIn();
            return;
          }
        } else {
          bargeAboveSince = 0;
        }
        bargeRafId = requestAnimationFrame(tick);
      };
      bargeRafId = requestAnimationFrame(tick);
    } catch (e) {
      // Mic permission denied or not available — barge-in just won't work,
      // but the rest of the conversation flow stays functional.
      bargeStream = null;
    }
  }

  function stopBargeInWatch() {
    if (bargeRafId) cancelAnimationFrame(bargeRafId);
    bargeRafId = null;
    bargeAboveSince = 0;
    if (bargeStream) {
      try { bargeStream.getTracks().forEach(t => t.stop()); } catch (e) {}
      bargeStream = null;
    }
    if (bargeAudioCtx) {
      try { bargeAudioCtx.close(); } catch (e) {}
      bargeAudioCtx = null;
    }
    bargeAnalyser = null;
  }

  function bargeIn() {
    // User started talking — kill Maya's TTS and hand the mic back to them.
    stopBargeInWatch();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    speaking = false;
    speakEndedAt = Date.now();
    skipBtn.classList.remove('visible');
    setStatus('listening', 'Listening...');
    if (active) restartLater(120);   // very short delay — user is already talking
  }

  async function respond() {
    setStatus('thinking', 'Maya is thinking...');
    try {
      const resp = await fetch(ENDPOINT, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + API_KEY,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: MODEL,
          messages: messages.slice(-20),
          temperature: 0.6,
          max_tokens: 400,
        }),
      });
      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(resp.status + ': ' + errText.slice(0, 120));
      }
      const data = await resp.json();
      const reply = (data.choices && data.choices[0] && data.choices[0].message.content) || '';
      const clean = reply.trim();
      if (!clean) {
        setStatus('idle', 'Empty reply — try again.');
        if (active) restartLater(400);
        return;
      }
      messages.push({ role: 'assistant', content: clean });
      addBubble('assistant', clean, false);
      speak(clean);
    } catch (e) {
      setStatus('error', 'Sorry, the AI service hit a snag: ' + e.message);
      if (active) restartLater(800);
    }
  }

  function speak(text) {
    if (!window.speechSynthesis) {
      if (active) restartLater(RESTART_DELAY_MS);
      return;
    }
    // Hard-stop the mic before Maya opens her mouth — prevents the
    // recognition object from catching her own voice through the speaker.
    clearTimeout(restartTimer);
    abortRecognition();

    speaking = true;
    lastSpokenTail = text.slice(-60);
    skipBtn.classList.add('visible');
    setStatus('speaking', 'Maya is speaking — talk to interrupt.');

    const u = new SpeechSynthesisUtterance(text);
    u.rate = 1.0;
    u.pitch = 1.0;
    if (!voicePref) voicePref = pickVoice();
    if (voicePref) u.voice = voicePref;
    u.onend = () => {
      if (!speaking) return;  // already handled by barge-in or skip
      speaking = false;
      speakEndedAt = Date.now();
      skipBtn.classList.remove('visible');
      stopBargeInWatch();
      if (active) restartLater(RESTART_DELAY_MS);
      else setStatus('idle', 'Idle');
    };
    u.onerror = () => {
      if (!speaking) return;
      speaking = false;
      speakEndedAt = Date.now();
      skipBtn.classList.remove('visible');
      stopBargeInWatch();
      if (active) restartLater(RESTART_DELAY_MS);
    };
    // Some browsers queue old utterances; clear before speaking.
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
    // Start listening for voice-activity-based barge-in.
    startBargeInWatch();
  }

  function skipSpeech() {
    if (!speaking) return;
    stopBargeInWatch();
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();   // triggers u.onend → restart mic
    }
    // Defensive: if the browser swallows onend after cancel(), still recover.
    speaking = false;
    speakEndedAt = Date.now();
    skipBtn.classList.remove('visible');
    if (active) restartLater(200);
  }

  function startConvo() {
    if (!API_KEY) {
      setStatus('error', 'No Groq API key configured. Set GROQ_API_KEY in your .env.');
      return;
    }
    active = true;
    toggle.classList.add('active');
    toggleLabel.textContent = 'Stop';
    startListening();
  }

  function stopConvo() {
    active = false;
    toggle.classList.remove('active');
    toggleLabel.textContent = 'Start conversation';
    clearTimeout(restartTimer);
    abortRecognition();
    stopBargeInWatch();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    speaking = false;
    skipBtn.classList.remove('visible');
    setStatus('idle', 'Conversation paused');
  }

  toggle.addEventListener('click', () => {
    if (active) stopConvo();
    else startConvo();
  });
  skipBtn.addEventListener('click', skipSpeech);

  setStatus('idle', 'Tap "Start conversation" to begin.');
})();
</script>
</body>
</html>
"""


def render_voice_chat_html(api_key: str | None) -> str:
    """Return the HTML for the voice-chat iframe, with the API key and system
    prompt baked in as JSON literals (no escaping pitfalls)."""
    key = api_key or os.getenv("GROQ_API_KEY") or ""
    return (
        _VOICE_CHAT_HTML
        .replace("__API_KEY__", json.dumps(key))
        .replace("__SYSTEM_PROMPT__", json.dumps(SYSTEM_PROMPT))
    )
