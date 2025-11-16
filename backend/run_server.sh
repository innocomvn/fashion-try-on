#!/bin/bash

# Fashion Try-On Backend Server Launcher

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        Fashion Try-On Backend Server Launcher             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  .env file not found!"
    echo "Copying from .env.example..."
    cp backend/.env.example backend/.env
    echo "✅ Please edit backend/.env with your API keys"
    echo ""
fi

# Start server
echo "🚀 Starting FastAPI server..."
echo ""
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
