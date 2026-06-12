"""
LLM client — gọi OpenRouter nếu có OPENROUTER_API_KEY, fallback về mock.
"""
import os
import time
import random
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL   = os.getenv("OPENROUTER_MODEL", "anthropic/claude-haiku-4-5")
OPENROUTER_BASE    = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Bạn là một AI assistant thông minh, thân thiện, được deploy trên cloud bởi DuongCoder04.
Trả lời ngắn gọn, súc tích bằng ngôn ngữ người dùng đang dùng (tiếng Việt hoặc tiếng Anh).
Nếu câu hỏi liên quan đến kỹ thuật (Docker, cloud, AI, lập trình), hãy giải thích rõ ràng."""

# ─── Mock fallback ────────────────────────────────────────
_MOCK = {
    "default": [
        "Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenRouter.",
        "Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.",
        "Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.",
    ],
    "docker":  ["Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!"],
    "deploy":  ["Deployment là quá trình đưa code từ máy bạn lên server để người khác dùng được."],
    "health":  ["Agent đang hoạt động bình thường. All systems operational."],
}

def _mock_ask(question: str) -> str:
    time.sleep(0.1 + random.uniform(0, 0.05))
    q = question.lower()
    for kw, responses in _MOCK.items():
        if kw in q:
            return random.choice(responses)
    return random.choice(_MOCK["default"])


# ─── OpenRouter call ──────────────────────────────────────
def _openrouter_ask(question: str, history: list | None = None) -> str:
    """
    Gọi OpenRouter API đồng bộ bằng httpx.
    history: list of {"role": "user"|"assistant", "content": "..."}
    """
    import httpx

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history[-10:])  # tối đa 10 tin nhắn gần nhất
    messages.append({"role": "user", "content": question})

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                OPENROUTER_BASE,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type":  "application/json",
                    "HTTP-Referer":  "https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com",
                    "X-Title":       "DuongCoder04 AI Agent",
                },
                json={
                    "model":       OPENROUTER_MODEL,
                    "messages":    messages,
                    "max_tokens":  512,
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.warning(f"OpenRouter error: {e} — falling back to mock")
        return _mock_ask(question)


# ─── Public API ───────────────────────────────────────────
def ask(question: str, delay: float = 0.0, history: list | None = None) -> str:
    """
    Gọi LLM thật nếu có OPENROUTER_API_KEY, ngược lại dùng mock.
    """
    if OPENROUTER_API_KEY:
        return _openrouter_ask(question, history=history)
    return _mock_ask(question)


def ask_stream(question: str):
    """
    Streaming mock — yield từng token (dùng cho demo).
    OpenRouter streaming chưa được implement ở đây.
    """
    response = ask(question)
    for word in response.split():
        time.sleep(0.03)
        yield word + " "
