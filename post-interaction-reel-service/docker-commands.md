# =============================================================================
# POST, INTERACTION & REEL SERVICE - DOCKER SETUP
# =============================================================================
# Scripts để quản lý Docker containers

# =============================================================================
# 1. DOCKER COMMANDS
# =============================================================================

# Build và chạy toàn bộ stack
docker-compose up -d

# Build lại image
docker-compose build

# Xem logs
docker-compose logs -f app

# Dừng tất cả services
docker-compose down

# Dừng và xóa volumes
docker-compose down -v

# Restart service cụ thể
docker-compose restart app

# Scale service
docker-compose up -d --scale celery_worker=3

# =============================================================================
# 2. DEVELOPMENT COMMANDS
# =============================================================================

# Chạy chỉ database và redis
docker-compose up -d db redis

# Chạy app trong development mode
docker-compose up app

# Chạy tests trong container
docker-compose exec app pytest

# Vào container để debug
docker-compose exec app bash

# =============================================================================
# 3. PRODUCTION COMMANDS
# =============================================================================

# Build production image
docker build -t post-interaction-reel-service:latest .

# Chạy production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# =============================================================================
# 4. UTILITY COMMANDS
# =============================================================================

# Xem status containers
docker-compose ps

# Xem resource usage
docker stats

# Clean up
docker system prune -f

# Backup database
docker-compose exec db pg_dump -U postgres post_interaction_reel_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres post_interaction_reel_db < backup.sql



