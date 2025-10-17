# =============================================================================
# POST, INTERACTION & REEL SERVICE - IMPORTS MANAGER
# =============================================================================
# File quản lý import thư viện cho dự án

# =============================================================================
# 1. CORE IMPORTS (Bắt buộc)
# =============================================================================
# FastAPI & Web Framework
from fastapi import FastAPI, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

# Database & ORM (PostgreSQL)
from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, Boolean, ForeignKey, ARRAY, desc, and_, func
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import psycopg2
from psycopg2.extras import RealDictCursor

# Pydantic & Validation
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any, Union

# Environment & Configuration
import os
from dotenv import load_dotenv

# =============================================================================
# 2. OPTIONAL IMPORTS (Chỉ import khi cần)
# =============================================================================
# Redis (nếu dùng cache)
# import redis
# from redis import Redis

# File Storage (nếu dùng S3/MinIO)
# import boto3
# from minio import Minio
# from minio.error import S3Error

# Video Processing (nếu dùng FFmpeg)
# import ffmpeg
# from PIL import Image

# Notifications (nếu dùng Firebase)
# import firebase_admin
# from firebase_admin import credentials, messaging

# HTTP Client
import httpx

# Security
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
import secrets
import hashlib

# Testing
import pytest
from unittest.mock import Mock, patch

# =============================================================================
# 3. APPLICATION IMPORTS (Tự tạo)
# =============================================================================
# Configuration
from app.config.database import Base, engine, SessionLocal, get_db
from app.config.settings import settings

# Models
from app.model.post_model import Post, Comment, Like
from app.model.reel_model import Reel, ReelComment
from app.model.notification_model import Notification

# Schemas
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse, PostFeedResponse
from app.schema.comment_schema import CommentCreate, CommentUpdate, CommentResponse, LikeRequest, LikeResponse
from app.schema.reel_schema import ReelCreate, ReelUpdate, ReelResponse, ReelFeedResponse, ReelCommentCreate, ReelCommentResponse
from app.schema.notification_schema import NotificationResponse, NotificationListResponse, MarkAsReadRequest

# Repositories
from app.repository.post_repository import PostRepository
from app.repository.comment_repository import CommentRepository, LikeRepository
from app.repository.reel_repository import ReelRepository, ReelCommentRepository
from app.repository.notification_repository import NotificationRepository

# Services
from app.service.post_service import PostService
from app.service.reel_service import ReelService
from app.service.notification_service import NotificationService

# Controllers
from app.controller.post_controller import router as post_router
from app.controller.reel_controller import router as reel_router
from app.controller.notification_controller import router as notification_router

# Utilities (nếu cần)
# from app.util.s3_helper import S3Helper
# from app.util.ffmpeg_worker import FFmpegWorker
# from app.util.notification_helper import NotificationHelper
# from app.util.cache_helper import CacheHelper

# =============================================================================
# 4. STANDARD LIBRARY IMPORTS (Built-in)
# =============================================================================
import json
import asyncio
import threading
import multiprocessing
import functools
import itertools
from collections import defaultdict, Counter
import re
import base64
import io
import gzip
import zipfile
import traceback
import sys
import logging
import time
from datetime import datetime, timedelta, timezone
import shutil
import mimetypes
import platform
import subprocess
import signal

# =============================================================================
# 5. IMPORT HELPER FUNCTIONS
# =============================================================================
def import_optional(module_name: str, package: str = None):
    """
    Import module một cách an toàn, trả về None nếu không tìm thấy
    """
    try:
        if package:
            return __import__(module_name, fromlist=[package])
        return __import__(module_name)
    except ImportError:
        return None

def check_dependencies():
    """
    Kiểm tra các dependencies cần thiết
    """
    required_modules = [
        'fastapi',
        'uvicorn', 
        'sqlalchemy',
        'pydantic',
        'psycopg2'
    ]
    
    missing_modules = []
    for module in required_modules:
        if import_optional(module) is None:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True

# =============================================================================
# 6. USAGE EXAMPLES
# =============================================================================
"""
# Cách sử dụng:

# 1. Import cơ bản cho main.py
from fastapi import FastAPI
from app.config.database import engine, Base
from app.config.settings import settings

# 2. Import cho controller
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.service.post_service import PostService

# 3. Import cho service
from sqlalchemy.orm import Session
from app.repository.post_repository import PostRepository
from app.schema.post_schema import PostCreate, PostResponse

# 4. Import cho repository
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from app.model.post_model import Post

# 5. Import cho model
from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

# 6. Import cho schema
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
"""
