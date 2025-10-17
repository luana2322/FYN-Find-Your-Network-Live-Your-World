-- =============================================================================
-- POST, INTERACTION & REEL SERVICE - DATABASE INITIALIZATION
-- =============================================================================
-- SQL script để khởi tạo database PostgreSQL

-- Tạo database nếu chưa tồn tại
-- CREATE DATABASE post_interaction_reel_db;

-- Sử dụng database
\c post_interaction_reel_db;

-- Tạo extension nếu cần
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tạo schema nếu cần
-- CREATE SCHEMA IF NOT EXISTS app_schema;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE post_interaction_reel_db TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

-- Tạo bảng users (nếu cần cho authentication)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo index cho performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Insert sample data (optional)
INSERT INTO users (username, email, full_name, bio) VALUES 
('admin', 'admin@example.com', 'Administrator', 'System administrator'),
('user1', 'user1@example.com', 'User One', 'First user'),
('user2', 'user2@example.com', 'User Two', 'Second user')
ON CONFLICT (username) DO NOTHING;

-- Tạo function để update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tạo trigger cho users table
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Thông báo hoàn thành
\echo 'Database post_interaction_reel_db initialized successfully!'
\echo 'Tables created: users'
\echo 'Extensions enabled: uuid-ossp'
\echo 'Triggers created: update_users_updated_at'



