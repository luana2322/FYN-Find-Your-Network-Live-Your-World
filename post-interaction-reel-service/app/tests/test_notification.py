import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.service.notification_service import NotificationService
from app.schema.notification_schema import MarkAsReadRequest

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def notification_service(mock_db):
    return NotificationService(mock_db)

def test_create_notification(notification_service, mock_db):
    """Test creating a notification"""
    user_id = 1
    actor_id = 2
    notification_type = "like"
    message = "User liked your post"
    reference_id = 123
    
    mock_notification = Mock()
    mock_notification.id = 1
    mock_notification.user_id = user_id
    mock_notification.actor_id = actor_id
    mock_notification.type = notification_type
    mock_notification.message = message
    mock_notification.reference_id = reference_id
    mock_notification.is_read = False
    
    with patch.object(notification_service.notification_repo, 'create_notification', 
                      return_value=mock_notification):
        result = notification_service.create_notification(
            user_id, actor_id, notification_type, message, reference_id
        )
        
        assert result is not None
        assert result.user_id == user_id
        assert result.actor_id == actor_id
        assert result.type == notification_type
        assert result.message == message

def test_get_user_notifications(notification_service, mock_db):
    """Test getting user notifications"""
    user_id = 1
    page = 1
    size = 20
    
    mock_notifications = []
    for i in range(3):
        mock_notification = Mock()
        mock_notification.id = i + 1
        mock_notification.user_id = user_id
        mock_notification.actor_id = 2
        mock_notification.type = "like"
        mock_notification.message = f"Notification {i + 1}"
        mock_notification.is_read = False
        mock_notifications.append(mock_notification)
    
    with patch.object(notification_service.notification_repo, 'get_user_notifications', 
                      return_value=mock_notifications), \
         patch.object(notification_service.notification_repo, 'get_unread_count', 
                      return_value=2):
        
        result = notification_service.get_user_notifications(user_id, page, size)
        
        assert result is not None
        assert len(result.notifications) == 3
        assert result.total == 3
        assert result.page == page
        assert result.size == size
        assert result.unread_count == 2

def test_mark_as_read(notification_service, mock_db):
    """Test marking notifications as read"""
    notification_ids = [1, 2, 3]
    user_id = 1
    
    with patch.object(notification_service.notification_repo, 'mark_as_read', 
                      return_value=3):
        result = notification_service.mark_as_read(notification_ids, user_id)
        
        assert result == 3

def test_mark_all_as_read(notification_service, mock_db):
    """Test marking all notifications as read"""
    user_id = 1
    
    with patch.object(notification_service.notification_repo, 'mark_all_as_read', 
                      return_value=5):
        result = notification_service.mark_all_as_read(user_id)
        
        assert result == 5

def test_delete_notification(notification_service, mock_db):
    """Test deleting a notification"""
    notification_id = 1
    user_id = 1
    
    with patch.object(notification_service.notification_repo, 'delete_notification', 
                      return_value=True):
        result = notification_service.delete_notification(notification_id, user_id)
        
        assert result is True

def test_get_unread_count(notification_service, mock_db):
    """Test getting unread notification count"""
    user_id = 1
    
    with patch.object(notification_service.notification_repo, 'get_unread_count', 
                      return_value=3):
        result = notification_service.get_unread_count(user_id)
        
        assert result == 3

def test_send_like_notification(notification_service, mock_db):
    """Test sending like notification"""
    post_owner_id = 1
    actor_id = 2
    actor_name = "Test User"
    post_id = 123
    post_type = "post"
    
    mock_notification = Mock()
    mock_notification.id = 1
    mock_notification.user_id = post_owner_id
    mock_notification.actor_id = actor_id
    mock_notification.type = "like"
    mock_notification.message = f"{actor_name} liked your {post_type}"
    mock_notification.reference_id = post_id
    mock_notification.is_read = False
    
    with patch.object(notification_service, 'create_notification', 
                      return_value=mock_notification):
        result = notification_service.send_like_notification(
            post_owner_id, actor_id, actor_name, post_id, post_type
        )
        
        assert result is True

def test_send_comment_notification(notification_service, mock_db):
    """Test sending comment notification"""
    post_owner_id = 1
    actor_id = 2
    actor_name = "Test User"
    post_id = 123
    post_type = "post"
    
    mock_notification = Mock()
    mock_notification.id = 1
    mock_notification.user_id = post_owner_id
    mock_notification.actor_id = actor_id
    mock_notification.type = "comment"
    mock_notification.message = f"{actor_name} commented on your {post_type}"
    mock_notification.reference_id = post_id
    mock_notification.is_read = False
    
    with patch.object(notification_service, 'create_notification', 
                      return_value=mock_notification):
        result = notification_service.send_comment_notification(
            post_owner_id, actor_id, actor_name, post_id, post_type
        )
        
        assert result is True

def test_send_follow_notification(notification_service, mock_db):
    """Test sending follow notification"""
    user_id = 1
    actor_id = 2
    actor_name = "Test User"
    
    mock_notification = Mock()
    mock_notification.id = 1
    mock_notification.user_id = user_id
    mock_notification.actor_id = actor_id
    mock_notification.type = "follow"
    mock_notification.message = f"{actor_name} started following you"
    mock_notification.is_read = False
    
    with patch.object(notification_service, 'create_notification', 
                      return_value=mock_notification):
        result = notification_service.send_follow_notification(
            user_id, actor_id, actor_name
        )
        
        assert result is True

def test_send_notification_error_handling(notification_service, mock_db):
    """Test error handling in notification sending"""
    post_owner_id = 1
    actor_id = 2
    actor_name = "Test User"
    post_id = 123
    post_type = "post"
    
    with patch.object(notification_service, 'create_notification', 
                      side_effect=Exception("Database error")):
        result = notification_service.send_like_notification(
            post_owner_id, actor_id, actor_name, post_id, post_type
        )
        
        assert result is False




