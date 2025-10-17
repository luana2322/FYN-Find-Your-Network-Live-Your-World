# Exception Handling System

Hệ thống exception handling của Auth User Service được thiết kế để cung cấp error handling nhất quán và dễ hiểu cho tất cả các API endpoints.

## 📋 Danh sách Exception Classes

### 🔴 Core Exceptions

#### `ApiException`
- **Mục đích**: Exception chung cho các lỗi API
- **HTTP Status**: 400 Bad Request
- **Sử dụng**: Các lỗi chung không thuộc category cụ thể

#### `ResourceNotFoundException`
- **Mục đích**: Khi không tìm thấy resource
- **HTTP Status**: 404 Not Found
- **Sử dụng**: User không tồn tại, RefreshToken không tồn tại
- **Constructor đặc biệt**: `ResourceNotFoundException(String resourceType, String fieldName, Object fieldValue)`

#### `UnauthorizedException`
- **Mục đích**: Lỗi xác thực/ủy quyền
- **HTTP Status**: 401 Unauthorized
- **Sử dụng**: Account bị deactivate, không có quyền truy cập

#### `InvalidTokenException`
- **Mục đích**: Lỗi liên quan đến JWT token
- **HTTP Status**: 401 Unauthorized
- **Sử dụng**: Token không hợp lệ, token hết hạn, token không tìm thấy

### 🟡 Business Logic Exceptions

#### `ValidationException`
- **Mục đích**: Lỗi validation dữ liệu đầu vào
- **HTTP Status**: 400 Bad Request
- **Sử dụng**: Dữ liệu không hợp lệ, format sai

#### `DuplicateResourceException`
- **Mục đích**: Resource đã tồn tại
- **HTTP Status**: 409 Conflict
- **Sử dụng**: Email đã tồn tại, Phone đã tồn tại
- **Constructor đặc biệt**: `DuplicateResourceException(String resourceType, String fieldName, Object fieldValue)`

#### `BusinessLogicException`
- **Mục đích**: Lỗi logic nghiệp vụ
- **HTTP Status**: 400 Bad Request
- **Sử dụng**: Follow chính mình, đã follow rồi, không follow mà muốn unfollow

### 🔵 Service-Specific Exceptions

#### `FileUploadException`
- **Mục đích**: Lỗi upload file
- **HTTP Status**: 400 Bad Request
- **Sử dụng**: File quá lớn, format không hỗ trợ, lỗi MinIO

#### `EmailServiceException`
- **Mục đích**: Lỗi gửi email
- **HTTP Status**: 500 Internal Server Error
- **Sử dụng**: Lỗi SMTP, không gửi được email verification

## 🛠️ GlobalExceptionHandler

`GlobalExceptionHandler` xử lý tất cả exceptions và trả về response format nhất quán:

```json
{
  "success": false,
  "message": "Error message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Exception Mapping:

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `ApiException` | 400 | General API errors |
| `ResourceNotFoundException` | 404 | Resource not found |
| `UnauthorizedException` | 401 | Authentication/Authorization errors |
| `InvalidTokenException` | 401 | JWT token errors |
| `ValidationException` | 400 | Input validation errors |
| `DuplicateResourceException` | 409 | Resource already exists |
| `FileUploadException` | 400 | File upload errors |
| `EmailServiceException` | 500 | Email service errors |
| `BusinessLogicException` | 400 | Business logic errors |
| `AuthenticationException` | 401 | Spring Security auth errors |
| `BadCredentialsException` | 401 | Invalid credentials |
| `MethodArgumentNotValidException` | 400 | Validation annotation errors |
| `IllegalArgumentException` | 400 | Invalid arguments |
| `Exception` | 500 | Generic catch-all |

## 📝 Ví dụ sử dụng

### Trong Service Layer:

```java
// Resource not found
User user = userRepository.findByEmail(email)
    .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

// Duplicate resource
if (userRepository.existsByEmail(email)) {
    throw new DuplicateResourceException("User", "email", email);
}

// Business logic error
if (followerId.equals(followeeId)) {
    throw new BusinessLogicException("Cannot follow yourself");
}

// File upload error
if (file.getSize() > MAX_SIZE) {
    throw new FileUploadException("File size must be less than 5MB");
}

// Email service error
try {
    emailService.sendEmail(email, code);
} catch (Exception e) {
    throw new EmailServiceException("Failed to send email", e);
}
```

### Response Examples:

#### Resource Not Found:
```json
{
  "success": false,
  "message": "User not found with email: john@example.com",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Duplicate Resource:
```json
{
  "success": false,
  "message": "User already exists with email: john@example.com",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Validation Error:
```json
{
  "success": false,
  "message": "Validation failed: {email=must be a valid email, password=size must be between 6 and 20}",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔧 Best Practices

1. **Sử dụng exception phù hợp**: Chọn exception class phù hợp với loại lỗi
2. **Constructor đặc biệt**: Sử dụng constructor với resourceType, fieldName, fieldValue khi có thể
3. **Wrap exceptions**: Wrap checked exceptions với custom exceptions
4. **Logging**: Log exceptions trước khi throw
5. **Consistent messages**: Sử dụng message format nhất quán

## 🚀 Mở rộng

Để thêm exception mới:

1. Tạo exception class extend từ `RuntimeException`
2. Thêm constructor với message và cause
3. Thêm handler trong `GlobalExceptionHandler`
4. Cập nhật documentation này
