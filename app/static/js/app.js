// app/static/js/app.js — v0.4 (clocks + chat + nav)

// ══════════════════════════════════════════
// CHAT
// ══════════════════════════════════════════
let chatHistory = [];
let currentSessionId = null;
let isSending = false;
let msgCounter = 0;

function formatProviderName(provider) {
    const labels = {
        deepseek: 'DeepSeek',
        openai: 'OpenAI',
        gemini: 'Gemini',
    };
    return labels[provider] || provider || '—';
}

function updateProviderBadge(provider) {
    const modelEl = document.getElementById('modelProvider');
    if (modelEl) {
        modelEl.textContent = formatProviderName(provider);
    }
}

window.updateProviderBadge = updateProviderBadge;

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

    const loadingId = appendMessage('assistant', '⏳ Готовлю ответ, ожидайте...');

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

        if (data.provider) {
            updateProviderBadge(data.provider);
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
    const id = ++msgCounter;
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
        if (bubble) bubble.innerHTML = renderMarkdown(text);
    }
}

function renderMarkdown(text) {
    return text
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code style="background:rgba(0,200,100,.1);padding:1px 5px;border-radius:3px;font-family:monospace;">$1</code>')
        .replace(/^\|(.+)\|$/gm, (match, cells) => {
            if (cells.includes('---')) return '';
            const tds = cells.split('|').map(c =>
                `<td style="padding:5px 10px;border:1px solid rgba(0,200,100,.2)">${c.trim()}</td>`
            ).join('');
            return `<tr>${tds}</tr>`;
        })
        .replace(/(<tr>.*<\/tr>)/gs, '<table style="border-collapse:collapse;margin:8px 0;font-size:13px;width:100%">$1</table>')
        .replace(/^### (.+)$/gm, '<h4 style="color:var(--gold);margin:10px 0 4px;font-size:13px;letter-spacing:1px">$1</h4>')
        .replace(/^## (.+)$/gm,  '<h3 style="color:var(--gold-bright);margin:12px 0 5px;font-size:14px">$1</h3>')
        .replace(/^# (.+)$/gm,   '<h2 style="color:var(--gold-bright);margin:14px 0 6px;font-size:16px">$1</h2>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, '<ul style="padding-left:18px;margin:6px 0">$1</ul>')
        .replace(/\n/g, '<br>');
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
