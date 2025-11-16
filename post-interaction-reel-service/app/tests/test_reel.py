import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.service.reel_service import ReelService
from app.schema.reel_schema import ReelCreate, ReelUpdate

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def reel_service(mock_db):
    return ReelService(mock_db)

def test_create_reel(reel_service, mock_db):
    """Test creating a reel"""
    reel_data = ReelCreate(
        video_url="https://example.com/video.mp4",
        duration=30
    )
    user_id = 1
    
    # Mock FFmpeg processing
    mock_video_url = "https://processed.com/video.mp4"
    mock_thumbnail_url = "https://processed.com/thumbnail.jpg"
    mock_audio_url = "https://processed.com/audio.mp3"
    mock_video_info = {"duration": 30, "width": 720, "height": 1280}
    
    mock_reel = Mock()
    mock_reel.id = 1
    mock_reel.user_id = user_id
    mock_reel.video_url = mock_video_url
    mock_reel.thumbnail_url = mock_thumbnail_url
    mock_reel.audio_url = mock_audio_url
    mock_reel.duration = 30
    mock_reel.view_count = 0
    mock_reel.like_count = 0
    mock_reel.comment_count = 0
    
    with patch.object(reel_service.ffmpeg_worker, 'process_reel_video', 
                      return_value=(mock_video_url, mock_thumbnail_url, mock_audio_url, mock_video_info)), \
         patch.object(reel_service.reel_repo, 'create_reel', return_value=mock_reel):
        
        result = reel_service.create_reel(reel_data, user_id)
        
        assert result is not None
        assert result.user_id == user_id
        assert result.video_url == mock_video_url
        assert result.duration == 30

def test_create_reel_processing_failed(reel_service, mock_db):
    """Test creating a reel when FFmpeg processing fails"""
    reel_data = ReelCreate(
        video_url="https://example.com/video.mp4",
        duration=30
    )
    user_id = 1
    
    with patch.object(reel_service.ffmpeg_worker, 'process_reel_video', 
                      return_value=(None, None, None, {})):
        
        result = reel_service.create_reel(reel_data, user_id)
        
        assert result is None

def test_get_reel(reel_service, mock_db):
    """Test getting a reel"""
    reel_id = 1
    
    mock_reel = Mock()
    mock_reel.id = reel_id
    mock_reel.user_id = 1
    mock_reel.video_url = "https://example.com/video.mp4"
    mock_reel.duration = 30
    mock_reel.view_count = 0
    mock_reel.like_count = 0
    mock_reel.comment_count = 0
    
    with patch.object(reel_service.reel_repo, 'get_reel_by_id', return_value=mock_reel):
        result = reel_service.get_reel(reel_id)
        
        assert result is not None
        assert result.id == reel_id

def test_get_reel_not_found(reel_service, mock_db):
    """Test getting a non-existent reel"""
    reel_id = 999
    
    with patch.object(reel_service.reel_repo, 'get_reel_by_id', return_value=None):
        result = reel_service.get_reel(reel_id)
        
        assert result is None

def test_like_reel(reel_service, mock_db):
    """Test liking a reel"""
    reel_id = 1
    user_id = 1
    
    with patch.object(reel_service.like_repo, 'is_liked', return_value=False), \
         patch.object(reel_service.like_repo, 'create_like', return_value=True), \
         patch.object(reel_service.reel_repo, 'increment_like_count'):
        
        result = reel_service.like_reel(reel_id, user_id)
        
        assert result is True

def test_like_reel_already_liked(reel_service, mock_db):
    """Test liking an already liked reel"""
    reel_id = 1
    user_id = 1
    
    with patch.object(reel_service.like_repo, 'is_liked', return_value=True):
        result = reel_service.like_reel(reel_id, user_id)
        
        assert result is False

def test_unlike_reel(reel_service, mock_db):
    """Test unliking a reel"""
    reel_id = 1
    user_id = 1
    
    with patch.object(reel_service.like_repo, 'remove_like', return_value=True), \
         patch.object(reel_service.reel_repo, 'decrement_like_count'):
        
        result = reel_service.unlike_reel(reel_id, user_id)
        
        assert result is True

def test_view_reel(reel_service, mock_db):
    """Test recording a reel view"""
    reel_id = 1
    
    with patch.object(reel_service.reel_repo, 'increment_view_count'):
        result = reel_service.view_reel(reel_id)
        
        assert result is True

def test_create_reel_comment(reel_service, mock_db):
    """Test creating a reel comment"""
    from app.schema.reel_schema import ReelCommentCreate
    
    comment_data = ReelCommentCreate(
        reel_id=1,
        content="Test reel comment"
    )
    user_id = 1
    
    mock_comment = Mock()
    mock_comment.id = 1
    mock_comment.reel_id = comment_data.reel_id
    mock_comment.user_id = user_id
    mock_comment.content = comment_data.content
    
    with patch.object(reel_service.reel_comment_repo, 'create_comment', return_value=mock_comment), \
         patch.object(reel_service.reel_repo, 'increment_comment_count'):
        
        result = reel_service.create_reel_comment(comment_data, user_id)
        
        assert result is not None
        assert result.content == comment_data.content
        assert result.reel_id == comment_data.reel_id

def test_get_reel_feed(reel_service, mock_db):
    """Test getting reel feed"""
    page = 1
    size = 20
    
    mock_reels = []
    for i in range(5):
        mock_reel = Mock()
        mock_reel.id = i + 1
        mock_reel.user_id = 1
        mock_reel.video_url = f"https://example.com/video{i}.mp4"
        mock_reel.duration = 30
        mock_reel.view_count = 0
        mock_reel.like_count = 0
        mock_reel.comment_count = 0
        mock_reels.append(mock_reel)
    
    with patch.object(reel_service.reel_repo, 'get_reel_feed', return_value=mock_reels):
        result = reel_service.get_reel_feed(page, size)
        
        assert result is not None
        assert len(result.reels) == 5
        assert result.total == 5
        assert result.page == page
        assert result.size == size

def test_update_reel(reel_service, mock_db):
    """Test updating a reel"""
    reel_id = 1
    user_id = 1
    
    reel_update = ReelUpdate(thumbnail_url="https://example.com/new_thumbnail.jpg")
    
    mock_reel = Mock()
    mock_reel.id = reel_id
    mock_reel.user_id = user_id
    mock_reel.video_url = "https://example.com/video.mp4"
    mock_reel.thumbnail_url = reel_update.thumbnail_url
    mock_reel.duration = 30
    mock_reel.view_count = 0
    mock_reel.like_count = 0
    mock_reel.comment_count = 0
    
    with patch.object(reel_service.reel_repo, 'update_reel', return_value=mock_reel):
        result = reel_service.update_reel(reel_id, reel_update, user_id)
        
        assert result is not None
        assert result.thumbnail_url == reel_update.thumbnail_url

def test_delete_reel(reel_service, mock_db):
    """Test deleting a reel"""
    reel_id = 1
    user_id = 1
    
    with patch.object(reel_service.reel_repo, 'delete_reel', return_value=True):
        result = reel_service.delete_reel(reel_id, user_id)
        
        assert result is True




