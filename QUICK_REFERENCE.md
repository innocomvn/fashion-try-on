# ⚡ Quick Reference - Fashion Try-On App

Tham khảo nhanh tất cả commands và URLs.

---

## 🚀 Chạy App

### Option 1: Local Only (Localhost)

```bash
# Basic
python -m uvicorn backend.main:app --reload

# Hoặc dùng script
./backend/run_server.sh
```

**Access:** http://localhost:8000/app

---

### Option 2: Ngrok (Internet Access) ⭐ Recommended for testing

```bash
# Auto-start cả backend + ngrok
./start_with_ngrok.sh

# Hoặc manual (2 terminals)
# Terminal 1:
python -m uvicorn backend.main:app --reload

# Terminal 2:
ngrok http 8000
```

**Access:**
- Local: http://localhost:8000/app
- Public: https://random-string.ngrok-free.app/app
- Dashboard: http://localhost:4040

---

## 📋 URLs Quan Trọng

| Service | URL | Mô tả |
|---------|-----|-------|
| **Frontend** | `/app` | Giao diện web |
| **API Docs** | `/docs` | Swagger UI |
| **ReDoc** | `/redoc` | API documentation |
| **Health Check** | `/` | API status |
| **Create Task** | `POST /api/v1/tryon` | Tạo try-on task |
| **Check Status** | `GET /api/v1/tryon/{id}` | Kiểm tra trạng thái |
| **Download Result** | `GET /api/v1/tryon/{id}/result` | Tải ảnh kết quả |

---

## 🔧 Setup Commands

### Lần đầu tiên:

```bash
# Clone repo
git clone https://github.com/your-repo/fashion-try-on.git
cd fashion-try-on

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Setup .env
cp backend/.env.example backend/.env
# Edit backend/.env với API keys
```

### Ngrok setup (1 lần):

```bash
# Install
sudo snap install ngrok

# Setup token
ngrok config add-authtoken YOUR_TOKEN
```

---

## 🎯 Test Commands

### Test API với curl:

```bash
# Health check
curl http://localhost:8000/

# Create task
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@person.jpg" \
  -F "garment_image=@shirt.jpg" \
  -F "provider=replicate"

# Check status
curl http://localhost:8000/api/v1/tryon/{task_id}
```

### Test với Python script:

```bash
python backend/test_api.py \
  --model person.jpg \
  --garment shirt.jpg \
  --provider replicate
```

---

## 📦 Dependencies

**Core:**
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pydantic 2.5.3
- python-dotenv 1.0.0

**External APIs:**
- replicate 0.22.0
- requests 2.31.0

**Production:**
- gunicorn 21.2.0

**Install all:**
```bash
pip install -r backend/requirements.txt
```

---

## 🔑 Environment Variables (.env)

**Minimum (Replicate):**
```bash
USE_EXTERNAL_API=True
API_PROVIDER="replicate"
REPLICATE_API_TOKEN="r8_xxxxx"
```

**On-Premise:**
```bash
USE_ON_PREMISE=True
MODEL_TYPE="idm-vton"
DEVICE="cuda"
```

**Production:**
```bash
DEBUG=False
DATABASE_URL="postgresql://..."
SECRET_KEY="your-secret"
```

---

## 📊 Logs

```bash
# Backend logs
tail -f logs/backend.log
tail -f logs/error.log

# Ngrok logs
tail -f logs/ngrok.log

# App logs (if using logger)
tail -f logs/app.log
```

---

## 🐛 Common Issues

### Port 8000 already in use:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 8001
```

### Can't import modules:
```bash
# Activate venv
source venv/bin/activate

# Reinstall
pip install -r backend/requirements.txt
```

### Ngrok not found:
```bash
# Install
sudo snap install ngrok

# Or
brew install ngrok/ngrok/ngrok
```

### API timeout:
```bash
# Increase timeout in frontend/js/app.js
MAX_POLL_ATTEMPTS: 100  # Change this

# Or in backend/config.py
API_TIMEOUT: 300  # 5 minutes
```

---

## 📁 Project Structure

```
fashion-try-on/
├── backend/              # FastAPI backend
│   ├── main.py          # Main app
│   ├── config.py        # Settings
│   ├── services/        # On-premise & API services
│   ├── utils/           # Database, files, logging
│   └── models/          # Pydantic schemas
├── frontend/            # Web UI
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── uploads/             # Uploaded images (auto-created)
├── results/             # Result images (auto-created)
├── models/              # AI model weights (for on-premise)
└── logs/                # Log files (auto-created)
```

---

## 🎓 Documentation Files

| File | Purpose |
|------|---------|
| `RUN_APP.md` | Full running guide |
| `QUICK_TEST_NGROK.md` | 5-min ngrok setup |
| `NGROK_SETUP.md` | Complete ngrok guide |
| `BACKEND_QUICKSTART.md` | Backend quick start |
| `DEPLOYMENT.md` | Production deployment |
| `PROJECT_SUMMARY.md` | Project overview |
| `backend/README.md` | Backend API docs |
| `frontend/README.md` | Frontend docs |
| **`QUICK_REFERENCE.md`** | This file! |

---

## 🔥 Most Common Workflows

### 1. Development (Local only):
```bash
python -m uvicorn backend.main:app --reload
# Open: http://localhost:8000/app
```

### 2. Testing with Ngrok (Share with others):
```bash
./start_with_ngrok.sh
# Share: https://xxx.ngrok-free.app/app
```

### 3. Production Deployment:
```bash
gunicorn backend.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### 4. Docker:
```bash
docker build -t fashion-tryon .
docker run -p 8000:8000 fashion-tryon
```

---

## 💡 Pro Tips

### 1. Use .env for different environments:
```bash
.env.development
.env.production
.env.testing
```

### 2. Multiple terminals:
```
Terminal 1: Backend
Terminal 2: Ngrok
Terminal 3: Logs
Terminal 4: Testing
```

### 3. Browser bookmarks:
```
http://localhost:8000/app    (Frontend)
http://localhost:8000/docs   (API Docs)
http://localhost:4040        (Ngrok Dashboard)
```

### 4. Quick restart:
```bash
# Kill all
pkill -f uvicorn
pkill -f ngrok

# Restart
./start_with_ngrok.sh
```

---

## 📱 Mobile Testing Checklist

- [ ] Install ngrok
- [ ] Setup authtoken
- [ ] Run `./start_with_ngrok.sh`
- [ ] Copy public URL
- [ ] Open on phone browser
- [ ] Test upload & try-on
- [ ] Share with friends!

---

## ⚡ Speed Reference

| Action | Time |
|--------|------|
| Install dependencies | 1-2 min |
| Start backend | 2-3 sec |
| Start ngrok | 2-3 sec |
| Upload images | < 1 sec |
| Process (Replicate) | 20-40 sec |
| Process (On-premise GPU) | 10-30 sec |
| Process (On-premise CPU) | 60-120 sec |

---

## 🎯 Provider Comparison

| Provider | Setup | Speed | Cost | Best For |
|----------|-------|-------|------|----------|
| On-Premise | Hard | Fast | Free* | Production |
| Replicate | Easy | Medium | $0.01/img | Testing |
| Fal.ai | Easy | Fast | $0.02/img | Speed |
| HeyBeauty | Medium | Medium | Contact | Pro |

*After initial GPU investment

---

## 📞 Getting Help

1. **Documentation**: Read files above
2. **API Docs**: http://localhost:8000/docs
3. **Logs**: Check `logs/` directory
4. **Issues**: GitHub issues
5. **Community**: Discord/Slack (if available)

---

**Last Updated:** 2024-01-XX

**Quick Links:**
- [Run App Guide](RUN_APP.md)
- [Ngrok Quick Start](QUICK_TEST_NGROK.md)
- [Full Ngrok Guide](NGROK_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)

**Happy Coding! 🚀**
