# ============================
# 1. Build Stage
# ============================
FROM maven:3.9.6-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy toàn bộ source
COPY . .

# Build dự án (bỏ test để nhanh)
RUN mvn clean package -DskipTests

# ============================
# 2. Run Stage
# ============================
FROM eclipse-temurin:17-jdk
WORKDIR /app

# Copy jar từ stage build
COPY --from=builder /app/target/*.jar app.jar

# Expose port Spring Boot
EXPOSE 8080

# Chạy Spring Boot
ENTRYPOINT ["java", "-jar", "app.jar"]
