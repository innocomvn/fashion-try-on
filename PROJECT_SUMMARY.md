# 📦 Fashion Try-On - Tổng quan Project

## 🎯 Mô tả

**Fashion Try-On** là ứng dụng AI thử đồ ảo, cho phép người dùng upload ảnh người mẫu và ảnh quần áo để tạo ra ảnh người mẫu mặc quần áo đó.

Project được triển khai với **2 phương án**:
- **Phương án 1**: On-Premise (chạy AI model trên server riêng)
- **Phương án 2**: External API (dùng service cloud như Replicate, Fal.ai, HeyBeauty)

## 🏗️ Kiến trúc Tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Web UI                      │
│  (HTML + CSS + JavaScript - Vanilla, no frameworks)        │
│           http://localhost:8000/app                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend Server                    │
│                  http://localhost:8000                      │
├─────────────────────────────────────────────────────────────┤
│  Endpoints:                                                 │
│  - POST /api/v1/tryon       Create task                    │
│  - GET  /api/v1/tryon/{id}  Check status                   │
│  - GET  /api/v1/tryon/{id}/result  Download                │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌──────────────────┐
│ PHƯƠNG ÁN 1     │         │ PHƯƠNG ÁN 2      │
│ On-Premise      │         │ External API     │
├─────────────────┤         ├──────────────────┤
│ - IDM-VTON      │         │ - Replicate      │
│ - OOTDiffusion  │         │ - Fal.ai         │
│ - OutfitAnyone  │         │ - HeyBeauty      │
│                 │         │                  │
│ Cần: GPU 8GB+   │         │ Cần: API Keys    │
│ Local Model     │         │ Cloud Service    │
└─────────────────┘         └──────────────────┘
```

## 📁 Cấu trúc Project

```
fashion-try-on/
│
├── backend/                          # Backend API với FastAPI
│   ├── main.py                       # FastAPI application chính
│   ├── config.py                     # Configuration cho 2 phương án
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Template cấu hình
│   │
│   ├── models/
│   │   └── schemas.py                # Pydantic models (Request/Response)
│   │
│   ├── services/
│   │   ├── on_premise_service.py     # PHƯƠNG ÁN 1: On-Premise AI
│   │   └── external_api_service.py   # PHƯƠNG ÁN 2: External APIs
│   │
│   ├── utils/
│   │   ├── database.py               # SQLite database
│   │   └── file_utils.py             # File upload/storage
│   │
│   ├── README.md                     # Backend documentation
│   ├── test_api.py                   # API testing script
│   ├── run_server.sh                 # Linux/Mac launcher
│   └── run_server.bat                # Windows launcher
│
├── frontend/                         # Frontend Web UI
│   ├── index.html                    # Main HTML page
│   ├── css/
│   │   └── style.css                 # All styles (1000+ lines)
│   ├── js/
│   │   └── app.js                    # JavaScript logic
│   └── README.md                     # Frontend documentation
│
├── uploads/                          # Uploaded images (auto-created)
├── results/                          # Result images (auto-created)
├── models/                           # AI model weights (for Phương án 1)
│
├── BACKEND_QUICKSTART.md             # Quick start guide cho backend
├── RUN_APP.md                        # Hướng dẫn chạy app đầy đủ
├── PROJECT_SUMMARY.md                # File này
└── README.md                         # Main README (từ OutfitAnyone)
```

## 🔧 Chi tiết Implementation

### Backend (FastAPI)

**File: `backend/main.py`**
- REST API với 6 endpoints chính
- Background task processing (async)
- CORS enabled
- Static files serving (uploads, results, frontend)
- Swagger UI documentation tự động

**File: `backend/config.py`**
- Settings cho cả 2 phương án
- Environment variables support (.env)
- Flexible configuration

**File: `backend/services/on_premise_service.py`** (Phương án 1)
- Load và chạy AI models local
- Support: IDM-VTON, OOTDiffusion, OutfitAnyone
- GPU/CPU mode
- Mock mode cho testing không cần model

**File: `backend/services/external_api_service.py`** (Phương án 2)
- Integration với 3 cloud providers:
  - Replicate: Dễ dùng, có free tier
  - Fal.ai: Fast inference
  - HeyBeauty: Professional API (code từ repo gốc)
- Retry logic
- Error handling

**File: `backend/utils/database.py`**
- SQLite database đơn giản
- Track tasks: pending → processing → completed/failed
- CRUD operations

**File: `backend/utils/file_utils.py`**
- File upload validation
- Image preprocessing
- File storage management

### Frontend (Vanilla JS)

**File: `frontend/index.html`**
- Modern, semantic HTML5
- Sections: Upload, Settings, Progress, Result
- Responsive grid layout
- Accessibility-friendly

**File: `frontend/css/style.css`**
- 1000+ lines of modern CSS
- CSS Variables cho theming
- Flexbox + Grid layout
- Animations (fade, slide, shimmer)
- Responsive breakpoints
- Dark gradient background

**File: `frontend/js/app.js`**
- Vanilla JavaScript (no jQuery, React, etc.)
- Features:
  - Drag & drop upload
  - FormData API for file upload
  - Fetch API for REST calls
  - Real-time polling for task status
  - Progress bar updates
  - Toast notifications
  - Error handling

## 🚀 Workflow

### User Journey:

1. **Upload** → User tải lên 2 ảnh (người + quần áo)
2. **Select** → Chọn provider (On-Premise hoặc External API)
3. **Configure** → (Optional) Advanced settings
4. **Submit** → Click "Bắt Đầu Thử Đồ"
5. **Processing** → Backend xử lý:
   - Tạo task trong database
   - Upload files
   - Call service (on-premise hoặc API)
   - Background processing
6. **Polling** → Frontend poll status mỗi 3s
7. **Complete** → Hiển thị kết quả
8. **Download** → User tải ảnh về

### Backend Processing Flow:

```
POST /api/v1/tryon
    ↓
Save uploaded images
    ↓
Create task in DB (status: pending)
    ↓
Start background task
    ↓
Update status: processing
    ↓
┌──────────────┐         ┌──────────────┐
│ Phương án 1  │   OR    │ Phương án 2  │
│ Local Model  │         │ External API │
└──────────────┘         └──────────────┘
    ↓                           ↓
Process image               Call API
    ↓                           ↓
Save result                 Download result
    ↓                           ↓
Update DB (status: completed/failed)
    ↓
Frontend polls → Gets result → Shows to user
```

## 💾 Database Schema

**Table: `tryon_tasks`**

```sql
CREATE TABLE tryon_tasks (
    id INTEGER PRIMARY KEY,
    task_id TEXT UNIQUE,              -- UUID
    model_image_path TEXT,            -- Path to uploaded model image
    garment_image_path TEXT,          -- Path to uploaded garment image
    result_image_path TEXT,           -- Path to result image
    provider TEXT,                    -- on_premise/replicate/fal/heybeauty
    category TEXT,                    -- upperbody/lowerbody/dress
    status TEXT,                      -- pending/processing/completed/failed
    error_message TEXT,               -- Error if failed
    denoise_steps INTEGER,            -- AI parameter
    seed INTEGER,                     -- Random seed
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    processing_time REAL              -- Seconds
);
```

## 🔌 API Endpoints

| Endpoint | Method | Mô tả | Request | Response |
|----------|--------|-------|---------|----------|
| `/` | GET | Health check | - | `{status, version, ...}` |
| `/app` | GET | Serve frontend | - | HTML page |
| `/api/v1/tryon` | POST | Create task | FormData: images + params | `{task_id, status, ...}` |
| `/api/v1/tryon/{id}` | GET | Get status | - | `{status, progress, result_url, ...}` |
| `/api/v1/tryon/{id}/result` | GET | Download result | - | Image file |
| `/api/v1/tasks` | GET | List tasks | Query: limit, offset | `{total, tasks[]}` |
| `/api/v1/tryon/{id}` | DELETE | Delete task | - | `{message}` |

## 🎨 UI/UX Features

### Upload Section
- Drag & drop support
- Visual preview
- File validation (type, size)
- Green checkmark when uploaded

### Provider Selection
- Card-based UI
- Visual icons (🖥️ ☁️ ⚡ 💄)
- "Khuyến nghị" badge cho Replicate
- Phương án badges (1 hoặc 2)

### Progress Tracking
- Real-time progress bar (0-100%)
- Status text updates
- Task ID display
- Processing details

### Result Display
- 3-column grid (Original | Garment | Result)
- Hover effects
- Download button
- Processing stats
- "Thử Lại" button

### Animations
- Fade in/down on load
- Smooth transitions
- Shimmer effect on progress bar
- Pulse animations

## 🔐 Security & Validation

### Backend
- File size limit: 10MB
- File type validation: JPG, PNG only
- Input sanitization
- Error handling
- CORS configured

### Frontend
- Client-side file validation
- Max file size check
- Image type check
- Error messages
- Timeout handling

## 📊 Performance

### Backend
- Async processing (FastAPI)
- Background tasks
- Database indexing
- File storage optimization

### Frontend
- Lazy loading
- Efficient DOM updates
- Debounced polling
- CSS animations (GPU-accelerated)

## 🧪 Testing

### Manual Testing

```bash
# 1. Start backend
python -m uvicorn backend.main:app --reload

# 2. Open frontend
http://localhost:8000/app

# 3. Test với ảnh mẫu
# 4. Kiểm tra cả 2 phương án
```

### API Testing

```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@person.jpg" \
  -F "garment_image=@shirt.jpg" \
  -F "provider=replicate"

# Using test script
python backend/test_api.py --model person.jpg --garment shirt.jpg
```

## 📈 Scalability

### Current (Single Server)
- 1 server handles all requests
- SQLite database
- Local file storage
- Good for: Development, small deployments

### Future (Production)
- Load balancer
- Multiple workers
- PostgreSQL database
- S3/Cloud storage
- Redis for caching
- Message queue (Celery, RabbitMQ)
- Kubernetes deployment

## 💰 Cost Analysis

### Phương án 1: On-Premise
- **Initial**: $2000-5000 (GPU server)
- **Monthly**: $50-200 (electricity, maintenance)
- **Per image**: ~$0.001 (electricity only)
- **Best for**: High volume (>10k images/month)

### Phương án 2: External API
- **Initial**: $0 (no hardware)
- **Monthly**: Pay-per-use
- **Per image**: $0.01-0.05
- **Best for**: Low-medium volume, MVP, testing

**Break-even**: ~100k-200k images

## 🎓 Learning Points

### Technologies Used
- **Backend**: Python, FastAPI, SQLite, Pydantic
- **Frontend**: HTML5, CSS3, Vanilla JS
- **AI**: Deep Learning models (IDM-VTON, etc.)
- **APIs**: REST, Replicate, Fal.ai
- **DevOps**: Git, Environment variables

### Design Patterns
- MVC architecture
- Service layer pattern
- Repository pattern (database)
- Factory pattern (service providers)
- Observer pattern (progress polling)

## 🚀 Deployment Options

### Development
```bash
python -m uvicorn backend.main:app --reload
```

### Production

**Option 1: Simple VPS**
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Option 2: Docker**
```dockerfile
FROM python:3.10
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

**Option 3: Cloud**
- Heroku: Easy deploy
- Railway: Modern platform
- AWS EC2: Full control
- Google Cloud Run: Serverless

## 📝 Documentation Files

- `README.md` - Main project overview (OutfitAnyone)
- `BACKEND_QUICKSTART.md` - Backend quick start (detailed)
- `RUN_APP.md` - Full app running guide
- `backend/README.md` - Backend API docs
- `frontend/README.md` - Frontend docs
- `PROJECT_SUMMARY.md` - This file (overview)

## ✅ Features Checklist

**Backend:**
- [x] FastAPI REST API
- [x] File upload handling
- [x] SQLite database
- [x] Background task processing
- [x] On-premise model support
- [x] External API integration (3 providers)
- [x] Error handling
- [x] CORS enabled
- [x] Swagger documentation

**Frontend:**
- [x] Modern UI/UX
- [x] Image upload (drag & drop)
- [x] Provider selection
- [x] Progress tracking
- [x] Result display
- [x] Download feature
- [x] Responsive design
- [x] Toast notifications
- [x] Advanced settings

**Documentation:**
- [x] Backend README
- [x] Frontend README
- [x] Quick start guide
- [x] Full running guide
- [x] Project summary
- [x] API documentation (Swagger)

## 🎯 Next Steps

### Short-term
- [ ] Add sample images
- [ ] Video tutorial
- [ ] Docker deployment
- [ ] More error handling

### Medium-term
- [ ] User authentication
- [ ] Task history UI
- [ ] Multiple garment selection
- [ ] Image cropping tool
- [ ] WebSocket for real-time updates

### Long-term
- [ ] Mobile app (React Native)
- [ ] Social sharing
- [ ] User accounts
- [ ] Payment integration
- [ ] Admin dashboard
- [ ] Analytics

## 🏆 Credits

- **Backend Framework**: FastAPI
- **AI Models**: IDM-VTON, OOTDiffusion, OutfitAnyone
- **API Providers**: Replicate, Fal.ai, HeyBeauty
- **UI Design**: Modern web design principles
- **Fonts**: Google Fonts (Inter)

---

**Made with ❤️ by Claude**

**Last Updated**: 2024-01-XX

**Version**: 1.0.0

**License**: MIT
