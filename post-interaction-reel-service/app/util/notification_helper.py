import firebase_admin
from firebase_admin import credentials, messaging
from typing import List, Optional
import json
import os
from app.config.settings import settings

class NotificationHelper:
    def __init__(self):
        self.app = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                self.app = firebase_admin.initialize_app(cred)
            else:
                print("Firebase credentials not found. Push notifications will be disabled.")
        except Exception as e:
            print(f"Firebase initialization error: {e}")
    
    def send_notification(self, user_tokens: List[str], title: str, body: str, 
                         data: Optional[dict] = None) -> bool:
        """Send push notification to user devices"""
        if not self.app or not user_tokens:
            return False
        
        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=user_tokens
            )
            
            response = messaging.send_multicast(message)
            print(f"Successfully sent message: {response.success_count} successful, {response.failure_count} failed")
            return response.success_count > 0
            
        except Exception as e:
            print(f"Push notification error: {e}")
            return False
    
    def send_like_notification(self, user_tokens: List[str], actor_name: str, 
                              post_type: str, reference_id: int) -> bool:
        """Send like notification"""
        title = "New Like!"
        body = f"{actor_name} liked your {post_type}"
        data = {
            "type": "like",
            "reference_id": str(reference_id),
            "post_type": post_type
        }
        return self.send_notification(user_tokens, title, body, data)
    
    def send_comment_notification(self, user_tokens: List[str], actor_name: str, 
                                 post_type: str, reference_id: int) -> bool:
        """Send comment notification"""
        title = "New Comment!"
        body = f"{actor_name} commented on your {post_type}"
        data = {
            "type": "comment",
            "reference_id": str(reference_id),
            "post_type": post_type
        }
        return self.send_notification(user_tokens, title, body, data)
    
    def send_follow_notification(self, user_tokens: List[str], actor_name: str) -> bool:
        """Send follow notification"""
        title = "New Follower!"
        body = f"{actor_name} started following you"
        data = {
            "type": "follow"
        }
        return self.send_notification(user_tokens, title, body, data)
    
    def create_notification_message(self, notification_type: str, actor_name: str, 
                                   post_type: str = None, reference_id: int = None) -> str:
        """Create notification message based on type"""
        messages = {
            "like": f"{actor_name} liked your {post_type}",
            "comment": f"{actor_name} commented on your {post_type}",
            "follow": f"{actor_name} started following you",
            "mention": f"{actor_name} mentioned you in a {post_type}",
            "share": f"{actor_name} shared your {post_type}"
        }
        return messages.get(notification_type, f"{actor_name} interacted with your content")
