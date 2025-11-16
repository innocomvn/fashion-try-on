# Fashion Try-On Backend API

Backend API cho ứng dụng thử đồ ảo (virtual try-on) với **2 phương án triển khai**:
- **Phương án 1**: Sử dụng model on-premise (chạy trên server riêng)
- **Phương án 2**: Sử dụng API của các service bên ngoài

## 🌟 Tính năng

- ✅ Upload ảnh người mẫu và ảnh quần áo
- ✅ Tạo ảnh người mẫu mặc quần áo (virtual try-on)
- ✅ Hỗ trợ 2 phương án: On-premise và External API
- ✅ REST API với FastAPI
- ✅ Background task processing
- ✅ SQLite database để lưu task history
- ✅ File storage cho ảnh upload và kết quả
- ✅ Swagger UI documentation tự động

## 📋 Yêu cầu hệ thống

### Chung
- Python 3.8+
- 4GB RAM minimum
- 10GB disk space

### Phương án 1 (On-Premise)
- GPU: NVIDIA GPU với 8GB+ VRAM (khuyến nghị)
- CUDA 11.7+ và cuDNN
- 20GB+ disk space cho models

### Phương án 2 (External API)
- Không cần GPU
- Cần API key từ các service: Replicate, Fal.ai, hoặc HeyBeauty

## 🚀 Cài đặt

### 1. Clone repository

```bash
cd fashion-try-on
```

### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies

**Cho Phương án 2 (External API) - Nhẹ nhàng hơn:**
```bash
pip install -r backend/requirements.txt
```

**Cho Phương án 1 (On-Premise) - Cần thêm ML libraries:**
```bash
pip install -r backend/requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate opencv-python
```

### 4. Cấu hình

Tạo file `.env` từ template:

```bash
cp backend/.env.example backend/.env
```

Chỉnh sửa `.env` theo phương án bạn chọn:

#### Phương án 1: On-Premise
```bash
USE_ON_PREMISE=True
MODEL_TYPE="idm-vton"  # hoặc "ootdiffusion"
DEVICE="cuda"  # hoặc "cpu"
```

#### Phương án 2: External API

**Option A - Replicate (Khuyến nghị):**
```bash
USE_EXTERNAL_API=True
API_PROVIDER="replicate"
REPLICATE_API_TOKEN="your_token_here"
```
👉 Lấy token tại: https://replicate.com/account/api-tokens

**Option B - HeyBeauty:**
```bash
API_PROVIDER="heybeauty"
HEYBEAUTY_API_URL="your_api_url"
HEYBEAUTY_OPEN_ID="your_open_id"
HEYBEAUTY_API_KEY="your_api_key"
HEYBEAUTY_OSS_URL="your_oss_url"
```
👉 Lấy API keys tại: https://heybeauty.ai/keys

**Option C - Fal.ai:**
```bash
API_PROVIDER="fal"
FAL_API_KEY="your_fal_key"
```
👉 Lấy key tại: https://fal.ai/dashboard/keys

## 🎯 Chạy server

```bash
cd /home/user/fashion-try-on
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Hoặc:

```bash
python -m backend.main
```

Server sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

Khi server đang chạy, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### 1. Health Check
```bash
GET /
```

### 2. Tạo task thử đồ mới

**Phương án 1 - On-Premise:**
```bash
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@person.jpg" \
  -F "garment_image=@shirt.jpg" \
  -F "provider=on_premise" \
  -F "category=upperbody" \
  -F "denoise_steps=30"
```

**Phương án 2 - External API (Replicate):**
```bash
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@person.jpg" \
  -F "garment_image=@shirt.jpg" \
  -F "provider=replicate" \
  -F "category=upperbody"
```

Response:
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "pending",
  "message": "Task created successfully",
  "created_at": "2024-01-01T12:00:00"
}
```

### 3. Kiểm tra trạng thái task
```bash
GET /api/v1/tryon/{task_id}
```

Response:
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "completed",
  "progress": 100,
  "result_url": "/results/abc123-def456-ghi789.jpg",
  "processing_time": 15.5
}
```

### 4. Tải ảnh kết quả
```bash
GET /api/v1/tryon/{task_id}/result
```

### 5. Xem danh sách tasks
```bash
GET /api/v1/tasks?limit=10&offset=0
```

### 6. Xóa task
```bash
DELETE /api/v1/tryon/{task_id}
```

## 📊 So sánh 2 phương án

| Tiêu chí | Phương án 1: On-Premise | Phương án 2: External API |
|----------|-------------------------|---------------------------|
| **Chi phí** | Đầu tư ban đầu cao (GPU) | Pay-per-use, linh hoạt |
| **Hiệu năng** | Nhanh nếu có GPU mạnh | Phụ thuộc API provider |
| **Bảo mật** | Dữ liệu ở local, an toàn hơn | Dữ liệu gửi lên cloud |
| **Bảo trì** | Cần maintain model & infra | Provider lo việc maintain |
| **Khả năng mở rộng** | Giới hạn bởi hardware | Dễ scale theo nhu cầu |
| **Thời gian xử lý** | 10-30 giây (GPU) | 20-60 giây (tùy provider) |
| **Yêu cầu kỹ thuật** | Cao (ML, GPU, DevOps) | Thấp (chỉ cần API key) |

## 🏗️ Kiến trúc

```
backend/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   ├── on_premise_service.py     # PHƯƠNG ÁN 1
│   └── external_api_service.py   # PHƯƠNG ÁN 2
└── utils/
    ├── database.py        # SQLite utilities
    └── file_utils.py      # File handling
```

## 🎨 Models hỗ trợ

### Phương án 1 - On-Premise Models
1. **IDM-VTON** (Khuyến nghị)
   - Paper: https://arxiv.org/abs/2403.05139
   - GitHub: https://github.com/yisol/IDM-VTON
   - Chất lượng: ⭐⭐⭐⭐⭐

2. **OOTDiffusion**
   - Paper: https://arxiv.org/abs/2403.01779
   - GitHub: https://github.com/levihsu/OOTDiffusion
   - Chất lượng: ⭐⭐⭐⭐

3. **OutfitAnyone**
   - Repository hiện tại
   - Chất lượng: ⭐⭐⭐⭐⭐

### Phương án 2 - External APIs
1. **Replicate** (Khuyến nghị cho bắt đầu)
   - Dễ setup, có free tier
   - Model: IDM-VTON
   - Pricing: ~$0.01-0.05/image

2. **HeyBeauty**
   - Service chuyên nghiệp
   - Có API riêng
   - Pricing: Contact

3. **Fal.ai**
   - Fast inference
   - Model: IDM-VTON
   - Pricing: ~$0.02/image

## 🧪 Testing

```bash
# Test với curl
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@test_person.jpg" \
  -F "garment_image=@test_garment.jpg" \
  -F "provider=replicate"

# Hoặc dùng Python
python test_api.py
```

## 🔧 Troubleshooting

### Lỗi: "CUDA out of memory"
- Giảm `denoise_steps` xuống 20
- Resize ảnh nhỏ hơn
- Dùng CPU mode: `DEVICE="cpu"`

### Lỗi: "API token not configured"
- Kiểm tra file `.env` đã set API key chưa
- Restart server sau khi thay đổi `.env`

### Lỗi: "Model not found"
- Download model weights về folder `models/`
- Xem hướng dẫn setup model trong docs của từng model

## 📈 Roadmap

- [ ] Thêm model support: Stable Diffusion XL
- [ ] WebSocket cho real-time progress updates
- [ ] Admin dashboard
- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching layer với Redis
- [ ] Docker deployment
- [ ] Kubernetes manifests

## 📝 License

MIT License - Xem file LICENSE

## 👥 Authors

- Backend API: Claude
- Based on: OutfitAnyone project

## 🙏 Acknowledgments

- OutfitAnyone team
- IDM-VTON authors
- OOTDiffusion authors
- FastAPI framework
- HuggingFace community

---

**Happy Coding! 🚀**

Nếu có vấn đề gì, tạo issue trên GitHub hoặc liên hệ team.
