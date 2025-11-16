@echo off
REM Fashion Try-On - Start with Ngrok (Windows)

echo ╔══════════════════════════════════════════════════════════╗
echo ║     Fashion Try-On - Internet Access with Ngrok         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ngrok chưa được cài đặt!
    echo.
    echo Cài đặt ngrok:
    echo   1. Download từ: https://ngrok.com/download
    echo   2. Giải nén và thêm vào PATH
    echo   3. Hoặc dùng Chocolatey: choco install ngrok
    echo.
    echo Sau đó setup authtoken:
    echo   ngrok config add-authtoken YOUR_TOKEN
    echo.
    echo Lấy token tại: https://dashboard.ngrok.com/get-started/your-authtoken
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment không tồn tại. Đang tạo...
    python -m venv venv
    echo ✅ Virtual environment đã được tạo
)

REM Activate virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 📦 Cài đặt dependencies...
    pip install -r backend\requirements.txt
    echo ✅ Dependencies đã được cài đặt
)

REM Check if .env exists
if not exist "backend\.env" (
    echo ⚠️  File .env không tồn tại. Đang tạo từ template...
    copy backend\.env.example backend\.env
    echo ✅ File .env đã được tạo
    echo 👉 Vui lòng edit backend\.env và thêm API keys
    echo.
)

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo 🚀 Đang khởi động FastAPI backend...
start "Fashion Try-On Backend" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

echo ⏳ Đợi backend khởi động...
timeout /t 3 /nobreak >nul

echo 🌐 Đang khởi động Ngrok...
start "Fashion Try-On Ngrok" cmd /k "ngrok http 8000"

echo ⏳ Đợi ngrok kết nối...
timeout /t 4 /nobreak >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ Services đã khởi động thành công!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📊 URLs:
echo    Frontend: http://localhost:8000/app
echo    API Docs: http://localhost:8000/docs
echo    Ngrok Dashboard: http://localhost:4040
echo.
echo 🌍 Ngrok Public URL:
echo    👉 Mở http://localhost:4040 để xem public URL
echo.
echo 🛑 Đóng cửa sổ cmd để dừng services
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pause
