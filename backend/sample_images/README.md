# Sample Images for Testing

Để test Fashion Try-On app, bạn cần 2 loại ảnh:

## 📸 1. Ảnh Người Mẫu (Model Image)

**Yêu cầu:**
- ✅ Người đứng thẳng, nhìn thẳng camera
- ✅ Toàn thân hoặc nửa thân trở lên
- ✅ Nền đơn giản, sáng (nền trắng tốt nhất)
- ✅ Mặc quần áo bình thường
- ✅ Độ phân giải: 512x512 đến 1024x1024 pixels
- ✅ Format: JPG hoặc PNG
- ✅ File size: < 10MB

**Không nên:**
- ❌ Người quay lưng hoặc nghiêng quá nhiều
- ❌ Nhiều người trong ảnh
- ❌ Ảnh mờ, tối
- ❌ Nền phức tạp, nhiều vật thể

## 👔 2. Ảnh Quần Áo (Garment Image)

**Yêu cầu:**
- ✅ Nền trắng hoặc trong suốt
- ✅ Quần áo phẳng, không nhăn
- ✅ Chụp toàn bộ sản phẩm
- ✅ Rõ nét, chi tiết
- ✅ Độ phân giải: 512x512 đến 1024x1024 pixels
- ✅ Format: JPG hoặc PNG
- ✅ File size: < 10MB

**Loại quần áo:**
- 👕 **Upperbody**: Áo thun, áo sơ mi, áo khoác, hoodie
- 👖 **Lowerbody**: Quần jean, quần tây, quần short
- 👗 **Dress**: Váy, đầm

## 🔗 Nguồn ảnh mẫu miễn phí

### Ảnh người mẫu:
1. **Unsplash** - https://unsplash.com/s/photos/portrait
   - Tìm kiếm: "portrait full body", "fashion model standing"

2. **Pexels** - https://www.pexels.com/search/fashion%20model/
   - Chất lượng cao, miễn phí

3. **Pixabay** - https://pixabay.com/images/search/fashion-model/
   - Free to use

### Ảnh quần áo:
1. **Remove.bg** - https://www.remove.bg/
   - Upload ảnh quần áo bất kỳ → Remove background → Download

2. **E-commerce sites** (chỉ để test):
   - ASOS, Zara, H&M product images
   - **Lưu ý**: Chỉ dùng để test, không commercial

3. **Fashion datasets**:
   - DeepFashion dataset
   - VITON dataset

## 📥 Download ảnh mẫu

### Quick test images:

Bạn có thể download từ Google Images với keyword:
- "person standing white background"
- "full body portrait white background"
- "t-shirt white background product"
- "dress white background product"

### Recommended dimensions:

```
Ảnh người:  768 x 1024 (portrait ratio)
Ảnh quần áo: 768 x 1024 (cùng ratio)
```

## 🎯 Ví dụ ảnh tốt

### Ảnh người mẫu tốt:
```
┌─────────────────┐
│                 │
│    👤          │ <- Person centered
│   /|\          │ <- Full body visible
│   / \          │ <- Simple background
│                 │
└─────────────────┘
```

### Ảnh quần áo tốt:
```
┌─────────────────┐
│                 │
│      👕        │ <- Garment centered
│                 │ <- White/transparent bg
│                 │ <- Flat, no wrinkles
│                 │
└─────────────────┘
```

## 🧪 Test với ảnh của bạn

1. Chụp ảnh bản thân:
   - Đứng cách tường 1-2m
   - Dùng timer hoặc nhờ người chụp
   - Ánh sáng tốt (ban ngày)

2. Chụp ảnh quần áo:
   - Trải phẳng trên nền trắng
   - Chụp từ trên xuống
   - Ánh sáng đều

3. Hoặc dùng ảnh từ Internet (cho mục đích test)

## 💡 Tips

- Ảnh càng rõ nét → kết quả càng tốt
- Nền càng đơn giản → xử lý càng nhanh
- Lighting tốt → chất lượng cao hơn
- Pose tự nhiên → kết quả tự nhiên hơn

## 🚀 Bắt đầu test

1. Download 1 ảnh người + 1 ảnh quần áo
2. Mở http://localhost:8000/app
3. Upload 2 ảnh
4. Chọn provider
5. Click "Bắt Đầu Thử Đồ"
6. Đợi kết quả!

---

**Note**: Folder này để hướng dẫn, không chứa ảnh thật.
Bạn tự download ảnh mẫu từ các nguồn trên.
