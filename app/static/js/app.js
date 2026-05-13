// app/static/js/app.js — v0.4 (clocks + chat + nav)

// ══════════════════════════════════════════
// CHAT
// ══════════════════════════════════════════
let chatHistory = [];
let currentSessionId = null;
let isSending = false;

function handleKey(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        if (!isSending) sendMessage();
    }
}

async function sendMessage() {
    if (isSending) return;

    const input = document.getElementById('chatInput');
    const userMsg = input.value.trim();
    if (!userMsg) return;

    isSending = true;
    input.value = '';

    appendMessage('user', userMsg);
    chatHistory.push({ role: 'user', content: userMsg });

    const loadingId = appendMessage('assistant', '⏳ Анализирую данные...');

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: userMsg,
                session_id: currentSessionId,
                history: chatHistory.slice(-10)
            })
        });

        const data = await res.json();

        if (data.session_id) {
            currentSessionId = data.session_id;
            const sessEl = document.getElementById('sessionId');
            if (sessEl) sessEl.textContent = currentSessionId.substring(0, 8) + '...';
        }

        updateMessage(loadingId, data.reply);
        chatHistory.push({ role: 'assistant', content: data.reply });

    } catch (err) {
        console.error('Chat error:', err);
        updateMessage(loadingId, `❌ Ошибка: ${err.message}`);
    } finally {
        isSending = false;
    }
}

function appendMessage(role, text) {
    const id = Date.now();
    const chat = document.getElementById('chatMessages');
    if (!chat) return null;

    const div = document.createElement('div');
    div.id = `msg-${id}`;
    div.className = `msg ${role === 'user' ? 'user-msg' : 'ai-msg'}`;

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.textContent = text;

    div.appendChild(bubble);
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return id;
}

function updateMessage(id, text) {
    const el = document.getElementById(`msg-${id}`);
    if (el) {
        const bubble = el.querySelector('.msg-bubble');
        if (bubble) bubble.textContent = text;
    }
}

// ══════════════════════════════════════════
// WORLD CLOCKS
// ══════════════════════════════════════════
const CLOCKS = [
    { id: 'usa', clockId: 'clock-usa', dateId: 'date-usa', offset: -4  },  // EDT
    { id: 'uk',  clockId: 'clock-uk',  dateId: 'date-uk',  offset: +1  },  // BST
    { id: 'ger', clockId: 'clock-ger', dateId: 'date-ger', offset: +2  },  // CEST
    { id: 'fin', clockId: 'clock-fin', dateId: 'date-fin', offset: +3  },  // EEST
    { id: 'ru',  clockId: 'clock-ru',  dateId: 'date-ru',  offset: +3  },  // MSK
];

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const DAYS   = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function pad(n) { return String(n).padStart(2, '0'); }

function updateClocks() {
    const now = new Date();
    const utcMs = now.getTime() + now.getTimezoneOffset() * 60000;

    CLOCKS.forEach(({ clockId, dateId, offset }) => {
        const local = new Date(utcMs + offset * 3600000);
        const h = pad(local.getHours());
        const m = pad(local.getMinutes());
        const s = pad(local.getSeconds());

        const clockEl = document.getElementById(clockId);
        const dateEl  = document.getElementById(dateId);

        if (clockEl) clockEl.textContent = `${h}:${m}:${s}`;
        if (dateEl)  dateEl.textContent  =
            `${DAYS[local.getDay()]}, ${local.getDate()} ${MONTHS[local.getMonth()]}`;
    });
}

// ══════════════════════════════════════════
// INIT
// ══════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ AIKIVAVIORA Chat UI initialized');

    // Запускаем часы сразу и каждую секунду
    updateClocks();
    setInterval(updateClocks, 1000);
});
