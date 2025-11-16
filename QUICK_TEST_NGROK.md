# 🚀 Quick Test với Ngrok - 5 phút setup!

## Cách nhanh nhất để test app từ Internet

### ⚡ Super Quick (3 lệnh)

```bash
# 1. Cài ngrok
sudo snap install ngrok

# 2. Setup token (lấy từ https://dashboard.ngrok.com/get-started/your-authtoken)
ngrok config add-authtoken YOUR_AUTH_TOKEN

# 3. Chạy!
./start_with_ngrok.sh
```

**🎉 Done! App đã expose ra Internet!**

---

## 📱 Chi tiết từng bước

### Bước 1: Cài Ngrok (1 phút)

**Linux:**
```bash
sudo snap install ngrok
```

**Mac:**
```bash
brew install ngrok/ngrok/ngrok
```

**Windows:**
```powershell
choco install ngrok
```

### Bước 2: Đăng ký FREE account (2 phút)

1. Vào: https://dashboard.ngrok.com/signup
2. Đăng ký (có thể dùng Google/GitHub)
3. Copy authtoken từ: https://dashboard.ngrok.com/get-started/your-authtoken

### Bước 3: Setup token (10 giây)

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### Bước 4: Chạy script (1 lệnh)

```bash
# Linux/Mac
./start_with_ngrok.sh

# Windows
start_with_ngrok.bat
```

**Output:**
```
╔══════════════════════════════════════════════════════════╗
║     Fashion Try-On - Internet Access with Ngrok         ║
╚══════════════════════════════════════════════════════════╝

🔄 Kích hoạt virtual environment...
✅ Dependencies đã được cài đặt
🚀 Đang khởi động FastAPI backend...
✅ Backend đang chạy (PID: 12345)
🌐 Đang khởi động Ngrok...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Services đã khởi động thành công!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 Public URL (Ngrok):
https://abc123xyz.ngrok-free.app/app

👉 Share link này để test từ bất kỳ đâu!

📊 Local URLs:
   Frontend: http://localhost:8000/app
   API Docs: http://localhost:8000/docs
   Ngrok Dashboard: http://localhost:4040

🛑 Nhấn Ctrl+C để dừng tất cả services
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 Ngrok URL có dạng:

```
https://random-string.ngrok-free.app
```

**VD:**
- `https://abc123xyz.ngrok-free.app/app` ← Frontend
- `https://abc123xyz.ngrok-free.app/docs` ← API Docs
- `https://abc123xyz.ngrok-free.app/api/v1/tryon` ← API Endpoint

---

## 📱 Test từ điện thoại

1. **Lấy URL** từ output của script
2. **Mở trình duyệt** trên điện thoại
3. **Truy cập** URL đó (VD: `https://abc123xyz.ngrok-free.app/app`)
4. **Upload ảnh** và test!

---

## 🌐 Share với người khác

**Message mẫu:**

```
Hãy test app thử đồ ảo của mình nhé! 👗

👉 Link: https://abc123xyz.ngrok-free.app/app

Cách dùng:
1. Mở link
2. Upload ảnh người mẫu (ảnh của bạn hoặc bất kỳ)
3. Upload ảnh quần áo
4. Chọn "Replicate" (provider)
5. Click "Bắt Đầu Thử Đồ"
6. Đợi 30 giây
7. Xem kết quả! 🎉

Ảnh mẫu tốt:
- Người: đứng thẳng, nền trắng
- Quần áo: nền trắng, phẳng
```

---

## 📊 Ngrok Dashboard

Mở: **http://localhost:4040**

Xem được:
- 📈 Số requests real-time
- 🔍 Chi tiết từng request
- ⏱️ Response time
- 📝 Request/response body
- 🎯 Status codes

---

## 🛑 Dừng services

**Cách 1:** Nhấn `Ctrl+C` trong terminal đang chạy script

**Cách 2:** Đóng terminal

**Cách 3:** Kill processes:
```bash
pkill -f uvicorn
pkill -f ngrok
```

---

## ⚙️ Chạy manual (không dùng script)

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Ngrok:**
```bash
ngrok http 8000
```

---

## 💡 Tips & Tricks

### 1. URL thay đổi mỗi lần restart
Free plan của ngrok tạo random URL mỗi lần. Muốn URL cố định cần upgrade.

### 2. Xem Ngrok logs
```bash
tail -f logs/ngrok.log
```

### 3. Xem Backend logs
```bash
tail -f logs/backend.log
```

### 4. Test nhiều devices cùng lúc
- Điện thoại của bạn
- Điện thoại bạn bè
- Máy tính khác
- Từ mạng khác (4G, cafe, etc.)

### 5. QR Code để scan
Nếu có `qrencode`:
```bash
qrencode -t ANSI "https://your-url.ngrok-free.app/app"
```

---

## 🐛 Troubleshooting

### "ngrok not found"
```bash
# Cài lại
sudo snap install ngrok

# Hoặc
brew install ngrok/ngrok/ngrok
```

### "Authtoken not found"
```bash
ngrok config add-authtoken YOUR_TOKEN
```

### Backend không chạy
```bash
# Check logs
cat logs/backend.log

# Test manual
python -m uvicorn backend.main:app
```

### CORS errors trên ngrok URL
Backend đã config CORS cho phép tất cả origins (`*`), nên không vấn đề!

### Ngrok URL không hiển thị
Mở: http://localhost:4040 để xem URL

---

## 🔒 Bảo mật

⚠️ **Lưu ý:**
- Ngrok URL là **PUBLIC** - ai có link đều vào được
- Chỉ share với người cần test
- Tắt ngrok khi không dùng
- Không để lộ API keys trong code

---

## 📈 Upgrade Ngrok (Optional)

**Free Plan:**
- ✅ Random URLs
- ✅ HTTPS
- ✅ 40 connections/min
- ❌ Custom domains

**Paid ($8/month):**
- ✅ Static URLs (không đổi)
- ✅ Custom domains
- ✅ Unlimited connections
- ✅ Multiple tunnels

👉 Free plan đủ dùng để test/demo!

---

## 🎬 Video Demo

Coming soon: Video hướng dẫn setup ngrok!

---

## 📚 Đọc thêm

- Full guide: `NGROK_SETUP.md`
- Ngrok docs: https://ngrok.com/docs
- Dashboard: https://dashboard.ngrok.com

---

**Chúc test vui vẻ! 🚀**

**Thắc mắc?** Đọc `NGROK_SETUP.md` hoặc Google "ngrok tutorial"
