from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    actor_id: int
    type: str
    reference_id: Optional[int]
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    page: int
    size: int
    has_next: bool
    unread_count: int

class MarkAsReadRequest(BaseModel):
    notification_ids: List[int]
