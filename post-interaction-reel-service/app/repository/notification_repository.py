from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from typing import List, Optional
from app.model.notification_model import Notification
from app.schema.notification_schema import MarkAsReadRequest

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(self, user_id: int, actor_id: int, notification_type: str, 
                          message: str, reference_id: Optional[int] = None) -> Notification:
        db_notification = Notification(
            user_id=user_id,
            actor_id=actor_id,
            type=notification_type,
            reference_id=reference_id,
            message=message
        )
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification
    
    def get_user_notifications(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Notification]:
        return self.db.query(Notification).filter(Notification.user_id == user_id).order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    
    def get_unread_count(self, user_id: int) -> int:
        return self.db.query(Notification).filter(
            and_(Notification.user_id == user_id, Notification.is_read == False)
        ).count()
    
    def mark_as_read(self, notification_ids: List[int], user_id: int) -> int:
        updated_count = self.db.query(Notification).filter(
            and_(
                Notification.id.in_(notification_ids),
                Notification.user_id == user_id
            )
        ).update({"is_read": True})
        self.db.commit()
        return updated_count
    
    def mark_all_as_read(self, user_id: int) -> int:
        updated_count = self.db.query(Notification).filter(
            and_(Notification.user_id == user_id, Notification.is_read == False)
        ).update({"is_read": True})
        self.db.commit()
        return updated_count
    
    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        db_notification = self.db.query(Notification).filter(
            and_(Notification.id == notification_id, Notification.user_id == user_id)
        ).first()
        if db_notification:
            self.db.delete(db_notification)
            self.db.commit()
            return True
        return False

