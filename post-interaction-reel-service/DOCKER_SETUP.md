# =============================================================================
# POST, INTERACTION & REEL SERVICE - DOCKER SETUP GUIDE
# =============================================================================
# Hướng dẫn sử dụng Docker để chạy dự án

## 🐳 Docker Setup

### 1. Yêu cầu hệ thống
- Docker Desktop (Windows/Mac) hoặc Docker Engine (Linux)
- Docker Compose
- ít nhất 4GB RAM
- 10GB disk space

### 2. Cài đặt Docker

#### Windows:
1. Download Docker Desktop từ https://docker.com
2. Cài đặt và khởi động Docker Desktop
3. Đảm bảo Docker đang chạy

#### Mac:
1. Download Docker Desktop từ https://docker.com
2. Cài đặt và khởi động Docker Desktop

#### Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Kiểm tra cài đặt
```bash
docker --version
docker-compose --version
```

## 🚀 Cách sử dụng

### Quick Start (Cách nhanh nhất)
```bash
# Windows
docker-manage.bat start

# Linux/Mac
./docker-manage.sh start
```

### Cài đặt thủ công
```bash
# 1. Build và start tất cả services
docker-compose up -d --build

# 2. Khởi tạo database
docker-compose exec app python app/db/init_db.py init

# 3. Kiểm tra status
docker-compose ps
```

### Các lệnh hữu ích

#### Quản lý services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f app

# Check status
docker-compose ps
```

#### Development
```bash
# Run tests
docker-compose exec app pytest

# Access container shell
docker-compose exec app bash

# View database
docker-compose exec db psql -U postgres -d post_interaction_reel_db
```

#### Production
```bash
# Build production image
docker build -t post-interaction-reel-service:latest .

# Run with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🌐 Services và Ports

| Service | Port | URL | Mô tả |
|---------|------|-----|-------|
| **FastAPI App** | 8000 | http://localhost:8000 | Main API |
| **API Docs** | 8000 | http://localhost:8000/docs | Swagger UI |
| **PostgreSQL** | 5432 | localhost:5432 | Database |
| **Redis** | 6379 | localhost:6379 | Cache |
| **MinIO** | 9000 | localhost:9000 | Object Storage |
| **MinIO Console** | 9001 | http://localhost:9001 | MinIO Web UI |
| (RabbitMQ removed) |  |  |  |

## 🔧 Configuration

### Environment Variables
File `env.docker` chứa tất cả environment variables:
```env
DATABASE_URL=postgresql://postgres:password@db:5432/post_interaction_reel_db
REDIS_URL=redis://redis:6379
MINIO_ENDPOINT=minio:9000
# ... và nhiều hơn
```

### Volumes
- `postgres_data`: Database data
- `redis_data`: Redis data
- `minio_data`: MinIO object storage
  

### Networks
- `app-network`: Bridge network cho tất cả services

## 🧪 Testing

### Chạy tests
```bash
# Sử dụng script
docker-manage.bat test  # Windows
./docker-manage.sh test  # Linux/Mac

# Hoặc trực tiếp
docker-compose exec app pytest app/tests/ -v
```

### Test coverage
```bash
docker-compose exec app pytest --cov=app --cov-report=html
```

## 🐛 Troubleshooting

### Services không start
```bash
# Kiểm tra logs
docker-compose logs

# Kiểm tra status
docker-compose ps

# Restart services
docker-compose restart
```

### Database connection error
```bash
# Kiểm tra database
docker-compose exec db psql -U postgres -c "\l"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Port conflicts
```bash
# Kiểm tra ports đang sử dụng
netstat -tulpn | grep :8000

# Thay đổi ports trong docker-compose.yml
```

### Memory issues
```bash
# Kiểm tra resource usage
docker stats

# Tăng memory limit trong Docker Desktop
```

## 🧹 Cleanup

### Clean up containers
```bash
# Stop và remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Clean up system
```bash
# Remove unused containers, networks, images
docker system prune -f

# Remove everything
docker system prune -a -f
```

## 📊 Monitoring

### Health checks
```bash
# API health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready -U postgres

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs
```bash
# Application logs
docker-compose logs -f app

# Database logs
docker-compose logs -f db

# All logs
docker-compose logs -f
```

## 🔒 Security

### Production setup
1. Thay đổi default passwords
2. Sử dụng secrets management
3. Enable SSL/TLS
4. Configure firewall
5. Regular security updates

### Secrets
```bash
# Create secrets
echo "your-secret-key" | docker secret create secret_key -

# Use in docker-compose.yml
secrets:
  - secret_key
```

## 📈 Scaling

### Horizontal scaling
```bash
# Scale workers
docker-compose up -d --scale celery_worker=3

# Load balancer
docker-compose up -d --scale app=3
```

### Vertical scaling
```bash
# Increase memory/CPU limits
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
```

---

**Docker Setup** - Xây dựng với ❤️ bằng Docker và Docker Compose



