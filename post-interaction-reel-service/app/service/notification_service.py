from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.notification_repository import NotificationRepository
from app.schema.notification_schema import NotificationResponse, NotificationListResponse, MarkAsReadRequest
from app.util.notification_helper import NotificationHelper

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(db)
        self.notification_helper = NotificationHelper()
    
    def create_notification(self, user_id: int, actor_id: int, notification_type: str, 
                           message: str, reference_id: Optional[int] = None) -> NotificationResponse:
        """Create a new notification"""
        db_notification = self.notification_repo.create_notification(
            user_id, actor_id, notification_type, message, reference_id
        )
        
        # Send push notification (async)
        # This would typically be done via Celery task
        # self._send_push_notification(user_id, message)
        
        return NotificationResponse.from_orm(db_notification)
    
    def get_user_notifications(self, user_id: int, page: int = 1, size: int = 20) -> NotificationListResponse:
        """Get user notifications with pagination"""
        skip = (page - 1) * size
        notifications = self.notification_repo.get_user_notifications(user_id, skip, size)
        unread_count = self.notification_repo.get_unread_count(user_id)
        
        notification_responses = [NotificationResponse.from_orm(notif) for notif in notifications]
        
        return NotificationListResponse(
            notifications=notification_responses,
            total=len(notification_responses),
            page=page,
            size=size,
            has_next=len(notification_responses) == size,
            unread_count=unread_count
        )
    
    def mark_as_read(self, notification_ids: List[int], user_id: int) -> int:
        """Mark notifications as read"""
        return self.notification_repo.mark_as_read(notification_ids, user_id)
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read"""
        return self.notification_repo.mark_all_as_read(user_id)
    
    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete notification"""
        return self.notification_repo.delete_notification(notification_id, user_id)
    
    def get_unread_count(self, user_id: int) -> int:
        """Get unread notification count"""
        return self.notification_repo.get_unread_count(user_id)
    
    def send_like_notification(self, post_owner_id: int, actor_id: int, actor_name: str, 
                              post_id: int, post_type: str = "post") -> bool:
        """Send like notification"""
        try:
            message = self.notification_helper.create_notification_message(
                "like", actor_name, post_type
            )
            
            self.create_notification(
                user_id=post_owner_id,
                actor_id=actor_id,
                notification_type="like",
                message=message,
                reference_id=post_id
            )
            
            # Send push notification
            # user_tokens = self._get_user_device_tokens(post_owner_id)
            # self.notification_helper.send_like_notification(
            #     user_tokens, actor_name, post_type, post_id
            # )
            
            return True
        except Exception as e:
            print(f"Error sending like notification: {e}")
            return False
    
    def send_comment_notification(self, post_owner_id: int, actor_id: int, actor_name: str, 
                                 post_id: int, post_type: str = "post") -> bool:
        """Send comment notification"""
        try:
            message = self.notification_helper.create_notification_message(
                "comment", actor_name, post_type
            )
            
            self.create_notification(
                user_id=post_owner_id,
                actor_id=actor_id,
                notification_type="comment",
                message=message,
                reference_id=post_id
            )
            
            # Send push notification
            # user_tokens = self._get_user_device_tokens(post_owner_id)
            # self.notification_helper.send_comment_notification(
            #     user_tokens, actor_name, post_type, post_id
            # )
            
            return True
        except Exception as e:
            print(f"Error sending comment notification: {e}")
            return False
    
    def send_follow_notification(self, user_id: int, actor_id: int, actor_name: str) -> bool:
        """Send follow notification"""
        try:
            message = self.notification_helper.create_notification_message("follow", actor_name)
            
            self.create_notification(
                user_id=user_id,
                actor_id=actor_id,
                notification_type="follow",
                message=message
            )
            
            # Send push notification
            # user_tokens = self._get_user_device_tokens(user_id)
            # self.notification_helper.send_follow_notification(user_tokens, actor_name)
            
            return True
        except Exception as e:
            print(f"Error sending follow notification: {e}")
            return False
