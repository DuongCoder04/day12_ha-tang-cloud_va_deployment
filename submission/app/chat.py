"""
Chat UI — Giao diện chatbot đơn giản để test agent trên trình duyệt.
"""

CHAT_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DuongCoder04 AI Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg: #0f1419;
            --bg-surface: #1a1f2e;
            --bg-chat: #141821;
            --bg-input: #1e2433;
            --border: rgba(255,255,255,0.08);
            --text: #e8edf5;
            --text-secondary: #8b95a5;
            --text-muted: #5a6577;
            --accent: #3b82f6;
            --accent-glow: rgba(59,130,246,0.15);
            --user-bg: #2563eb;
            --bot-bg: #1e293b;
            --radius: 12px;
            --shadow: 0 4px 24px rgba(0,0,0,0.3);
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Header */
        .header {
            padding: 16px 24px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header .logo {
            width: 36px; height: 36px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 14px; color: white;
        }
        .header h1 {
            font-size: 16px; font-weight: 600; color: var(--text);
        }
        .header .badge {
            font-size: 11px;
            padding: 3px 8px;
            background: rgba(16,185,129,0.15);
            color: #10b981;
            border-radius: 20px;
            font-weight: 500;
        }
        .header .info {
            margin-left: auto;
            font-size: 12px;
            color: var(--text-muted);
        }

        /* Chat area */
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .chat-container::-webkit-scrollbar { width: 6px; }
        .chat-container::-webkit-scrollbar-track { background: transparent; }
        .chat-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

        .message {
            display: flex;
            gap: 10px;
            max-width: 80%;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot { align-self: flex-start; }

        .message .avatar {
            width: 32px; height: 32px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; font-weight: 600;
            flex-shrink: 0;
        }
        .message.user .avatar { background: var(--user-bg); color: white; }
        .message.bot .avatar { background: #374151; color: #a5b4fc; }

        .message .bubble {
            padding: 12px 16px;
            border-radius: var(--radius);
            font-size: 14px;
            line-height: 1.6;
            word-break: break-word;
        }
        .message.user .bubble {
            background: var(--user-bg);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.bot .bubble {
            background: var(--bot-bg);
            color: var(--text);
            border: 1px solid var(--border);
            border-bottom-left-radius: 4px;
        }
        .message .bubble .meta {
            margin-top: 6px;
            font-size: 11px;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Typing indicator */
        .typing {
            display: flex; gap: 4px; padding: 8px 0;
        }
        .typing span {
            width: 7px; height: 7px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: bounce 1.2s infinite;
        }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-6px); }
        }

        /* Welcome */
        .welcome {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-secondary);
        }
        .welcome h2 {
            font-size: 20px; font-weight: 600; color: var(--text);
            margin-bottom: 8px;
        }
        .welcome p { font-size: 14px; margin-bottom: 20px; }
        .welcome .suggestions {
            display: flex; flex-wrap: wrap; justify-content: center; gap: 8px;
        }
        .welcome .suggestions button {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .welcome .suggestions button:hover {
            background: var(--accent-glow);
            border-color: var(--accent);
            color: var(--text);
        }

        /* Input area */
        .input-area {
            padding: 16px 24px;
            background: var(--bg-surface);
            border-top: 1px solid var(--border);
        }
        .input-wrapper {
            display: flex;
            gap: 10px;
            max-width: 800px;
            margin: 0 auto;
        }
        .input-wrapper input {
            flex: 1;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-size: 14px;
            color: var(--text);
            outline: none;
            transition: border-color 0.2s;
        }
        .input-wrapper input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        .input-wrapper input::placeholder { color: var(--text-muted); }
        .input-wrapper button {
            background: var(--accent);
            border: none;
            border-radius: var(--radius);
            padding: 12px 20px;
            color: white;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex; align-items: center; gap: 6px;
        }
        .input-wrapper button:hover { background: #2563eb; transform: scale(1.02); }
        .input-wrapper button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">D</div>
        <h1>DuongCoder04 AI Agent</h1>
        <span class="badge">● Online</span>
        <span class="info">Production — Day 12 Lab</span>
    </div>

    <div class="chat-container" id="chat">
        <div class="welcome">
            <h2>👋 Chào mừng bạn!</h2>
            <p>Hãy hỏi tôi bất kỳ điều gì. Đây là AI Agent demo sử dụng Mock LLM.</p>
            <div class="suggestions">
                <button onclick="sendSuggestion(this)">AI là gì?</button>
                <button onclick="sendSuggestion(this)">Giải thích Docker</button>
                <button onclick="sendSuggestion(this)">Cloud deployment là gì?</button>
                <button onclick="sendSuggestion(this)">Hello World!</button>
            </div>
        </div>
    </div>

    <div class="input-area">
        <div class="input-wrapper">
            <input type="text" id="input" placeholder="Nhập câu hỏi của bạn..." autocomplete="off"
                   onkeydown="if(event.key==='Enter')sendMessage()">
            <button id="sendBtn" onclick="sendMessage()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                </svg>
                Gửi
            </button>
        </div>
    </div>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const sendBtn = document.getElementById('sendBtn');
        let sessionId = localStorage.getItem('chat_session') || crypto.randomUUID();
        localStorage.setItem('chat_session', sessionId);
        let welcomeShown = true;

        function sendSuggestion(btn) {
            input.value = btn.textContent;
            sendMessage();
        }

        function addMessage(text, role, meta) {
            if (welcomeShown) {
                const welcome = chat.querySelector('.welcome');
                if (welcome) welcome.remove();
                welcomeShown = false;
            }
            const div = document.createElement('div');
            div.className = `message ${role}`;
            const avatar = role === 'user' ? 'U' : 'AI';
            let metaHtml = meta ? `<div class="meta">${meta}</div>` : '';
            div.innerHTML = `
                <div class="avatar">${avatar}</div>
                <div class="bubble">${escapeHtml(text)}${metaHtml}</div>
            `;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
            return div;
        }

        function showTyping() {
            const div = document.createElement('div');
            div.className = 'message bot';
            div.id = 'typing';
            div.innerHTML = `
                <div class="avatar">AI</div>
                <div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>
            `;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        function hideTyping() {
            const el = document.getElementById('typing');
            if (el) el.remove();
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            input.value = '';
            sendBtn.disabled = true;
            addMessage(text, 'user');
            showTyping();

            try {
                const res = await fetch('/chat/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: text, session_id: sessionId })
                });
                const data = await res.json();
                hideTyping();

                if (res.ok) {
                    const meta = `model: ${data.model} · session: ${data.session_id.slice(0,8)}`;
                    addMessage(data.answer, 'bot', meta);
                    sessionId = data.session_id;
                    localStorage.setItem('chat_session', sessionId);
                } else {
                    addMessage(`Error: ${data.detail || 'Có lỗi xảy ra'}`, 'bot');
                }
            } catch (e) {
                hideTyping();
                addMessage(`Connection error: ${e.message}`, 'bot');
            }

            sendBtn.disabled = false;
            input.focus();
        }

        input.focus();
    </script>
</body>
</html>
"""
