# 🚀 Hướng dẫn chạy Fashion Try-On App

## Cách nhanh nhất - 3 bước đơn giản!

### Bước 1: Cài đặt dependencies

```bash
cd fashion-try-on

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Cài packages
pip install -r backend/requirements.txt
```

### Bước 2: Cấu hình API (Chọn 1 trong 2)

#### Option A: Dùng External API - Replicate (Khuyến nghị cho test)

```bash
# Copy file cấu hình
cp backend/.env.example backend/.env

# Edit backend/.env với text editor, set:
USE_EXTERNAL_API=True
API_PROVIDER="replicate"
REPLICATE_API_TOKEN="r8_xxxxx"  # Lấy token miễn phí tại https://replicate.com
```

**Lấy Replicate API Token:**
1. Đăng ký tại: https://replicate.com/
2. Vào: https://replicate.com/account/api-tokens
3. Create token
4. Copy và paste vào `.env`

#### Option B: Dùng On-Premise (Cần GPU)

```bash
# Edit backend/.env:
USE_ON_PREMISE=True
MODEL_TYPE="idm-vton"
DEVICE="cuda"  # hoặc "cpu" nếu không có GPU
```

### Bước 3: Chạy app!

```bash
# Chạy backend server
python -m uvicorn backend.main:app --reload

# Server sẽ chạy tại: http://localhost:8000
```

### Bước 4: Mở frontend

Mở trình duyệt và truy cập:

```
http://localhost:8000/app
```

🎉 **Done! Bắt đầu thử đồ ngay!**

---

## 📖 Hướng dẫn chi tiết

### Test với Phương án 2 - External API

1. **Upload ảnh người mẫu**:
   - Click vào khung "Ảnh Người Mẫu"
   - Chọn ảnh người (toàn thân, nền đơn giản tốt nhất)
   - Hoặc kéo thả ảnh vào khung

2. **Upload ảnh quần áo**:
   - Click vào khung "Ảnh Quần Áo"
   - Chọn ảnh áo/váy/quần (nền trắng tốt nhất)

3. **Chọn provider**:
   - Click vào card **Replicate** (có badge "Khuyến nghị")
   - Hoặc chọn Fal.ai / HeyBeauty nếu đã có API key

4. **Cài đặt nâng cao** (Optional):
   - Click "Cài đặt nâng cao"
   - Chọn loại quần áo: Upperbody (áo), Lowerbody (quần), Dress (váy)
   - Điều chỉnh Denoise Steps (20-40 tốt)

5. **Chạy**:
   - Click nút **"Bắt Đầu Thử Đồ"**
   - Đợi 20-40 giây (progress bar sẽ hiển thị tiến trình)
   - Xem kết quả!

6. **Download kết quả**:
   - Click nút **"Tải Xuống"** để lưu ảnh
   - Hoặc click **"Thử Lại"** để làm lại với ảnh khác

### Test với Phương án 1 - On-Premise

1. **Chuẩn bị model** (lần đầu tiên):
   ```bash
   # Tạo thư mục models
   mkdir -p models/idm-vton

   # Download model weights (xem hướng dẫn trong backend/README.md)
   # Hoặc để mock mode để test UI (không cần download)
   ```

2. **Chạy tương tự như trên**, nhưng chọn provider **On-Premise**

3. **Thời gian xử lý**:
   - Với GPU: 10-30 giây
   - Với CPU: 60-120 giây (chậm hơn)

---

## 📊 So sánh 2 phương án

| Tiêu chí | Phương án 1: On-Premise | Phương án 2: External API |
|----------|-------------------------|---------------------------|
| **Setup** | Phức tạp (cần GPU & models) | Dễ (5 phút) |
| **Chi phí** | Miễn phí (sau khi đầu tư) | ~$0.01-0.05/ảnh |
| **Tốc độ** | 10-30s (GPU) | 20-40s |
| **Chất lượng** | Cao (tùy model) | Cao |
| **Test nhanh** | ❌ Khó | ✅ Dễ |

**👉 Khuyến nghị**: Bắt đầu với **Phương án 2 (Replicate)** để test nhanh, sau đó chuyển sang Phương án 1 nếu cần.

---

## 🎯 Ví dụ test

### Ảnh test tốt:

**Ảnh người mẫu:**
- Toàn thân, đứng thẳng
- Nền đơn giản, sáng
- Mặc quần áo bình thường
- Nhìn thẳng camera

**Ảnh quần áo:**
- Nền trắng hoặc trong suốt
- Phẳng, không nhăn
- Rõ nét, chi tiết
- Chụp toàn bộ sản phẩm

### Ảnh test không tốt:

- Người quay lưng, nghiêng nhiều
- Nền quá rối, nhiều người
- Ảnh mờ, tối
- Quần áo bị che khuất

---

## 🔧 Troubleshooting

### Backend không chạy?

```bash
# Kiểm tra Python version (cần 3.8+)
python --version

# Kiểm tra dependencies
pip list | grep fastapi

# Reinstall nếu cần
pip install --upgrade -r backend/requirements.txt
```

### Frontend không load?

```bash
# Kiểm tra backend có chạy không
curl http://localhost:8000/

# Nếu OK, mở: http://localhost:8000/app
```

### API token không hoạt động?

- Kiểm tra token có đúng không
- Restart backend sau khi sửa `.env`
- Kiểm tra credits còn không (Replicate free trial: $5)

### "CUDA out of memory"?

```bash
# Trong .env, đổi sang CPU:
DEVICE="cpu"

# Hoặc giảm denoise steps:
IDM_VTON_DENOISE_STEPS=20
```

---

## 📚 Tài liệu thêm

- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`
- **Quick Start**: `BACKEND_QUICKSTART.md`

---

## 🎬 Video Demo (Coming soon)

- YouTube tutorial
- Setup guide
- Example results

---

## 💡 Tips

1. **Chất lượng ảnh**: Ảnh đầu vào tốt → kết quả tốt
2. **Provider**: Thử nhiều provider để so sánh
3. **Settings**: Denoise steps càng cao càng chi tiết (nhưng chậm hơn)
4. **Cache**: Kết quả được lưu trong database, có thể xem lại

---

## 🆘 Cần giúp đỡ?

- **GitHub Issues**: https://github.com/innocomvn/fashion-try-on/issues
- **Email**: jiangxiaoguo@heybeautify.online
- **Docs**: Đọc README files trong từng folder

---

**Happy Virtual Try-On! 🎉👗**

Made with ❤️ using FastAPI, AI, and lots of coffee ☕
