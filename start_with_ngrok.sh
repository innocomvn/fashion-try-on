#!/bin/bash

# Fashion Try-On - Start with Ngrok
# Chạy backend + ngrok để expose ra internet

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Fashion Try-On - Internet Access with Ngrok         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}❌ Ngrok chưa được cài đặt!${NC}"
    echo ""
    echo "Cài đặt ngrok:"
    echo ""
    echo "Linux/Mac:"
    echo "  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null"
    echo "  echo \"deb https://ngrok-agent.s3.amazonaws.com buster main\" | sudo tee /etc/apt/sources.list.d/ngrok.list"
    echo "  sudo apt update && sudo apt install ngrok"
    echo ""
    echo "Hoặc dùng snap:"
    echo "  sudo snap install ngrok"
    echo ""
    echo "Mac (Homebrew):"
    echo "  brew install ngrok/ngrok/ngrok"
    echo ""
    echo "Sau đó setup authtoken:"
    echo "  ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "Lấy token tại: https://dashboard.ngrok.com/get-started/your-authtoken"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment không tồn tại. Đang tạo...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment đã được tạo${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔄 Kích hoạt virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}📦 Cài đặt dependencies...${NC}"
    pip install -r backend/requirements.txt
    echo -e "${GREEN}✅ Dependencies đã được cài đặt${NC}"
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  File .env không tồn tại. Đang tạo từ template...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ File .env đã được tạo${NC}"
    echo -e "${YELLOW}👉 Vui lòng edit backend/.env và thêm API keys${NC}"
    echo ""
fi

# Create PID file directory
mkdir -p .pids

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Đang dừng services...${NC}"

    # Kill backend
    if [ -f .pids/backend.pid ]; then
        PID=$(cat .pids/backend.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            echo -e "${GREEN}✅ Backend đã dừng${NC}"
        fi
        rm .pids/backend.pid
    fi

    # Kill ngrok
    if [ -f .pids/ngrok.pid ]; then
        PID=$(cat .pids/ngrok.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            echo -e "${GREEN}✅ Ngrok đã dừng${NC}"
        fi
        rm .pids/ngrok.pid
    fi

    echo -e "${GREEN}👋 Bye!${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Start backend in background
echo -e "${BLUE}🚀 Đang khởi động FastAPI backend...${NC}"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > .pids/backend.pid

# Wait for backend to start
echo -e "${BLUE}⏳ Đợi backend khởi động...${NC}"
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend không khởi động được!${NC}"
    echo -e "${YELLOW}📋 Xem logs:${NC}"
    tail -20 logs/backend.log
    exit 1
fi

echo -e "${GREEN}✅ Backend đang chạy (PID: $BACKEND_PID)${NC}"

# Start ngrok in background
echo -e "${BLUE}🌐 Đang khởi động Ngrok...${NC}"
ngrok http 8000 --log=stdout > logs/ngrok.log 2>&1 &
NGROK_PID=$!
echo $NGROK_PID > .pids/ngrok.pid

# Wait for ngrok to start
echo -e "${BLUE}⏳ Đợi ngrok kết nối...${NC}"
sleep 4

# Get ngrok public URL
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Services đã khởi động thành công!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Try to get ngrok URL from API
NGROK_URL=""
for i in {1..5}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1)
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
    sleep 1
done

if [ ! -z "$NGROK_URL" ]; then
    echo -e "${GREEN}🌍 Public URL (Ngrok):${NC}"
    echo -e "${BLUE}${NGROK_URL}/app${NC}"
    echo ""
    echo -e "${YELLOW}👉 Share link này để test từ bất kỳ đâu!${NC}"
    echo ""

    # Generate QR code if qrencode is available
    if command -v qrencode &> /dev/null; then
        echo -e "${GREEN}📱 QR Code (quét bằng điện thoại):${NC}"
        echo ""
        qrencode -t ANSI "${NGROK_URL}/app"
        echo ""
    fi
else
    echo -e "${YELLOW}⚠️  Không lấy được Ngrok URL tự động${NC}"
    echo -e "${YELLOW}👉 Mở http://localhost:4040 để xem Ngrok URL${NC}"
    echo ""
fi

echo -e "${GREEN}📊 Local URLs:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:8000/app${NC}"
echo -e "   API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "   Ngrok Dashboard: ${BLUE}http://localhost:4040${NC}"
echo ""

echo -e "${GREEN}📋 Logs:${NC}"
echo -e "   Backend: ${BLUE}tail -f logs/backend.log${NC}"
echo -e "   Ngrok: ${BLUE}tail -f logs/ngrok.log${NC}"
echo ""

echo -e "${YELLOW}🛑 Nhấn Ctrl+C để dừng tất cả services${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Keep script running
wait $BACKEND_PID
