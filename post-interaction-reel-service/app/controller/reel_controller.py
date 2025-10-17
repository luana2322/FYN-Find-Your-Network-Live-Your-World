from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.service.reel_service import ReelService
from app.schema.reel_schema import ReelCreate, ReelUpdate, ReelResponse, ReelFeedResponse, ReelCommentCreate, ReelCommentResponse
from app.util.s3_helper import S3Helper

router = APIRouter(prefix="/reels", tags=["reels"])

def get_reel_service(db: Session = Depends(get_db)) -> ReelService:
    return ReelService(db)

@router.post("/", response_model=ReelResponse)
async def create_reel(
    video_url: str = Form(...),
    thumbnail_url: Optional[str] = Form(None),
    audio_url: Optional[str] = Form(None),
    duration: int = Form(...),
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Create a new reel"""
    try:
        reel_data = ReelCreate(
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            audio_url=audio_url,
            duration=duration
        )
        return service.create_reel(reel_data, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating reel: {str(e)}"
        )

@router.post("/upload")
async def upload_reel_video(
    file: UploadFile = File(...)
):
    """Upload reel video file"""
    if not file.content_type.startswith('video/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not supported for reels"
        )
    
    s3_helper = S3Helper()
    
    try:
        file_data = await file.read()
        url = s3_helper.upload_file(file_data, file.filename, file.content_type)
        
        return {
            "video_url": url,
            "filename": file.filename,
            "content_type": file.content_type,
            "message": "Video uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading video: {str(e)}"
        )

@router.get("/{reel_id}", response_model=ReelResponse)
async def get_reel(
    reel_id: int,
    service: ReelService = Depends(get_reel_service)
):
    """Get reel by ID"""
    reel = service.get_reel(reel_id)
    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reel not found"
        )
    return reel

@router.get("/user/{user_id}", response_model=ReelFeedResponse)
async def get_user_reels(
    user_id: int,
    page: int = 1,
    size: int = 20,
    service: ReelService = Depends(get_reel_service)
):
    """Get user's reels"""
    return service.get_user_reels(user_id, page, size)

@router.get("/feed", response_model=ReelFeedResponse)
async def get_reel_feed(
    page: int = 1,
    size: int = 20,
    service: ReelService = Depends(get_reel_service)
):
    """Get reel feed"""
    return service.get_reel_feed(page, size)

@router.put("/{reel_id}", response_model=ReelResponse)
async def update_reel(
    reel_id: int,
    reel_update: ReelUpdate,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Update reel"""
    reel = service.update_reel(reel_id, reel_update, user_id)
    if not reel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reel not found or you don't have permission to edit"
        )
    return reel

@router.delete("/{reel_id}")
async def delete_reel(
    reel_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Delete reel"""
    success = service.delete_reel(reel_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reel not found or you don't have permission to delete"
        )
    return {"message": "Reel deleted successfully"}

@router.post("/{reel_id}/like")
async def like_reel(
    reel_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Like a reel"""
    success = service.like_reel(reel_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reel not found or already liked"
        )
    return {"message": "Reel liked successfully"}

@router.delete("/{reel_id}/like")
async def unlike_reel(
    reel_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Unlike a reel"""
    success = service.unlike_reel(reel_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reel not found or not liked"
        )
    return {"message": "Reel unliked successfully"}

@router.post("/{reel_id}/view")
async def view_reel(
    reel_id: int,
    service: ReelService = Depends(get_reel_service)
):
    """Record reel view"""
    success = service.view_reel(reel_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reel not found"
        )
    return {"message": "View recorded successfully"}

@router.post("/comments", response_model=ReelCommentResponse)
async def create_reel_comment(
    comment: ReelCommentCreate,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Create a reel comment"""
    comment_response = service.create_reel_comment(comment, user_id)
    if not comment_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating comment"
        )
    return comment_response

@router.get("/{reel_id}/comments", response_model=List[ReelCommentResponse])
async def get_reel_comments(
    reel_id: int,
    page: int = 1,
    size: int = 20,
    service: ReelService = Depends(get_reel_service)
):
    """Get reel comments"""
    return service.get_reel_comments(reel_id, page, size)

@router.delete("/comments/{comment_id}")
async def delete_reel_comment(
    comment_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: ReelService = Depends(get_reel_service)
):
    """Delete reel comment"""
    success = service.delete_reel_comment(comment_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission to delete"
        )
    return {"message": "Comment deleted successfully"}

