# 🚀 Fashion Try-On Backend - Quick Start Guide

## Hướng dẫn khởi động nhanh cho backend thử đồ ảo

---

## 📌 Chọn phương án phù hợp với bạn

### 🏢 Phương án 1: On-Premise (Tự host model)

**Phù hợp khi:**
- Bạn có GPU mạnh (NVIDIA 8GB+ VRAM)
- Cần xử lý dữ liệu nhạy cảm (không muốn gửi ảnh lên cloud)
- Cần tốc độ xử lý nhanh và kiểm soát hoàn toàn
- Có đội ngũ kỹ thuật để maintain

**Ưu điểm:**
- ✅ Bảo mật cao
- ✅ Không phụ thuộc bên thứ 3
- ✅ Không tốn phí API call
- ✅ Tùy chỉnh model theo nhu cầu

**Nhược điểm:**
- ❌ Chi phí đầu tư hardware cao
- ❌ Cần kiến thức ML/AI
- ❌ Khó scale nhanh

---

### ☁️ Phương án 2: External API (Dùng service bên ngoài)

**Phù hợp khi:**
- Bạn chưa có GPU hoặc đang test
- Cần deploy nhanh, không muốn lo về infrastructure
- Sản phẩm MVP/prototype
- Budget linh hoạt theo usage

**Ưu điểm:**
- ✅ Setup nhanh trong 5 phút
- ✅ Không cần GPU
- ✅ Scale tự động
- ✅ Provider lo maintain model

**Nhược điểm:**
- ❌ Chi phí theo usage (~$0.01-0.05/ảnh)
- ❌ Phụ thuộc vào provider
- ❌ Dữ liệu gửi lên cloud

---

## ⚡ Setup siêu nhanh - 5 phút

### Bước 1: Clone và cài đặt

```bash
cd fashion-try-on

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài dependencies cơ bản
pip install -r backend/requirements.txt
```

### Bước 2: Cấu hình

```bash
# Copy file cấu hình
cp backend/.env.example backend/.env
```

**Chọn phương án của bạn:**

#### Option A: External API (Khuyến nghị cho bắt đầu)

Mở `backend/.env` và set:

```bash
USE_EXTERNAL_API=True
API_PROVIDER="replicate"

# Lấy token miễn phí tại: https://replicate.com/account/api-tokens
REPLICATE_API_TOKEN="r8_xxxxxxxxxxxxxxxxxxxxx"
```

#### Option B: On-Premise

```bash
USE_ON_PREMISE=True
MODEL_TYPE="idm-vton"
DEVICE="cpu"  # Hoặc "cuda" nếu có GPU
```

### Bước 3: Chạy server

```bash
# Cách 1: Dùng script launcher
./backend/run_server.sh  # Linux/Mac
# hoặc: backend\run_server.bat  # Windows

# Cách 2: Chạy trực tiếp
python -m uvicorn backend.main:app --reload
```

Server chạy tại: **http://localhost:8000**

### Bước 4: Test API

Mở trình duyệt và vào:
- **Swagger UI**: http://localhost:8000/docs

Hoặc test bằng curl:

```bash
curl -X POST "http://localhost:8000/api/v1/tryon" \
  -F "model_image=@test_person.jpg" \
  -F "garment_image=@test_shirt.jpg" \
  -F "provider=replicate"
```

---

## 📊 Ví dụ sử dụng

### Python Client

```python
import requests

# Upload và tạo task
files = {
    'model_image': open('person.jpg', 'rb'),
    'garment_image': open('shirt.jpg', 'rb')
}
data = {
    'provider': 'replicate',  # hoặc 'on_premise'
    'category': 'upperbody'
}

response = requests.post(
    'http://localhost:8000/api/v1/tryon',
    files=files,
    data=data
)

task_id = response.json()['task_id']
print(f"Task created: {task_id}")

# Kiểm tra trạng thái
import time
while True:
    status = requests.get(f'http://localhost:8000/api/v1/tryon/{task_id}')
    data = status.json()

    if data['status'] == 'completed':
        print(f"Done! Result: {data['result_url']}")
        break
    elif data['status'] == 'failed':
        print(f"Failed: {data['error_message']}")
        break

    print(f"Progress: {data['progress']}%")
    time.sleep(3)

# Tải ảnh kết quả
result = requests.get(f'http://localhost:8000/api/v1/tryon/{task_id}/result')
with open('result.jpg', 'wb') as f:
    f.write(result.content)
```

### JavaScript/TypeScript Client

```javascript
// Tạo task
const formData = new FormData();
formData.append('model_image', modelImageFile);
formData.append('garment_image', garmentImageFile);
formData.append('provider', 'replicate');

const response = await fetch('http://localhost:8000/api/v1/tryon', {
  method: 'POST',
  body: formData
});

const { task_id } = await response.json();

// Poll status
const checkStatus = async () => {
  const res = await fetch(`http://localhost:8000/api/v1/tryon/${task_id}`);
  const data = await res.json();

  if (data.status === 'completed') {
    console.log('Done!', data.result_url);
    return data.result_url;
  }

  setTimeout(checkStatus, 3000);
};

checkStatus();
```

---

## 🔑 Lấy API Keys

### Replicate (Khuyến nghị)
1. Đăng ký tại: https://replicate.com/
2. Vào: https://replicate.com/account/api-tokens
3. Tạo token mới
4. Copy và paste vào `.env`

**Free tier**: $5 credit, ~200-500 images

### HeyBeauty
1. Đăng ký tại: https://heybeauty.ai/
2. Vào: https://heybeauty.ai/keys
3. Lấy API credentials
4. Set trong `.env`:
   ```
   HEYBEAUTY_API_URL=...
   HEYBEAUTY_OPEN_ID=...
   HEYBEAUTY_API_KEY=...
   HEYBEAUTY_OSS_URL=...
   ```

### Fal.ai
1. Đăng ký: https://fal.ai/
2. Dashboard: https://fal.ai/dashboard/keys
3. Tạo API key
4. Set `FAL_API_KEY` trong `.env`

---

## 🎯 API Endpoints Chính

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Health check |
| `/api/v1/tryon` | POST | Tạo task try-on mới |
| `/api/v1/tryon/{task_id}` | GET | Kiểm tra trạng thái task |
| `/api/v1/tryon/{task_id}/result` | GET | Tải ảnh kết quả |
| `/api/v1/tasks` | GET | Xem tất cả tasks |
| `/api/v1/tryon/{task_id}` | DELETE | Xóa task |

---

## 🐛 Troubleshooting

### Lỗi: "Cannot connect to API"
```bash
# Kiểm tra server có chạy không
curl http://localhost:8000/

# Kiểm tra port có bị chiếm không
lsof -i :8000
```

### Lỗi: "API token not configured"
```bash
# Kiểm tra .env file
cat backend/.env | grep API

# Restart server sau khi sửa .env
```

### Lỗi: "CUDA out of memory" (On-Premise)
Trong `.env`:
```bash
DEVICE="cpu"  # Chuyển sang CPU
IDM_VTON_DENOISE_STEPS=20  # Giảm steps
```

---

## 📚 Tài liệu đầy đủ

- **API Docs**: http://localhost:8000/docs
- **Full README**: [backend/README.md](backend/README.md)
- **Architecture**: Xem source code comments

---

## 💡 Tips & Best Practices

1. **Chất lượng ảnh đầu vào**
   - Ảnh người: Rõ mặt, toàn thân, nền đơn giản
   - Ảnh quần áo: Nền trắng, phẳng, rõ nét
   - Độ phân giải: 512x512 đến 1024x1024

2. **Performance**
   - Replicate: ~20-40s/image
   - On-premise GPU: ~10-20s/image
   - On-premise CPU: ~60-120s/image

3. **Cost Optimization**
   - Cache kết quả cho cùng input
   - Batch processing cho nhiều ảnh
   - Sử dụng queue system cho high traffic

4. **Production Ready**
   - Thêm authentication
   - Rate limiting
   - Error monitoring (Sentry)
   - Use PostgreSQL thay SQLite
   - Deploy với Docker

---

## 🚢 Deployment

### Docker (Coming soon)
```bash
docker build -t fashion-tryon-backend .
docker run -p 8000:8000 fashion-tryon-backend
```

### Cloud Platforms
- **Heroku**: Easy deploy, có free tier
- **Railway**: Modern, CI/CD tốt
- **AWS EC2**: Full control, cần GPU instance cho on-premise
- **Google Cloud Run**: Serverless, scale tốt

---

## ❓ FAQ

**Q: Phương án nào tốt hơn?**
A: Phương án 2 (External API) tốt cho bắt đầu. Khi scale lớn, chuyển sang on-premise.

**Q: Chi phí External API là bao nhiêu?**
A: ~$0.01-0.05/ảnh. VD: 1000 ảnh/tháng = ~$10-50.

**Q: Cần GPU gì cho on-premise?**
A: NVIDIA RTX 3060 (12GB) trở lên. RTX 4090 (24GB) là optimal.

**Q: Có thể dùng cả 2 phương án?**
A: Có! Set `USE_ON_PREMISE=True` và `USE_EXTERNAL_API=True`, chọn provider khi call API.

**Q: Làm sao để improve chất lượng kết quả?**
A: Tăng `denoise_steps` (30-50), dùng ảnh input chất lượng cao, thử các provider khác nhau.

---

**Happy Coding! 🎉**

Nếu có vấn đề, tạo issue hoặc liên hệ team support.
