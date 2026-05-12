// ============================================================
// AIKIVAVIORA — Core Analytics System
// app.js
// ============================================================

// ── SESSION ID ───────────────────────────────────────────────
function randHex(n) {
    return [...crypto.getRandomValues(new Uint8Array(n))]
        .map(b => b.toString(16).padStart(2, '0')).join('');
}

const SESSION_ID = `${randHex(4)}-${randHex(2)}-${randHex(2)}`;

document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('sessionId');
    if (el) el.textContent = SESSION_ID;
});

// ── WORLD CLOCKS ─────────────────────────────────────────────
const ZONES = [
    { time: 'clock-usa', date: 'date-usa', tz: 'America/New_York' },
    { time: 'clock-uk',  date: 'date-uk',  tz: 'Europe/London'    },
    { time: 'clock-ger', date: 'date-ger', tz: 'Europe/Berlin'    },
    { time: 'clock-fin', date: 'date-fin', tz: 'Europe/Helsinki'  },
    { time: 'clock-ru',  date: 'date-ru',  tz: 'Europe/Moscow'    },
];

const MONTHS = ['JAN','FEB','MAR','APR','MAY','JUN',
                'JUL','AUG','SEP','OCT','NOV','DEC'];

function pad(n) { return String(n).padStart(2, '0'); }

function tickClocks() {
    const now = new Date();
    ZONES.forEach(z => {
        const d = new Date(now.toLocaleString('en-US', { timeZone: z.tz }));
        const timeEl = document.getElementById(z.time);
        const dateEl = document.getElementById(z.date);
        if (timeEl) timeEl.textContent =
            `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
        if (dateEl) dateEl.textContent =
            `${pad(d.getDate())} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
    });
}

tickClocks();
setInterval(tickClocks, 1000);

// ── NAV ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-item').forEach(el => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.nav-item')
                .forEach(i => i.classList.remove('active'));
            el.classList.add('active');
        });
    });
});

// ── CHAT ──────────────────────────────────────────────────────
function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const input   = document.getElementById('chatInput');
    const text    = input.value.trim();
    if (!text) return;

    // Показываем сообщение пользователя
    addBubble(text, 'user-msg');
    input.value = '';
    input.disabled = true;

    // Индикатор загрузки
    const loadId = addBubble('⏳ Thinking...', 'ai-msg', true);

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message:    text,
                session_id: SESSION_ID
            })
        });

        const data = await res.json();

        // Убираем индикатор
        removeBubble(loadId);

        if (data.status === 'ok') {
            addBubble(data.response, 'ai-msg');
        } else {
            addBubble(`❌ Error: ${data.message}`, 'ai-msg error');
        }

    } catch (err) {
        removeBubble(loadId);
        addBubble(`❌ Connection error: ${err.message}`, 'ai-msg error');
    } finally {
        input.disabled = false;
        input.focus();
    }
}

let bubbleCounter = 0;

function addBubble(text, cls, temp = false) {
    const box = document.getElementById('chatMessages');
    const id  = `bubble-${++bubbleCounter}`;
    const d   = document.createElement('div');
    d.className = `msg ${cls}`;
    d.id = id;
    d.innerHTML = `<div class="msg-bubble">${text}</div>`;
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
    return id;
}

function removeBubble(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
