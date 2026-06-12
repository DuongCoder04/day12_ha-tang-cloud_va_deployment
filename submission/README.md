# 🤖 DuongCoder04 AI Agent — Day 12 Submission

> **Production-ready AI chatbot** deployed trên Render, tích hợp LLM thật qua OpenRouter.

## 🌐 Live Demo

| | URL |
|---|---|
| **Chat UI** | https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/chat |
| **Swagger API** | https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/docs |
| **ReDoc** | https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/redoc |
| **Health Check** | https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/health |

### 🔑 Credentials (cho giáo viên test)

- **Chat UI password**: `duong2024`
- **API Key** (cho `/ask`, `/metrics`): xem env var `AGENT_API_KEY` trên Render Dashboard

---

## ✅ Production Checklist

| Feature | Status | Chi tiết |
|---------|--------|----------|
| 12-Factor Config | ✅ | Tất cả config từ env vars |
| Structured JSON Logging | ✅ | Log format JSON parse được |
| API Key Authentication | ✅ | `X-API-Key` header cho `/ask`, `/metrics` |
| Chat UI Authentication | ✅ | Password → HMAC token 7 ngày |
| Rate Limiting | ✅ | Sliding window 20 req/min |
| Daily Cost Guard | ✅ | Hard cap $5/ngày |
| Input Validation | ✅ | Pydantic, max 2000 chars |
| Health + Readiness Probe | ✅ | `/health`, `/ready` |
| Graceful Shutdown | ✅ | SIGTERM handler |
| Security Headers | ✅ | X-Content-Type-Options, X-Frame-Options, etc. |
| CORS | ✅ | Configurable origins |
| Redis Session (fallback) | ✅ | In-memory khi không có Redis |
| Real LLM Integration | ✅ | Google Gemma 4 31B via OpenRouter (free) |
| Conversation History | ✅ | Multi-turn, 20 messages/session |
| Docker Multi-stage Build | ✅ | Non-root user, slim image |
| CI/CD | ✅ | GitHub Actions → Render auto-deploy |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client                                │
│   (Browser /chat UI  ──or──  API client with X-API-Key)     │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Render (Docker Container)                     │
│                                                              │
│  FastAPI + Uvicorn (2 workers, non-root user)               │
│  ├── Security headers middleware                             │
│  ├── CORS middleware                                         │
│  ├── Rate limiter (sliding window, per API key / per IP)    │
│  ├── Cost guard ($5/day)                                     │
│  ├── Auth: X-API-Key (API) / HMAC token (Chat UI)          │
│  └── Session storage (Redis → fallback in-memory)           │
│                      │                                       │
│                      ▼                                       │
│         OpenRouter API (google/gemma-4-31b-it:free)          │
│         └── Fallback: Mock LLM (if no API key)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
submission/
├── app/
│   ├── main.py          # FastAPI app (endpoints, middleware, auth)
│   ├── config.py        # 12-Factor settings from env vars
│   └── chat.py          # Chat UI HTML (dark theme, login screen)
├── utils/
│   └── mock_llm.py      # LLM client (OpenRouter + mock fallback)
├── Dockerfile           # Multi-stage build, non-root user
├── docker-compose.yml   # Full stack: app + Redis
├── requirements.txt     # Pinned dependencies
├── render.yaml          # Render Blueprint deploy config
├── railway.toml         # Railway deploy config
├── .env.example         # Template env vars
├── DEPLOYMENT.md        # Hướng dẫn deploy chi tiết
└── MISSION_ANSWERS.md   # Trả lời bài tập Part 1-5
```

---

## 🚀 API Endpoints

| Method | Path | Auth | Mô tả |
|--------|------|------|--------|
| GET | `/` | ❌ | App info + danh sách endpoint |
| GET | `/chat` | ❌ | Giao diện chatbot web |
| POST | `/chat/login` | ❌ | Xác thực password → nhận token |
| POST | `/chat/send` | 🔐 X-Chat-Token | Gửi tin nhắn cho AI |
| POST | `/ask` | 🔐 X-API-Key | API gọi agent (programmatic) |
| GET | `/health` | ❌ | Liveness probe |
| GET | `/ready` | ❌ | Readiness probe |
| GET | `/metrics` | 🔐 X-API-Key | Usage metrics |
| GET | `/docs` | ❌ | Swagger UI |
| GET | `/redoc` | ❌ | ReDoc API docs |

---

## 🧪 Test nhanh (curl)

```bash
# 1. Health check
curl https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/health

# 2. Login chat UI
curl -X POST https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/chat/login \
  -H "Content-Type: application/json" \
  -d '{"password":"duong2024"}'
# → {"token":"<TOKEN>","expires_in":604800}

# 3. Chat (dùng token nhận được)
curl -X POST https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/chat/send \
  -H "Content-Type: application/json" \
  -H "X-Chat-Token: <TOKEN>" \
  -d '{"question":"Docker là gì?"}'

# 4. API (dùng API key)
curl -X POST https://day12-ha-tang-cloud-va-deployment-ozkn.onrender.com/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <AGENT_API_KEY>" \
  -d '{"question":"Giải thích CI/CD"}'
```

---

## 🏃 Chạy local

```bash
cd submission
pip install -r requirements.txt

# Không cần OpenRouter key — tự dùng mock LLM
uvicorn app.main:app --reload --port 8000

# Hoặc Docker Compose (có Redis)
docker compose up
```

---

## 🔐 Environment Variables

| Variable | Required | Default | Mô tả |
|----------|----------|---------|--------|
| `AGENT_API_KEY` | ✅ prod | `dev-key-...` | API key cho `/ask`, `/metrics` |
| `JWT_SECRET` | ✅ prod | `dev-jwt-...` | Secret ký token |
| `OPENROUTER_API_KEY` | ❌ | (empty) | Key OpenRouter. Bỏ trống = mock |
| `OPENROUTER_MODEL` | ❌ | `google/gemma-4-31b-it:free` | Model LLM |
| `CHAT_PASSWORD` | ❌ | `duong2024` | Password bảo vệ chat UI |
| `RATE_LIMIT_PER_MINUTE` | ❌ | `20` | Rate limit |
| `DAILY_BUDGET_USD` | ❌ | `5.0` | Budget cap/ngày |
| `REDIS_URL` | ❌ | (empty) | Redis URL, fallback in-memory |

---

## 👤 Thông tin sinh viên

| | |
|---|---|
| **Họ tên** | Nguyễn Văn Dương |
| **MSSV** | 2A202600967 |
| **GitHub** | [DuongCoder04](https://github.com/DuongCoder04) |
| **Lab** | Day 12 — Cloud Infrastructure & Deployment |
