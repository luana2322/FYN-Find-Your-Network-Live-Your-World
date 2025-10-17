from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.service.notification_service import NotificationService
from app.schema.notification_schema import NotificationResponse, NotificationListResponse, MarkAsReadRequest

router = APIRouter(prefix="/notifications", tags=["notifications"])

def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    user_id: int = 1,  # This would come from JWT token
    page: int = 1,
    size: int = 20,
    service: NotificationService = Depends(get_notification_service)
):
    """Get user notifications"""
    return service.get_user_notifications(user_id, page, size)

@router.get("/unread-count")
async def get_unread_count(
    user_id: int = 1,  # This would come from JWT token
    service: NotificationService = Depends(get_notification_service)
):
    """Get unread notification count"""
    count = service.get_unread_count(user_id)
    return {"unread_count": count}

@router.patch("/mark-read")
async def mark_notifications_as_read(
    request: MarkAsReadRequest,
    user_id: int = 1,  # This would come from JWT token
    service: NotificationService = Depends(get_notification_service)
):
    """Mark specific notifications as read"""
    updated_count = service.mark_as_read(request.notification_ids, user_id)
    return {
        "message": f"Marked {updated_count} notifications as read",
        "updated_count": updated_count
    }

@router.patch("/mark-all-read")
async def mark_all_notifications_as_read(
    user_id: int = 1,  # This would come from JWT token
    service: NotificationService = Depends(get_notification_service)
):
    """Mark all notifications as read"""
    updated_count = service.mark_all_as_read(user_id)
    return {
        "message": f"Marked {updated_count} notifications as read",
        "updated_count": updated_count
    }

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: NotificationService = Depends(get_notification_service)
):
    """Delete notification"""
    success = service.delete_notification(notification_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found or you don't have permission to delete"
        )
    return {"message": "Notification deleted successfully"}

@router.post("/test-like")
async def test_like_notification(
    post_owner_id: int,
    actor_id: int = 1,
    actor_name: str = "Test User",
    post_id: int = 1,
    post_type: str = "post",
    service: NotificationService = Depends(get_notification_service)
):
    """Test like notification (for development)"""
    success = service.send_like_notification(
        post_owner_id, actor_id, actor_name, post_id, post_type
    )
    if success:
        return {"message": "Like notification sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send like notification"
        )

@router.post("/test-comment")
async def test_comment_notification(
    post_owner_id: int,
    actor_id: int = 1,
    actor_name: str = "Test User",
    post_id: int = 1,
    post_type: str = "post",
    service: NotificationService = Depends(get_notification_service)
):
    """Test comment notification (for development)"""
    success = service.send_comment_notification(
        post_owner_id, actor_id, actor_name, post_id, post_type
    )
    if success:
        return {"message": "Comment notification sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send comment notification"
        )

@router.post("/test-follow")
async def test_follow_notification(
    user_id: int,
    actor_id: int = 1,
    actor_name: str = "Test User",
    service: NotificationService = Depends(get_notification_service)
):
    """Test follow notification (for development)"""
    success = service.send_follow_notification(user_id, actor_id, actor_name)
    if success:
        return {"message": "Follow notification sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send follow notification"
        )

