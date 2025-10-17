@echo off
REM =============================================================================
REM POST, INTERACTION & REEL SERVICE - DOCKER MANAGEMENT (Windows)
REM =============================================================================
REM Batch script để quản lý Docker containers trên Windows

echo.
echo =============================================================================
echo POST, INTERACTION & REEL SERVICE - DOCKER MANAGEMENT
echo =============================================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not running!
    echo Please install Docker Desktop from https://docker.com
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed!
    echo Please install Docker Compose first
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Parse command line arguments
if "%1"=="" goto :show_help
if "%1"=="start" goto :start_all
if "%1"=="stop" goto :stop_all
if "%1"=="restart" goto :restart_all
if "%1"=="logs" goto :show_logs
if "%1"=="status" goto :show_status
if "%1"=="test" goto :run_tests
if "%1"=="init-db" goto :init_db
if "%1"=="cleanup" goto :cleanup
if "%1"=="help" goto :show_help
goto :show_help

:show_help
echo.
echo Usage: docker-manage.bat [COMMAND]
echo.
echo Commands:
echo   start     Start all services
echo   stop      Stop all services
echo   restart   Restart all services
echo   logs      Show application logs
echo   status    Show service status
echo   test      Run tests
echo   init-db   Initialize database
echo   cleanup   Clean up everything
echo   help      Show this help message
echo.
echo Examples:
echo   docker-manage.bat start
echo   docker-manage.bat logs
echo   docker-manage.bat test
echo.
pause
exit /b 0

:start_all
echo.
echo 🚀 Starting Post, Interaction & Reel Service...
echo.

echo 📦 Building and starting all services...
docker-compose up -d --build
if errorlevel 1 (
    echo ❌ Failed to start services!
    pause
    exit /b 1
)

echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo ✅ Services started successfully!
echo.
echo 🌐 Services available at:
echo   - API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - MinIO Console: http://localhost:9001
echo.
goto :end

:stop_all
echo.
echo 🛑 Stopping Post, Interaction & Reel Service...
echo.

docker-compose down
if errorlevel 1 (
    echo ❌ Failed to stop services!
    pause
    exit /b 1
)

echo ✅ Services stopped successfully!
goto :end

:restart_all
echo.
echo 🔄 Restarting Post, Interaction & Reel Service...
echo.

docker-compose restart
if errorlevel 1 (
    echo ❌ Failed to restart services!
    pause
    exit /b 1
)

echo ✅ Services restarted successfully!
goto :end

:show_logs
echo.
echo 📋 Showing Application Logs...
echo Press Ctrl+C to exit
echo.

docker-compose logs -f app
goto :end

:show_status
echo.
echo 📊 Service Status:
echo.

docker-compose ps
goto :end

:run_tests
echo.
echo 🧪 Running Tests...
echo.

docker-compose exec app pytest app/tests/ -v
if errorlevel 1 (
    echo ❌ Some tests failed!
    pause
    exit /b 1
)

echo ✅ All tests passed!
goto :end

:init_db
echo.
echo 🗄️ Initializing Database...
echo.

docker-compose exec app python app/db/init_db.py init
if errorlevel 1 (
    echo ❌ Failed to initialize database!
    pause
    exit /b 1
)

echo ✅ Database initialized successfully!
goto :end

:cleanup
echo.
echo 🧹 Cleaning Up...
echo.
echo ⚠️  This will remove all containers, volumes, and images. Are you sure? (y/N)
set /p choice="Continue? "

if /i not "%choice%"=="y" (
    echo Cleanup cancelled.
    goto :end
)

echo.
echo 🛑 Stopping and removing containers...
docker-compose down -v

echo 🗑️ Removing images...
docker-compose down --rmi all

echo 🧹 Cleaning up system...
docker system prune -f

echo ✅ Cleanup completed!
goto :end

:end
echo.
pause



