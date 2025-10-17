from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.post_repository import PostRepository
from app.repository.comment_repository import CommentRepository, LikeRepository
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse, PostFeedResponse
from app.schema.comment_schema import CommentCreate, CommentUpdate, CommentResponse, LikeRequest, LikeResponse
from app.util.s3_helper import S3Helper
from app.util.cache_helper import CacheHelper
from app.util.notification_helper import NotificationHelper

class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.post_repo = PostRepository(db)
        self.comment_repo = CommentRepository(db)
        self.like_repo = LikeRepository(db)
        self.s3_helper = S3Helper()
        self.cache_helper = CacheHelper()
        self.notification_helper = NotificationHelper()
    
    def create_post(self, post: PostCreate, user_id: int) -> PostResponse:
        """Create a new post"""
        # Upload media files if provided
        media_urls = []
        if post.media_url:
            for url in post.media_url:
                # Here you would handle file upload from URL or file data
                # For now, we'll assume URLs are already processed
                media_urls.append(url)
        
        # Create post data
        post_data = PostCreate(
            content=post.content,
            media_url=media_urls,
            type=post.type
        )
        
        db_post = self.post_repo.create_post(post_data, user_id)
        
        # Invalidate cache
        self.cache_helper.invalidate_global_feed()
        self.cache_helper.invalidate_user_feed(user_id)
        
        return PostResponse.from_orm(db_post)
    
    def get_post(self, post_id: int) -> Optional[PostResponse]:
        """Get post by ID"""
        db_post = self.post_repo.get_post_by_id(post_id)
        if db_post:
            return PostResponse.from_orm(db_post)
        return None
    
    def get_user_posts(self, user_id: int, page: int = 1, size: int = 20) -> PostFeedResponse:
        """Get user's posts with pagination"""
        skip = (page - 1) * size
        
        # Try cache first
        cache_key = f"user_posts:{user_id}:{page}:{size}"
        cached_posts = self.cache_helper.get_cache(cache_key)
        if cached_posts:
            return PostFeedResponse(**cached_posts)
        
        posts = self.post_repo.get_user_posts(user_id, skip, size)
        post_responses = [PostResponse.from_orm(post) for post in posts]
        
        # Cache the result
        response_data = {
            "posts": [post.dict() for post in post_responses],
            "total": len(post_responses),
            "page": page,
            "size": size,
            "has_next": len(post_responses) == size
        }
        self.cache_helper.set_cache(cache_key, response_data, ttl=300)  # 5 minutes
        
        return PostFeedResponse(**response_data)
    
    def get_feed(self, user_id: int, following_ids: List[int], page: int = 1, size: int = 20) -> PostFeedResponse:
        """Get personalized feed for user"""
        skip = (page - 1) * size
        
        # Try cache first
        cache_key = f"user_feed:{user_id}:{page}:{size}"
        cached_feed = self.cache_helper.get_user_feed(cache_key)
        if cached_feed:
            return PostFeedResponse(**cached_feed)
        
        if following_ids:
            posts = self.post_repo.get_feed_posts(following_ids, skip, size)
        else:
            posts = self.post_repo.get_global_feed(skip, size)
        
        post_responses = [PostResponse.from_orm(post) for post in posts]
        
        # Cache the result
        response_data = {
            "posts": [post.dict() for post in post_responses],
            "total": len(post_responses),
            "page": page,
            "size": size,
            "has_next": len(post_responses) == size
        }
        self.cache_helper.cache_user_feed(cache_key, response_data)
        
        return PostFeedResponse(**response_data)
    
    def get_global_feed(self, page: int = 1, size: int = 20) -> PostFeedResponse:
        """Get global feed"""
        skip = (page - 1) * size
        
        # Try cache first
        cache_key = f"global_feed:{page}:{size}"
        cached_feed = self.cache_helper.get_global_feed()
        if cached_feed and page == 1:
            return PostFeedResponse(**cached_feed)
        
        posts = self.post_repo.get_global_feed(skip, size)
        post_responses = [PostResponse.from_orm(post) for post in posts]
        
        # Cache the result
        response_data = {
            "posts": [post.dict() for post in post_responses],
            "total": len(post_responses),
            "page": page,
            "size": size,
            "has_next": len(post_responses) == size
        }
        
        if page == 1:
            self.cache_helper.cache_global_feed(response_data)
        
        return PostFeedResponse(**response_data)
    
    def update_post(self, post_id: int, post_update: PostUpdate, user_id: int) -> Optional[PostResponse]:
        """Update post"""
        db_post = self.post_repo.update_post(post_id, post_update, user_id)
        if db_post:
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
            self.cache_helper.invalidate_user_feed(user_id)
            return PostResponse.from_orm(db_post)
        return None
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        """Delete post"""
        success = self.post_repo.delete_post(post_id, user_id)
        if success:
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
            self.cache_helper.invalidate_user_feed(user_id)
        return success
    
    def like_post(self, post_id: int, user_id: int) -> bool:
        """Like a post"""
        # Check if already liked
        if self.like_repo.is_liked(user_id, post_id=post_id):
            return False
        
        # Create like
        success = self.like_repo.create_like(user_id, post_id=post_id)
        if success:
            # Update like count
            self.post_repo.increment_like_count(post_id)
            
            # Send notification (async)
            # This would typically be done via Celery task
            # self._send_like_notification(post_id, user_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
        
        return success
    
    def unlike_post(self, post_id: int, user_id: int) -> bool:
        """Unlike a post"""
        success = self.like_repo.remove_like(user_id, post_id=post_id)
        if success:
            # Update like count
            self.post_repo.decrement_like_count(post_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
        
        return success
    
    def create_comment(self, comment: CommentCreate, user_id: int) -> Optional[CommentResponse]:
        """Create a comment"""
        db_comment = self.comment_repo.create_comment(comment, user_id)
        if db_comment:
            # Update comment count
            self.post_repo.increment_comment_count(comment.post_id)
            
            # Send notification (async)
            # self._send_comment_notification(comment.post_id, user_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
            
            return CommentResponse.from_orm(db_comment)
        return None
    
    def get_post_comments(self, post_id: int, page: int = 1, size: int = 20) -> List[CommentResponse]:
        """Get post comments"""
        skip = (page - 1) * size
        comments = self.comment_repo.get_post_comments(post_id, skip, size)
        return [CommentResponse.from_orm(comment) for comment in comments]
    
    def update_comment(self, comment_id: int, comment_update: CommentUpdate, user_id: int) -> Optional[CommentResponse]:
        """Update comment"""
        db_comment = self.comment_repo.update_comment(comment_id, comment_update, user_id)
        if db_comment:
            return CommentResponse.from_orm(db_comment)
        return None
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        """Delete comment"""
        # Get comment to find post_id
        comment = self.comment_repo.get_comment_by_id(comment_id)
        if not comment:
            return False
        
        success = self.comment_repo.delete_comment(comment_id, user_id)
        if success:
            # Update comment count
            self.post_repo.decrement_comment_count(comment.post_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_global_feed()
        
        return success

