# 🧾 Post, Interaction & Reel Service

API quản lý bài viết (Post), tương tác (Interaction), video ngắn (Reel) và thông báo (Notification) trong hệ thống mạng xã hội.

## 🎯 Mục tiêu

Cung cấp API quản lý bài viết, tương tác, video ngắn và thông báo. Dịch vụ này cho phép người dùng đăng bài, xem feed, tương tác, tải video ngắn, và nhận thông báo realtime.

## ⚙️ Công nghệ sử dụng

| Thành phần | Mô tả |
|------------|-------|
| **Ngôn ngữ** | Python 3.8+ |
| **Framework** | FastAPI |
| **Database** | PostgreSQL |
| **Validation** | Pydantic |
| **Testing** | Pytest |

## 🧩 Chức năng chính

### A. Post Service
- ✅ Tạo bài viết mới (văn bản, ảnh, video)
- ✅ Chỉnh sửa / xóa bài viết
- ✅ Lấy danh sách bài viết cá nhân
- ✅ Lấy feed toàn cục hoặc theo danh sách người theo dõi
- ✅ Like / Unlike bài viết
- ✅ Comment / Reply / Delete comment

### B. Reel Service
- ✅ Upload video ngắn ≤ 60s
- ✅ Phát video dạng cuộn dọc (vertical feed)
- ✅ Theo dõi lượt xem, lượt thích, bình luận
- ✅ Like / Unlike reel
- ✅ Comment reel

### C. Notification Service
- ✅ Trigger thông báo khi có like, comment, follow
- ✅ Lưu trạng thái đọc/chưa đọc
- ✅ Lấy danh sách thông báo

## 🧱 Cấu trúc thư mục dự án

```
post_interaction_reel_service/
│
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config/                    # Configuration
│   │   ├── database.py
│   │   ├── settings.py
│   │   └── redis_config.py
│   ├── controller/                # API Controllers
│   │   ├── post_controller.py
│   │   ├── reel_controller.py
│   │   └── notification_controller.py
│   ├── service/                   # Business Logic
│   │   ├── post_service.py
│   │   ├── reel_service.py
│   │   └── notification_service.py
│   ├── repository/                # Data Access
│   │   ├── post_repository.py
│   │   ├── comment_repository.py
│   │   ├── reel_repository.py
│   │   └── notification_repository.py
│   ├── model/                     # Database Models
│   │   ├── post_model.py
│   │   ├── comment_model.py
│   │   ├── reel_model.py
│   │   └── notification_model.py
│   ├── schema/                    # Pydantic Schemas
│   │   ├── post_schema.py
│   │   ├── comment_schema.py
│   │   ├── reel_schema.py
│   │   └── notification_schema.py
│   ├── util/                      # Utilities
│   │   ├── s3_helper.py
│   │   ├── ffmpeg_worker.py
│   │   ├── notification_helper.py
│   │   └── cache_helper.py
│   ├── db/                        # Database Scripts
│   │   └── init_db.py
│   └── tests/                     # Tests
│       ├── test_post.py
│       ├── test_reel.py
│       └── test_notification.py
│
├── requirements.txt               # Dependencies
├── run.py                        # Application runner
├── imports_summary.py            # Import manager
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker services
├── docker-manage.sh              # Docker management (Linux/Mac)
├── docker-manage.bat             # Docker management (Windows)
├── env.docker                    # Docker environment
├── docker-commands.md            # Docker commands reference
├── DOCKER_SETUP.md               # Docker setup guide
└── README.md                     # Documentation
```

## 🚀 Cài đặt và chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd post-interaction-reel-service
```

### 2. Docker Setup (Khuyến nghị)
```bash
# Quick start với Docker
docker-manage.bat start  # Windows
./docker-manage.sh start  # Linux/Mac

# Hoặc thủ công
docker-compose up -d --build
```

### 3. Local Development
```bash
# Quick start
python run.py --quick-start

# Cài đặt thủ công
python run.py --install
python run.py --setup
python run.py --init-db
python run.py
```

### 4. Chạy tests
```bash
# Với Docker
docker-manage.bat test  # Windows
./docker-manage.sh test  # Linux/Mac

# Local
python run.py --test
```

## 🧠 API Endpoints

### Posts
| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| POST | `/posts/` | Tạo bài viết |
| GET | `/posts/feed/global` | Lấy feed toàn cục |
| GET | `/posts/feed/personal` | Lấy feed cá nhân |
| GET | `/posts/{id}` | Lấy bài viết theo ID |
| PUT | `/posts/{id}` | Sửa bài viết |
| DELETE | `/posts/{id}` | Xóa bài viết |
| POST | `/posts/{id}/like` | Like bài viết |
| DELETE | `/posts/{id}/like` | Unlike bài viết |
| POST | `/posts/comments` | Bình luận bài viết |
| GET | `/posts/{id}/comments` | Lấy bình luận |

### Reels
| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| POST | `/reels/` | Upload reel mới |
| GET | `/reels/feed` | Lấy danh sách reel |
| GET | `/reels/{id}` | Lấy reel theo ID |
| PUT | `/reels/{id}` | Sửa reel |
| DELETE | `/reels/{id}` | Xóa reel |
| POST | `/reels/{id}/like` | Like reel |
| DELETE | `/reels/{id}/like` | Unlike reel |
| POST | `/reels/{id}/view` | Ghi nhận lượt xem |
| POST | `/reels/comments` | Bình luận reel |

### Notifications
| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| GET | `/notifications/` | Lấy thông báo |
| GET | `/notifications/unread-count` | Đếm thông báo chưa đọc |
| PATCH | `/notifications/mark-read` | Đánh dấu đã đọc |
| PATCH | `/notifications/mark-all-read` | Đánh dấu tất cả đã đọc |
| DELETE | `/notifications/{id}` | Xóa thông báo |

## 📚 Import Management

File `imports_summary.py` chứa tất cả các import cần thiết:

```python
# Import cơ bản cho main.py
from fastapi import FastAPI
from app.config.database import engine, Base
from app.config.settings import settings

# Import cho controller
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.service.post_service import PostService
```

## 🔧 Cấu hình

### Local Development
File `.env` sẽ được tạo tự động:
```env
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/post_interaction_reel_db

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# MinIO Configuration (optional)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=post-interaction-reel
MINIO_SECURE=false

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Debug Mode
DEBUG=true
```

### Docker Environment
File `env.docker` chứa cấu hình cho Docker:
```env
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:password@db:5432/post_interaction_reel_db

# Redis Configuration
REDIS_URL=redis://redis:6379

# MinIO Configuration
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=post-interaction-reel
MINIO_SECURE=false
```

## ✅ Kiểm thử

### Với Docker
```bash
# Windows
docker-manage.bat test

# Linux/Mac
./docker-manage.sh test

# Hoặc trực tiếp
docker-compose exec app pytest app/tests/ -v
```

### Local Development
```bash
# Chạy tất cả tests
python run.py --test

# Hoặc sử dụng pytest trực tiếp
pytest app/tests/ -v
```

## 🆘 Troubleshooting

### Docker Issues
```bash
# Kiểm tra Docker
docker --version
docker-compose --version

# Restart Docker services
docker-manage.bat restart  # Windows
./docker-manage.sh restart  # Linux/Mac

# Xem logs
docker-compose logs -f app
```

### Python không được tìm thấy
```bash
# Kiểm tra Python
python --version

# Nếu không có, cài đặt từ python.org
```

### Dependencies không được cài đặt
```bash
# Cài đặt lại dependencies
python run.py --install
```

### Database error
```bash
# Local development
python run.py --init-db

# Docker
docker-compose exec app python app/db/init_db.py init
```

### Port conflicts
```bash
# Kiểm tra ports đang sử dụng
netstat -tulpn | grep :8000

# Thay đổi ports trong docker-compose.yml
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

---

**Post, Interaction & Reel Service** - Xây dựng với ❤️ bằng FastAPI và Python
