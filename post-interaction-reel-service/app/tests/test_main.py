import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.database import Base, get_db
from app.config.settings import settings

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Post, Interaction & Reel Service API"
    assert data["version"] == "1.0.0"

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_post(client):
    """Test creating a post"""
    post_data = {
        "content": "Test post content",
        "type": "text"
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test post content"
    assert data["type"] == "text"
    assert data["user_id"] == 1

def test_get_post(client):
    """Test getting a post"""
    # First create a post
    post_data = {
        "content": "Test post for retrieval",
        "type": "text"
    }
    create_response = client.post("/posts/", json=post_data)
    post_id = create_response.json()["id"]
    
    # Then get the post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["content"] == "Test post for retrieval"

def test_get_global_feed(client):
    """Test getting global feed"""
    response = client.get("/posts/feed/global")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_like_post(client):
    """Test liking a post"""
    # First create a post
    post_data = {
        "content": "Test post for liking",
        "type": "text"
    }
    create_response = client.post("/posts/", json=post_data)
    post_id = create_response.json()["id"]
    
    # Like the post
    response = client.post(f"/posts/{post_id}/like")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Post liked successfully"

def test_create_comment(client):
    """Test creating a comment"""
    # First create a post
    post_data = {
        "content": "Test post for commenting",
        "type": "text"
    }
    create_response = client.post("/posts/", json=post_data)
    post_id = create_response.json()["id"]
    
    # Create a comment
    comment_data = {
        "post_id": post_id,
        "content": "Test comment"
    }
    response = client.post("/posts/comments", json=comment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test comment"
    assert data["post_id"] == post_id

def test_get_reel_feed(client):
    """Test getting reel feed"""
    response = client.get("/reels/feed")
    assert response.status_code == 200
    data = response.json()
    assert "reels" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_get_notifications(client):
    """Test getting notifications"""
    response = client.get("/notifications/")
    assert response.status_code == 200
    data = response.json()
    assert "notifications" in data
    assert "total" in data
    assert "unread_count" in data

def test_get_unread_count(client):
    """Test getting unread notification count"""
    response = client.get("/notifications/unread-count")
    assert response.status_code == 200
    data = response.json()
    assert "unread_count" in data
    assert isinstance(data["unread_count"], int)

