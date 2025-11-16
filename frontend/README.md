# Fashion Try-On Frontend

Frontend đơn giản và đẹp mắt cho app thử đồ ảo với AI.

## ✨ Tính năng

- 📸 **Upload ảnh dễ dàng**: Drag & drop hoặc click để chọn
- 🎨 **Giao diện đẹp**: Modern UI với gradients và animations
- ⚙️ **Chọn phương án**: Test cả 2 phương án (On-Premise và External API)
- 📊 **Real-time progress**: Theo dõi tiến trình xử lý
- 🎉 **Hiển thị kết quả**: Xem trước ảnh gốc, quần áo và kết quả
- 📥 **Download**: Tải kết quả về máy
- 📱 **Responsive**: Hoạt động tốt trên mobile và desktop

## 🚀 Cách sử dụng

### Option 1: Chạy với Backend (Khuyến nghị)

```bash
# Từ thư mục gốc của project
cd fashion-try-on

# Chạy backend (sẽ tự động serve frontend)
python -m uvicorn backend.main:app --reload

# Mở trình duyệt và truy cập:
# http://localhost:8000/app
```

### Option 2: Chạy độc lập (Development)

```bash
# Cài http-server (nếu chưa có)
npm install -g http-server

# Từ thư mục frontend
cd frontend
http-server -p 3000

# Mở: http://localhost:3000
```

## 📋 Hướng dẫn test

### Test Phương án 2 - External API (Replicate)

1. **Cấu hình Backend**:
   ```bash
   # Mở backend/.env
   USE_EXTERNAL_API=True
   API_PROVIDER="replicate"
   REPLICATE_API_TOKEN="your_token_here"
   ```

2. **Chạy backend**:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

3. **Mở frontend**: http://localhost:8000/app

4. **Test**:
   - Upload ảnh người mẫu (bất kỳ ảnh người nào)
   - Upload ảnh quần áo (ảnh áo/váy/quần)
   - Chọn provider: **Replicate** (hoặc Fal.ai, HeyBeauty)
   - Click "Bắt Đầu Thử Đồ"
   - Đợi 20-40 giây
   - Xem kết quả!

### Test Phương án 1 - On-Premise

1. **Cấu hình Backend**:
   ```bash
   # Mở backend/.env
   USE_ON_PREMISE=True
   MODEL_TYPE="idm-vton"
   DEVICE="cuda"  # hoặc "cpu"
   ```

2. **Download models** (cần thiết):
   ```bash
   # Tùy model bạn chọn, download weights về models/
   # Xem hướng dẫn trong backend/README.md
   ```

3. **Chạy backend**:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

4. **Test**:
   - Upload ảnh
   - Chọn provider: **On-Premise**
   - Click "Bắt Đầu Thử Đồ"
   - Đợi 10-30 giây (tùy GPU/CPU)
   - Xem kết quả!

## 🎨 Giao diện

### Các phần chính:

1. **Upload Section**: Upload 2 ảnh (người + quần áo)
2. **Settings Section**:
   - Chọn provider (On-Premise, Replicate, Fal, HeyBeauty)
   - Advanced settings: Category, Denoise steps, Seed
3. **Progress Section**: Hiển thị tiến trình xử lý
4. **Result Section**: Hiển thị kết quả cuối cùng

### Provider Options:

| Provider | Icon | Phương án | Mô tả |
|----------|------|-----------|-------|
| On-Premise | 🖥️ | 1 | Local model trên server |
| Replicate | ☁️ | 2 | Cloud API (Khuyến nghị) |
| Fal.ai | ⚡ | 2 | Fast cloud API |
| HeyBeauty | 💄 | 2 | Professional API |

## 🛠️ Công nghệ

- **HTML5**: Structure
- **CSS3**: Styling với modern features (Grid, Flexbox, Gradients, Animations)
- **Vanilla JavaScript**: Logic (không dùng framework)
- **Fetch API**: Call REST API
- **FormData**: Upload files

## 📁 Cấu trúc

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── style.css      # All styles
├── js/
│   └── app.js         # JavaScript logic
└── README.md          # This file
```

## 🎯 API Integration

Frontend tương tác với backend qua REST API:

### Endpoints sử dụng:

```javascript
// Health check
GET http://localhost:8000/

// Create task
POST http://localhost:8000/api/v1/tryon
FormData: {
  model_image: File,
  garment_image: File,
  provider: string,
  category: string,
  denoise_steps: number,
  seed: number
}

// Check status
GET http://localhost:8000/api/v1/tryon/{task_id}

// Download result
GET http://localhost:8000/api/v1/tryon/{task_id}/result
```

## 🎨 Customization

### Thay đổi theme colors:

Mở `css/style.css` và sửa CSS variables:

```css
:root {
    --primary: #6366f1;      /* Màu chính */
    --secondary: #ec4899;    /* Màu phụ */
    --success: #10b981;      /* Màu thành công */
    --error: #ef4444;        /* Màu lỗi */
}
```

### Thay đổi API URL:

Mở `js/app.js`:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',  // Đổi URL ở đây
    POLL_INTERVAL: 3000,
    MAX_POLL_ATTEMPTS: 100,
};
```

## 🐛 Troubleshooting

### Lỗi: "Không thể kết nối đến API server"

- Kiểm tra backend có đang chạy không
- Kiểm tra URL trong `js/app.js`
- Kiểm tra CORS settings trong backend

### Lỗi: "Task timeout"

- Tăng `MAX_POLL_ATTEMPTS` trong `js/app.js`
- Kiểm tra backend logs
- Thử provider khác

### Ảnh không hiển thị

- Kiểm tra file size (max 10MB)
- Kiểm tra định dạng (JPG, PNG)
- Clear browser cache

## 📱 Responsive Design

Frontend được thiết kế responsive:

- **Desktop**: Grid layout, 3 columns
- **Tablet**: 2 columns
- **Mobile**: 1 column, vertical stack

## 🚀 Performance

- Lazy load images
- Smooth animations với CSS transforms
- Debounced API calls
- Efficient DOM manipulation

## 📈 Future Improvements

- [ ] WebSocket cho real-time updates
- [ ] Image cropping tool
- [ ] Multiple garment selection
- [ ] History of tries
- [ ] User accounts
- [ ] Social sharing
- [ ] PWA support

## 👥 Credits

- UI/UX Design: Inspired by modern web apps
- Icons: Emoji
- Fonts: Google Fonts (Inter)
- Framework: Vanilla JS (no dependencies!)

---

**Enjoy virtual try-on! 🎉**
