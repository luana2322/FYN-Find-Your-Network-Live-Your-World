import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.service.post_service import PostService
from app.schema.post_schema import PostCreate, PostUpdate
from app.repository.post_repository import PostRepository

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def post_service(mock_db):
    return PostService(mock_db)

def test_create_post(post_service, mock_db):
    """Test creating a post"""
    post_data = PostCreate(
        content="Test post content",
        type="text"
    )
    user_id = 1
    
    # Mock the repository method
    mock_post = Mock()
    mock_post.id = 1
    mock_post.user_id = user_id
    mock_post.content = post_data.content
    mock_post.type = post_data.type
    mock_post.like_count = 0
    mock_post.comment_count = 0
    
    with patch.object(post_service.post_repo, 'create_post', return_value=mock_post):
        result = post_service.create_post(post_data, user_id)
        
        assert result.user_id == user_id
        assert result.content == post_data.content
        assert result.type == post_data.type

def test_get_post(post_service, mock_db):
    """Test getting a post"""
    post_id = 1
    
    mock_post = Mock()
    mock_post.id = post_id
    mock_post.user_id = 1
    mock_post.content = "Test content"
    mock_post.type = "text"
    mock_post.like_count = 0
    mock_post.comment_count = 0
    
    with patch.object(post_service.post_repo, 'get_post_by_id', return_value=mock_post):
        result = post_service.get_post(post_id)
        
        assert result is not None
        assert result.id == post_id

def test_get_post_not_found(post_service, mock_db):
    """Test getting a non-existent post"""
    post_id = 999
    
    with patch.object(post_service.post_repo, 'get_post_by_id', return_value=None):
        result = post_service.get_post(post_id)
        
        assert result is None

def test_like_post(post_service, mock_db):
    """Test liking a post"""
    post_id = 1
    user_id = 1
    
    with patch.object(post_service.like_repo, 'is_liked', return_value=False), \
         patch.object(post_service.like_repo, 'create_like', return_value=True), \
         patch.object(post_service.post_repo, 'increment_like_count'):
        
        result = post_service.like_post(post_id, user_id)
        
        assert result is True

def test_like_post_already_liked(post_service, mock_db):
    """Test liking an already liked post"""
    post_id = 1
    user_id = 1
    
    with patch.object(post_service.like_repo, 'is_liked', return_value=True):
        result = post_service.like_post(post_id, user_id)
        
        assert result is False

def test_unlike_post(post_service, mock_db):
    """Test unliking a post"""
    post_id = 1
    user_id = 1
    
    with patch.object(post_service.like_repo, 'remove_like', return_value=True), \
         patch.object(post_service.post_repo, 'decrement_like_count'):
        
        result = post_service.unlike_post(post_id, user_id)
        
        assert result is True

def test_create_comment(post_service, mock_db):
    """Test creating a comment"""
    from app.schema.comment_schema import CommentCreate
    
    comment_data = CommentCreate(
        post_id=1,
        content="Test comment"
    )
    user_id = 1
    
    mock_comment = Mock()
    mock_comment.id = 1
    mock_comment.post_id = comment_data.post_id
    mock_comment.user_id = user_id
    mock_comment.content = comment_data.content
    
    with patch.object(post_service.comment_repo, 'create_comment', return_value=mock_comment), \
         patch.object(post_service.post_repo, 'increment_comment_count'):
        
        result = post_service.create_comment(comment_data, user_id)
        
        assert result is not None
        assert result.content == comment_data.content
        assert result.post_id == comment_data.post_id

def test_update_post(post_service, mock_db):
    """Test updating a post"""
    post_id = 1
    user_id = 1
    
    post_update = PostUpdate(content="Updated content")
    
    mock_post = Mock()
    mock_post.id = post_id
    mock_post.user_id = user_id
    mock_post.content = post_update.content
    mock_post.type = "text"
    mock_post.like_count = 0
    mock_post.comment_count = 0
    
    with patch.object(post_service.post_repo, 'update_post', return_value=mock_post):
        result = post_service.update_post(post_id, post_update, user_id)
        
        assert result is not None
        assert result.content == post_update.content

def test_delete_post(post_service, mock_db):
    """Test deleting a post"""
    post_id = 1
    user_id = 1
    
    with patch.object(post_service.post_repo, 'delete_post', return_value=True):
        result = post_service.delete_post(post_id, user_id)
        
        assert result is True

def test_delete_post_not_found(post_service, mock_db):
    """Test deleting a non-existent post"""
    post_id = 999
    user_id = 1
    
    with patch.object(post_service.post_repo, 'delete_post', return_value=False):
        result = post_service.delete_post(post_id, user_id)
        
        assert result is False




