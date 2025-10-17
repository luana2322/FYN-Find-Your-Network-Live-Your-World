#!/usr/bin/env python3
# =============================================================================
# POST, INTERACTION & REEL SERVICE - RUN.PY
# =============================================================================
# File để chạy dự án một cách đơn giản

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_dependencies():
    """Kiểm tra dependencies"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Cài đặt dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment():
    """Thiết lập environment"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration (PostgreSQL)
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

# Celery Configuration (optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Debug Mode
DEBUG=true
"""
        env_file.write_text(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def init_database():
    """Khởi tạo database"""
    print("🗄️ Initializing database...")
    try:
        subprocess.run([sys.executable, "app/db/init_db.py", "init"], check=True)
        print("✅ Database initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize database")
        return False

def run_application(host="0.0.0.0", port=8000, reload=True):
    """Chạy ứng dụng"""
    print(f"🚀 Starting application on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("Press Ctrl+C to stop")
    
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

def run_tests():
    """Chạy tests"""
    print("🧪 Running tests...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "app/tests/", "-v"], check=True)
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Post, Interaction & Reel Service Runner")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--setup", action="store_true", help="Setup environment")
    parser.add_argument("--init-db", action="store_true", help="Initialize database")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--quick-start", action="store_true", help="Quick start with all setup")
    
    args = parser.parse_args()
    
    print("🧾 Post, Interaction & Reel Service")
    print("=" * 50)
    
    # Quick start
    if args.quick_start:
        check_python_version()
        if not install_dependencies():
            sys.exit(1)
        setup_environment()
        if not init_database():
            sys.exit(1)
        run_application(args.host, args.port, not args.no_reload)
        return
    
    # Individual commands
    if args.install:
        check_python_version()
        install_dependencies()
        return
    
    if args.setup:
        setup_environment()
        return
    
    if args.init_db:
        init_database()
        return
    
    if args.test:
        if not check_dependencies():
            sys.exit(1)
        run_tests()
        return
    
    # Default: run application
    check_python_version()
    if not check_dependencies():
        print("\n💡 Tip: Run 'python run.py --install' to install dependencies")
        sys.exit(1)
    run_application(args.host, args.port, not args.no_reload)

if __name__ == "__main__":
    main()