"""
Chat UI — Giao diện chatbot đơn giản để test agent trên trình duyệt.
Có màn hình login bảo vệ bằng password + HMAC token 7 ngày.
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
            --error: #ef4444;
            --success: #10b981;
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

        /* ── Login screen ── */
        #loginScreen {
            position: fixed; inset: 0;
            background: var(--bg);
            display: flex; align-items: center; justify-content: center;
            z-index: 100;
        }
        .login-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px;
            width: 100%; max-width: 380px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: fadeIn 0.4s ease;
        }
        .login-card .logo {
            width: 52px; height: 52px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 22px; color: white;
            margin: 0 auto 20px;
        }
        .login-card h2 {
            text-align: center;
            font-size: 20px; font-weight: 600;
            margin-bottom: 6px;
        }
        .login-card p {
            text-align: center;
            font-size: 13px; color: var(--text-secondary);
            margin-bottom: 28px;
        }
        .login-card label {
            display: block;
            font-size: 12px; font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 6px;
            text-transform: uppercase; letter-spacing: 0.5px;
        }
        .login-card input {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 12px 16px;
            font-size: 14px; color: var(--text);
            outline: none; margin-bottom: 16px;
            transition: border-color 0.2s;
        }
        .login-card input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        .login-card button {
            width: 100%;
            background: var(--accent);
            border: none; border-radius: var(--radius);
            padding: 13px; color: white;
            font-size: 15px; font-weight: 600;
            cursor: pointer; transition: all 0.2s;
        }
        .login-card button:hover { background: #2563eb; }
        .login-card button:disabled { opacity: 0.6; cursor: not-allowed; }
        .login-error {
            color: var(--error);
            font-size: 13px; text-align: center;
            margin-top: 12px; min-height: 18px;
        }

        /* ── Header ── */
        .header {
            padding: 14px 24px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; gap: 12px;
        }
        .header .logo {
            width: 34px; height: 34px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 13px; color: white;
        }
        .header h1 { font-size: 15px; font-weight: 600; }
        .header .badge {
            font-size: 11px; padding: 3px 8px;
            background: rgba(16,185,129,0.15); color: #10b981;
            border-radius: 20px; font-weight: 500;
        }
        .header .model-badge {
            font-size: 11px; padding: 3px 8px;
            background: rgba(139,92,246,0.15); color: #a78bfa;
            border-radius: 20px; font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
        }
        .header .logout-btn {
            margin-left: auto;
            background: none; border: 1px solid var(--border);
            border-radius: 8px; padding: 5px 12px;
            color: var(--text-muted); font-size: 12px;
            cursor: pointer; transition: all 0.2s;
        }
        .header .logout-btn:hover { border-color: var(--error); color: var(--error); }

        /* ── Chat area ── */
        .chat-container {
            flex: 1; overflow-y: auto;
            padding: 24px;
            display: flex; flex-direction: column; gap: 16px;
        }
        .chat-container::-webkit-scrollbar { width: 6px; }
        .chat-container::-webkit-scrollbar-track { background: transparent; }
        .chat-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

        .message {
            display: flex; gap: 10px;
            max-width: 80%;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot  { align-self: flex-start; }

        .message .avatar {
            width: 32px; height: 32px; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 600; flex-shrink: 0;
        }
        .message.user .avatar { background: var(--user-bg); color: white; }
        .message.bot  .avatar { background: #374151; color: #a5b4fc; }

        .message .bubble {
            padding: 12px 16px; border-radius: var(--radius);
            font-size: 14px; line-height: 1.65; word-break: break-word;
        }
        .message.user .bubble {
            background: var(--user-bg); color: white;
            border-bottom-right-radius: 4px;
        }
        .message.bot .bubble {
            background: var(--bot-bg); color: var(--text);
            border: 1px solid var(--border);
            border-bottom-left-radius: 4px;
            white-space: pre-wrap;
        }
        .message .bubble .meta {
            margin-top: 6px; font-size: 11px;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Typing indicator */
        .typing { display: flex; gap: 4px; padding: 6px 0; }
        .typing span {
            width: 7px; height: 7px;
            background: var(--text-muted); border-radius: 50%;
            animation: bounce 1.2s infinite;
        }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30%           { transform: translateY(-6px); }
        }

        /* Welcome */
        .welcome {
            text-align: center; padding: 48px 20px;
            color: var(--text-secondary);
        }
        .welcome h2 { font-size: 20px; font-weight: 600; color: var(--text); margin-bottom: 8px; }
        .welcome p  { font-size: 14px; margin-bottom: 20px; }
        .welcome .suggestions {
            display: flex; flex-wrap: wrap; justify-content: center; gap: 8px;
        }
        .welcome .suggestions button {
            background: var(--bg-input); border: 1px solid var(--border);
            color: var(--text-secondary); padding: 8px 14px;
            border-radius: 20px; font-size: 13px; cursor: pointer;
            transition: all 0.2s;
        }
        .welcome .suggestions button:hover {
            background: var(--accent-glow); border-color: var(--accent); color: var(--text);
        }

        /* Input area */
        .input-area {
            padding: 14px 24px;
            background: var(--bg-surface); border-top: 1px solid var(--border);
        }
        .input-wrapper {
            display: flex; gap: 10px;
            max-width: 800px; margin: 0 auto;
        }
        .input-wrapper input {
            flex: 1;
            background: var(--bg-input); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 12px 16px;
            font-size: 14px; color: var(--text); outline: none;
            transition: border-color 0.2s;
        }
        .input-wrapper input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        .input-wrapper input::placeholder { color: var(--text-muted); }
        .input-wrapper button {
            background: var(--accent); border: none;
            border-radius: var(--radius); padding: 12px 20px;
            color: white; font-size: 14px; font-weight: 500;
            cursor: pointer; transition: all 0.2s;
            display: flex; align-items: center; gap: 6px;
        }
        .input-wrapper button:hover { background: #2563eb; transform: scale(1.02); }
        .input-wrapper button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    </style>
</head>
<body>

<!-- ── Login screen ── -->
<div id="loginScreen">
    <div class="login-card">
        <div class="logo">D</div>
        <h2>DuongCoder04 AI Agent</h2>
        <p>Nhập password để truy cập chatbot</p>
        <label>Password</label>
        <input type="password" id="pwInput" placeholder="Nhập password..."
               onkeydown="if(event.key==='Enter') doLogin()">
        <button id="loginBtn" onclick="doLogin()">Đăng nhập</button>
        <div class="login-error" id="loginError"></div>
    </div>
</div>

<!-- ── Main UI ── -->
<div class="header">
    <div class="logo">D</div>
    <h1>DuongCoder04 AI Agent</h1>
    <span class="badge">● Online</span>
    <span class="model-badge">Gemma 4 31B · Free</span>
    <button class="logout-btn" onclick="logout()">Đăng xuất</button>
</div>

<div class="chat-container" id="chat">
    <div class="welcome">
        <h2>👋 Chào mừng!</h2>
        <p>Hãy hỏi tôi bất kỳ điều gì. Powered by Google Gemma 4 31B (free).</p>
        <div class="suggestions">
            <button onclick="sendSuggestion(this)">AI là gì?</button>
            <button onclick="sendSuggestion(this)">Giải thích Docker</button>
            <button onclick="sendSuggestion(this)">Cloud deployment là gì?</button>
            <button onclick="sendSuggestion(this)">Viết Python hello world</button>
        </div>
    </div>
</div>

<div class="input-area">
    <div class="input-wrapper">
        <input type="text" id="msgInput" placeholder="Nhập câu hỏi..." autocomplete="off"
               onkeydown="if(event.key==='Enter') sendMessage()">
        <button id="sendBtn" onclick="sendMessage()">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
            Gửi
        </button>
    </div>
</div>

<script>
    const STORAGE_TOKEN = 'chat_token';
    const STORAGE_SESSION = 'chat_session';

    let sessionId = localStorage.getItem(STORAGE_SESSION) || crypto.randomUUID();
    localStorage.setItem(STORAGE_SESSION, sessionId);
    let welcomeShown = true;

    // ── Auth ──────────────────────────────────────────────
    function getToken() { return localStorage.getItem(STORAGE_TOKEN) || ''; }

    function logout() {
        localStorage.removeItem(STORAGE_TOKEN);
        document.getElementById('loginScreen').style.display = 'flex';
        document.getElementById('pwInput').value = '';
        document.getElementById('loginError').textContent = '';
    }

    async function doLogin() {
        const pw = document.getElementById('pwInput').value.trim();
        if (!pw) return;
        const btn = document.getElementById('loginBtn');
        const err = document.getElementById('loginError');
        btn.disabled = true;
        btn.textContent = 'Đang xác thực...';
        err.textContent = '';
        try {
            const res = await fetch('/chat/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: pw }),
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem(STORAGE_TOKEN, data.token);
                document.getElementById('loginScreen').style.display = 'none';
                document.getElementById('msgInput').focus();
            } else {
                err.textContent = data.detail || 'Sai password';
            }
        } catch (e) {
            err.textContent = 'Lỗi kết nối: ' + e.message;
        }
        btn.disabled = false;
        btn.textContent = 'Đăng nhập';
    }

    // Kiểm tra token khi load
    (function init() {
        const token = getToken();
        if (token) {
            document.getElementById('loginScreen').style.display = 'none';
        }
        document.getElementById('pwInput').focus();
    })();

    // ── Chat ─────────────────────────────────────────────
    function sendSuggestion(btn) {
        document.getElementById('msgInput').value = btn.textContent;
        sendMessage();
    }

    function addMessage(text, role, meta) {
        if (welcomeShown) {
            const w = document.getElementById('chat').querySelector('.welcome');
            if (w) w.remove();
            welcomeShown = false;
        }
        const div = document.createElement('div');
        div.className = `message ${role}`;
        div.innerHTML = `
            <div class="avatar">${role === 'user' ? 'U' : 'AI'}</div>
            <div class="bubble">${escapeHtml(text)}${meta ? '<div class="meta">'+meta+'</div>' : ''}</div>
        `;
        document.getElementById('chat').appendChild(div);
        document.getElementById('chat').scrollTop = 9999;
        return div;
    }

    function showTyping() {
        const div = document.createElement('div');
        div.className = 'message bot'; div.id = 'typing';
        div.innerHTML = '<div class="avatar">AI</div><div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>';
        document.getElementById('chat').appendChild(div);
        document.getElementById('chat').scrollTop = 9999;
    }

    function hideTyping() {
        const el = document.getElementById('typing');
        if (el) el.remove();
    }

    function escapeHtml(t) {
        const d = document.createElement('div');
        d.textContent = t;
        return d.innerHTML;
    }

    async function sendMessage() {
        const input = document.getElementById('msgInput');
        const text = input.value.trim();
        if (!text) return;

        const token = getToken();
        if (!token) { logout(); return; }

        input.value = '';
        document.getElementById('sendBtn').disabled = true;
        addMessage(text, 'user');
        showTyping();

        try {
            const res = await fetch('/chat/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Chat-Token': token,
                },
                body: JSON.stringify({ question: text, session_id: sessionId }),
            });
            const data = await res.json();
            hideTyping();

            if (res.status === 401) {
                // Token hết hạn → về login
                logout();
                return;
            }
            if (res.ok) {
                const meta = `model: ${data.model} · session: ${data.session_id.slice(0,8)}`;
                addMessage(data.answer, 'bot', meta);
                sessionId = data.session_id;
                localStorage.setItem(STORAGE_SESSION, sessionId);
            } else {
                addMessage(`Lỗi: ${data.detail || 'Có lỗi xảy ra'}`, 'bot');
            }
        } catch (e) {
            hideTyping();
            addMessage(`Lỗi kết nối: ${e.message}`, 'bot');
        }

        document.getElementById('sendBtn').disabled = false;
        input.focus();
    }
</script>
</body>
</html>
"""
