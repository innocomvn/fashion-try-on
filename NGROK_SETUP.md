# 🌐 Ngrok Setup - Expose App to Internet

Hướng dẫn sử dụng Ngrok để test app từ Internet (điện thoại, máy khác, hoặc share với người khác).

## 🚀 Quick Start (3 bước)

### Bước 1: Cài đặt Ngrok

#### Linux/Mac:
```bash
# Download và cài đặt
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Hoặc dùng snap
sudo snap install ngrok
```

#### Windows:
```powershell
# Dùng Chocolatey
choco install ngrok

# Hoặc download từ: https://ngrok.com/download
# Giải nén và thêm vào PATH
```

#### Mac (Homebrew):
```bash
brew install ngrok/ngrok/ngrok
```

### Bước 2: Đăng ký và lấy token (FREE)

1. Đăng ký tại: https://dashboard.ngrok.com/signup
2. Vào: https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy authtoken

### Bước 3: Setup token

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

## 📱 Chạy Ngrok

### Cách 1: Manual (2 terminals)

**Terminal 1 - Chạy Backend:**
```bash
cd fashion-try-on
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Chạy Ngrok:**
```bash
ngrok http 8000
```

**Output:**
```
ngrok

Session Status                online
Account                       your-email@gmail.com (Plan: Free)
Version                       3.x.x
Region                        Asia Pacific (ap)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

🎉 **Link public**: `https://abc123.ngrok-free.app`

### Cách 2: Dùng Script Tự Động

Tôi đã tạo script `start_with_ngrok.sh` - chỉ cần chạy 1 lệnh!

```bash
chmod +x start_with_ngrok.sh
./start_with_ngrok.sh
```

## 🌍 Truy cập từ Internet

### Từ máy tính/điện thoại bất kỳ:

1. Mở trình duyệt
2. Truy cập: `https://your-ngrok-url.ngrok-free.app/app`
3. Upload ảnh và test!

### Share với người khác:

```
Hey! Test app thử đồ của mình nè:
👉 https://abc123.ngrok-free.app/app

- Upload ảnh người mẫu
- Upload ảnh quần áo
- Chọn provider "Replicate"
- Click "Bắt Đầu Thử Đồ"
- Đợi 30s để xem kết quả!
```

## 📊 Ngrok Dashboard

Mở: http://127.0.0.1:4040

**Features:**
- 📈 Real-time requests
- 🔍 Inspect & replay requests
- 📝 Request/response details
- 🎯 Status codes
- ⏱️ Response times

## ⚙️ Advanced Options

### Custom subdomain (Paid plan)
```bash
ngrok http 8000 --subdomain=fashion-tryon
# URL: https://fashion-tryon.ngrok.app
```

### Basic auth (bảo mật)
```bash
ngrok http 8000 --basic-auth="username:password"
```

### Multiple regions
```bash
# Auto-select best region
ngrok http 8000

# Force specific region
ngrok http 8000 --region=us  # US
ngrok http 8000 --region=eu  # Europe
ngrok http 8000 --region=ap  # Asia Pacific
ngrok http 8000 --region=au  # Australia
ngrok http 8000 --region=sa  # South America
ngrok http 8000 --region=jp  # Japan
ngrok http 8000 --region=in  # India
```

### Config file
**File: `~/.ngrok2/ngrok.yml`**
```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN

tunnels:
  fashion-tryon:
    proto: http
    addr: 8000
    inspect: true
    bind_tls: true
```

**Run:**
```bash
ngrok start fashion-tryon
```

## 🔒 Security Notes

### ⚠️ Lưu ý quan trọng:

1. **Ngrok URL là PUBLIC** - ai có link đều truy cập được
2. **Free plan**: URL thay đổi mỗi lần restart
3. **Giới hạn**: Free plan có giới hạn connections/phút
4. **Không dùng cho production** - chỉ để test/demo

### 🛡️ Bảo mật khi dùng Ngrok:

```bash
# 1. Chỉ share link với người cần test
# 2. Tắt ngrok khi không dùng (Ctrl+C)
# 3. Không commit authtoken vào git
# 4. Dùng basic auth nếu cần:
ngrok http 8000 --basic-auth="user:pass"
```

## 📱 Test từ điện thoại

### Cách 1: Scan QR code (Terminal)
```bash
# Install qrcode
pip install qrcode[pil]

# Generate QR
python -c "import qrcode; qrcode.make('https://your-url.ngrok-free.app/app').save('qr.png')"

# Show in terminal
qr "https://your-url.ngrok-free.app/app"
```

### Cách 2: SMS/Share link
- Copy ngrok URL
- Gửi qua SMS/WhatsApp/Telegram
- Mở trên điện thoại
- Test ngay!

## 🎯 Use Cases

### 1. Demo cho khách hàng
```
"Anh/chị mở link này để xem demo nhé:
https://abc123.ngrok-free.app/app"
```

### 2. Test trên nhiều thiết bị
- iPhone, Android, iPad
- Máy tính bạn bè
- Từ mạng khác (4G, WiFi khác)

### 3. Webhook testing
- Test API callbacks từ Replicate
- Test external services

### 4. Share với team
```
Team meeting: "Mọi người vào link này test giùm mình"
```

## 🐛 Troubleshooting

### Ngrok không connect?
```bash
# Check ngrok version
ngrok version

# Re-add authtoken
ngrok config add-authtoken YOUR_TOKEN

# Check config
ngrok config check
```

### CORS errors?
Backend đã config CORS cho `*` nên không vấn đề!

### SSL/HTTPS errors?
Ngrok tự động cung cấp HTTPS (miễn phí!)

### Slow connection?
```bash
# Try different region
ngrok http 8000 --region=ap  # Asia Pacific gần VN nhất
```

### "ERR_NGROK_6024" - Account limit
Free plan có giới hạn:
- 1 process/account
- 40 connections/minute
- Cần upgrade để dùng nhiều hơn

## 💰 Ngrok Pricing

### Free Plan (Đủ dùng để test)
- ✅ HTTPS
- ✅ Random URLs
- ✅ 40 connections/min
- ✅ Basic features
- ❌ Custom domains
- ❌ Static URLs

### Paid Plans ($8-49/month)
- ✅ Custom domains
- ✅ Static URLs
- ✅ More connections
- ✅ Multiple tunnels
- ✅ Reserved domains

**👉 Free plan là đủ cho test/demo!**

## 🔄 Alternatives to Ngrok

Nếu cần:
1. **Cloudflare Tunnel** - Free, unlimited
2. **LocalTunnel** - Free, open source
3. **Serveo** - Free SSH tunneling
4. **Telebit** - Free alternative

## 📚 Resources

- Ngrok Docs: https://ngrok.com/docs
- Dashboard: https://dashboard.ngrok.com
- Download: https://ngrok.com/download
- Pricing: https://ngrok.com/pricing

---

## 🎬 Example Session

```bash
# Terminal 1
$ python -m uvicorn backend.main:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000

# Terminal 2
$ ngrok http 8000

ngrok
Session Status                online
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000

# 🎉 Share this URL!
# https://abc123.ngrok-free.app/app
```

---

**Enjoy testing from anywhere! 🌍**

**Tips**:
- Tắt ngrok khi không dùng (Ctrl+C)
- URL mới mỗi lần chạy (free plan)
- Dùng script `start_with_ngrok.sh` để chạy tự động!
