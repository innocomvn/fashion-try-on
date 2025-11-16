# 🚢 Deployment Guide - Fashion Try-On App

Hướng dẫn deploy app lên production.

## 📋 Mục lục

1. [Docker Deployment](#docker-deployment)
2. [VPS/Cloud Deployment](#vpscloud-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Environment Variables](#environment-variables)
6. [Security Checklist](#security-checklist)

---

## 🐳 Docker Deployment

### 1. Tạo Dockerfile

**File: `Dockerfile`**

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create directories
RUN mkdir -p uploads results models logs

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose (với Redis - Optional)

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./fashion_tryon.db
      - REPLICATE_API_TOKEN=${REPLICATE_API_TOKEN}
    volumes:
      - ./uploads:/app/uploads
      - ./results:/app/results
      - ./models:/app/models
    restart: unless-stopped

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### 3. Build và Run

```bash
# Build image
docker build -t fashion-tryon .

# Run container
docker run -d -p 8000:8000 \
  -e REPLICATE_API_TOKEN="your_token" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/results:/app/results \
  --name fashion-tryon \
  fashion-tryon

# Hoặc dùng docker-compose
docker-compose up -d
```

---

## 🖥️ VPS/Cloud Deployment

### Prerequisites
- Ubuntu 20.04+ hoặc Debian 11+
- Python 3.10+
- Nginx (recommended)

### 1. Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python và dependencies
sudo apt install python3.10 python3.10-venv python3-pip nginx -y

# Create user
sudo useradd -m -s /bin/bash fashionapp
sudo su - fashionapp
```

### 2. Deploy Application

```bash
# Clone repo
git clone https://github.com/your-repo/fashion-try-on.git
cd fashion-try-on

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Create .env file
cp backend/.env.example backend/.env
nano backend/.env  # Edit với API keys

# Create directories
mkdir -p uploads results models logs

# Test run
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 3. Setup Systemd Service

**File: `/etc/systemd/system/fashion-tryon.service`**

```ini
[Unit]
Description=Fashion Try-On API
After=network.target

[Service]
Type=simple
User=fashionapp
WorkingDirectory=/home/fashionapp/fashion-try-on
Environment="PATH=/home/fashionapp/fashion-try-on/venv/bin"
ExecStart=/home/fashionapp/fashion-try-on/venv/bin/gunicorn \
    backend.main:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /home/fashionapp/fashion-try-on/logs/access.log \
    --error-logfile /home/fashionapp/fashion-try-on/logs/error.log

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable và start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable fashion-tryon
sudo systemctl start fashion-tryon
sudo systemctl status fashion-tryon
```

### 4. Setup Nginx Reverse Proxy

**File: `/etc/nginx/sites-available/fashion-tryon`**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:8000/app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Increase timeout for long-running tasks
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }

    # Static files
    location /static {
        proxy_pass http://127.0.0.1:8000/static;
    }

    location /uploads {
        proxy_pass http://127.0.0.1:8000/uploads;
    }

    location /results {
        proxy_pass http://127.0.0.1:8000/results;
    }

    # File upload size
    client_max_body_size 10M;
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/fashion-tryon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Setup SSL (HTTPS) with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🚀 Heroku Deployment

### 1. Tạo files cần thiết

**File: `Procfile`**
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

**File: `runtime.txt`**
```
python-3.10.12
```

### 2. Deploy

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create fashion-tryon-app

# Set environment variables
heroku config:set REPLICATE_API_TOKEN="your_token"
heroku config:set USE_EXTERNAL_API=True
heroku config:set API_PROVIDER="replicate"

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🚂 Railway Deployment

### 1. Tạo `railway.json`

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Deploy

1. Vào https://railway.app/
2. Click "New Project" → "Deploy from GitHub"
3. Chọn repository
4. Set environment variables
5. Deploy!

---

## 🔐 Environment Variables

### Production .env Example

```bash
# Application
APP_NAME="Fashion Try-On Production"
DEBUG=False
HOST="0.0.0.0"
PORT=8000

# External API (Choose one)
USE_EXTERNAL_API=True
API_PROVIDER="replicate"
REPLICATE_API_TOKEN="r8_xxxxx"

# Database (upgrade to PostgreSQL in production)
DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# File Storage (upgrade to S3 in production)
UPLOAD_DIR="/app/uploads"
RESULT_DIR="/app/results"

# Security
ALLOWED_HOSTS="your-domain.com,www.your-domain.com"
SECRET_KEY="your-secret-key-here"

# Logging
LOG_LEVEL="INFO"

# Optional
SENTRY_DSN="your-sentry-dsn"  # Error tracking
REDIS_URL="redis://localhost:6379"  # Caching
```

---

## 🛡️ Security Checklist

### Before Production:

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY`
- [ ] Setup HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Setup firewall (ufw)
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Use strong passwords
- [ ] Keep dependencies updated
- [ ] Setup error tracking (Sentry)
- [ ] Add authentication (if needed)
- [ ] Validate all inputs
- [ ] Sanitize file uploads
- [ ] Setup CDN for static files

### Firewall Setup (Ubuntu/Debian)

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## 📊 Monitoring

### Setup Logs

```bash
# View logs
sudo journalctl -u fashion-tryon -f

# Application logs
tail -f logs/app.log
tail -f logs/error.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Checks

```bash
# Check API health
curl http://localhost:8000/

# Check service status
sudo systemctl status fashion-tryon
sudo systemctl status nginx
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
cd /home/fashionapp/fashion-try-on
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart fashion-tryon
```

### Backup Database

```bash
# Backup SQLite
cp fashion_tryon.db backups/fashion_tryon_$(date +%Y%m%d).db

# Backup uploads/results
tar -czf backups/files_$(date +%Y%m%d).tar.gz uploads/ results/
```

---

## 🆘 Troubleshooting

### App not starting
```bash
# Check logs
sudo journalctl -u fashion-tryon -n 100

# Check permissions
ls -la /home/fashionapp/fashion-try-on

# Test manually
cd /home/fashionapp/fashion-try-on
source venv/bin/activate
python -m uvicorn backend.main:app
```

### High memory usage
```bash
# Monitor
htop

# Reduce workers
# Edit /etc/systemd/system/fashion-tryon.service
# Change: -w 4 to -w 2
```

---

## 📚 Resources

- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- Docker: https://docs.docker.com/
- Let's Encrypt: https://letsencrypt.org/

---

**Good luck with deployment! 🚀**
