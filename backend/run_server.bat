@echo off
REM Fashion Try-On Backend Server Launcher for Windows

echo ╔═══════════════════════════════════════════════════════════╗
echo ║        Fashion Try-On Backend Server Launcher             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r backend\requirements.txt
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  .env file not found!
    echo Copying from .env.example...
    copy backend\.env.example backend\.env
    echo ✅ Please edit backend\.env with your API keys
    echo.
)

REM Start server
echo 🚀 Starting FastAPI server...
echo.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
