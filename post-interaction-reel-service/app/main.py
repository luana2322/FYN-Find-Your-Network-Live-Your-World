from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.controller.post_controller import router as post_router
from app.controller.reel_controller import router as reel_router
from app.controller.notification_controller import router as notification_router
from app.config.database import engine, Base
from app.config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Post, Interaction & Reel Service...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    
    yield
    
    # Shutdown
    print("Shutting down Post, Interaction & Reel Service...")

app = FastAPI(
    title="Post, Interaction & Reel Service",
    description="API quản lý bài viết (Post), tương tác (Interaction), video ngắn (Reel) và thông báo (Notification)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(post_router)
app.include_router(reel_router)
app.include_router(notification_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Post, Interaction & Reel Service API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "post-interaction-reel-service",
        "version": "1.0.0"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
