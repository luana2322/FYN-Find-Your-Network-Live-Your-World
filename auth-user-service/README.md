# Auth User Service

Một microservice Spring Boot hoàn chỉnh cho xác thực và quản lý người dùng với các tính năng:

## 🚀 Tính năng chính

### 🔐 Authentication & Authorization
- **Đăng ký người dùng mới** với email và mật khẩu
- **Đăng nhập/đăng xuất** với JWT token
- **Refresh token** để gia hạn phiên đăng nhập
- **Quên mật khẩu** với email verification
- **Reset mật khẩu** với mã xác thực
- **Xác thực email** với OTP

### 👤 User Management
- **Xem/sửa profile** (tên, avatar, bio, thông tin cá nhân)
- **Upload/delete avatar** với MinIO storage
- **Tìm kiếm người dùng** theo username, email, phone
- **Deactivate account**

### 👥 Social Features
- **Follow/Unfollow** người dùng khác
- **Xem danh sách followers/following**
- **Thống kê số lượng followers/following**

## 🛠️ Công nghệ sử dụng

- **Spring Boot 3.5.6** với Java 21
- **Spring Security** cho authentication
- **JWT** cho token-based authentication
- **PostgreSQL** làm database
- **Redis** cho caching và session management
- **MinIO** cho file storage
- **Spring Mail** cho email service
- **Swagger/OpenAPI** cho API documentation

## 📋 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Đăng ký tài khoản mới
- `POST /login` - Đăng nhập
- `POST /refresh` - Refresh token
- `POST /logout` - Đăng xuất
- `POST /forgot-password` - Quên mật khẩu
- `POST /reset-password` - Reset mật khẩu
- `POST /verify-email` - Xác thực email

### User Management (`/api/users`)
- `GET /profile` - Xem profile hiện tại
- `PUT /profile` - Cập nhật profile
- `GET /{userId}` - Xem profile người dùng khác
- `GET /search` - Tìm kiếm người dùng
- `DELETE /profile` - Deactivate account

### Follow System (`/api/follows`)
- `POST /{followeeId}` - Follow người dùng
- `DELETE /{followeeId}` - Unfollow người dùng
- `GET /{userId}/followers` - Xem danh sách followers
- `GET /{userId}/following` - Xem danh sách following
- `GET /{userId}/is-following` - Kiểm tra trạng thái follow
- `GET /{userId}/stats` - Thống kê followers/following

### File Management (`/api/files`)
- `POST /upload/avatar` - Upload avatar
- `DELETE /avatar` - Xóa avatar

## ⚙️ Cấu hình

### Database (PostgreSQL)
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/auth_user_service
spring.datasource.username=postgres
spring.datasource.password=password
```

### Redis
```properties
spring.data.redis.host=localhost
spring.data.redis.port=6379
```

### MinIO
```properties
minio.url=http://localhost:9000
minio.access-key=minioadmin
minio.secret-key=minioadmin
minio.bucket.name=avatars
```

### Email (Gmail)
```properties
spring.mail.host=smtp.gmail.com
spring.mail.port=587
spring.mail.username=your-email@gmail.com
spring.mail.password=your-app-password
```

### JWT
```properties
jwt.secret=mySecretKey123456789012345678901234567890123456789012345678901234567890
jwt.access-expiration=900000
jwt.refresh-expiration=604800000
```

## 🚀 Chạy ứng dụng

1. **Cài đặt dependencies:**
   ```bash
   mvn clean install
   ```

2. **Cấu hình database và services:**
   - PostgreSQL
   - Redis
   - MinIO

3. **Cập nhật application.properties** với thông tin cấu hình của bạn

4. **Chạy ứng dụng:**
   ```bash
   mvn spring-boot:run
   ```

5. **Truy cập Swagger UI:**
   ```
   http://localhost:8080/swagger-ui.html
   ```

## 📝 Ví dụ sử dụng API

### Đăng ký
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "useOtp": true
  }'
```

### Đăng nhập
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "john@example.com",
    "password": "password123"
  }'
```

### Upload avatar
```bash
curl -X POST http://localhost:8080/api/files/upload/avatar \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@avatar.jpg"
```

## 🔒 Bảo mật

- JWT token với expiration time
- Password encryption với BCrypt
- CORS configuration
- Input validation
- Exception handling
- Token blacklisting với Redis

## 📊 Database Schema

### Users Table
- id, email, phone, username (unique)
- password (encrypted)
- avatar_url, bio
- is_active, created_at, updated_at

### Follows Table
- id, follower_id, followee_id
- created_at

### Refresh Tokens Table
- id, token (unique)
- user_id, expiry_date
- revoked, device_id, created_at

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License
