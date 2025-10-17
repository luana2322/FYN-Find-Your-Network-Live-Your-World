from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.service.post_service import PostService
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse, PostFeedResponse
from app.schema.comment_schema import CommentCreate, CommentUpdate, CommentResponse, LikeRequest
from app.util.s3_helper import S3Helper

router = APIRouter(prefix="/posts", tags=["posts"])

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(db)

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    user_id: int = 1,  # This would come from JWT token in real implementation
    service: PostService = Depends(get_post_service)
):
    """Create a new post"""
    try:
        return service.create_post(post, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating post: {str(e)}"
        )

@router.post("/upload")
async def upload_post_media(
    files: List[UploadFile] = File(...),
    content: Optional[str] = Form(None)
):
    """Upload media files for post"""
    s3_helper = S3Helper()
    uploaded_urls = []
    
    for file in files:
        if not file.content_type.startswith(('image/', 'video/')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} not supported"
            )
        
        try:
            file_data = await file.read()
            url = s3_helper.upload_file(file_data, file.filename, file.content_type)
            uploaded_urls.append(url)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading file {file.filename}: {str(e)}"
            )
    
    return {
        "media_urls": uploaded_urls,
        "content": content,
        "message": "Files uploaded successfully"
    }

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    service: PostService = Depends(get_post_service)
):
    """Get post by ID"""
    post = service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.get("/user/{user_id}", response_model=PostFeedResponse)
async def get_user_posts(
    user_id: int,
    page: int = 1,
    size: int = 20,
    service: PostService = Depends(get_post_service)
):
    """Get user's posts"""
    return service.get_user_posts(user_id, page, size)

@router.get("/feed/personal", response_model=PostFeedResponse)
async def get_personal_feed(
    user_id: int = 1,  # This would come from JWT token
    following_ids: List[int] = [],  # This would come from follow service
    page: int = 1,
    size: int = 20,
    service: PostService = Depends(get_post_service)
):
    """Get personalized feed"""
    return service.get_feed(user_id, following_ids, page, size)

@router.get("/feed/global", response_model=PostFeedResponse)
async def get_global_feed(
    page: int = 1,
    size: int = 20,
    service: PostService = Depends(get_post_service)
):
    """Get global feed"""
    return service.get_global_feed(page, size)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Update post"""
    post = service.update_post(post_id, post_update, user_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to edit"
        )
    return post

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Delete post"""
    success = service.delete_post(post_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to delete"
        )
    return {"message": "Post deleted successfully"}

@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Like a post"""
    success = service.like_post(post_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found or already liked"
        )
    return {"message": "Post liked successfully"}

@router.delete("/{post_id}/like")
async def unlike_post(
    post_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Unlike a post"""
    success = service.unlike_post(post_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found or not liked"
        )
    return {"message": "Post unliked successfully"}

@router.post("/comments", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Create a comment"""
    comment_response = service.create_comment(comment, user_id)
    if not comment_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating comment"
        )
    return comment_response

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int,
    page: int = 1,
    size: int = 20,
    service: PostService = Depends(get_post_service)
):
    """Get post comments"""
    return service.get_post_comments(post_id, page, size)

@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Update comment"""
    comment = service.update_comment(comment_id, comment_update, user_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission to edit"
        )
    return comment

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: int = 1,  # This would come from JWT token
    service: PostService = Depends(get_post_service)
):
    """Delete comment"""
    success = service.delete_comment(comment_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission to delete"
        )
    return {"message": "Comment deleted successfully"}

