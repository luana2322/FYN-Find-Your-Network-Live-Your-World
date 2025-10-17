from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.reel_repository import ReelRepository, ReelCommentRepository
from app.repository.comment_repository import LikeRepository
from app.schema.reel_schema import ReelCreate, ReelUpdate, ReelResponse, ReelFeedResponse, ReelCommentCreate, ReelCommentResponse
from app.util.s3_helper import S3Helper
from app.util.ffmpeg_worker import FFmpegWorker
from app.util.cache_helper import CacheHelper
from app.util.notification_helper import NotificationHelper

class ReelService:
    def __init__(self, db: Session):
        self.db = db
        self.reel_repo = ReelRepository(db)
        self.reel_comment_repo = ReelCommentRepository(db)
        self.like_repo = LikeRepository(db)
        self.s3_helper = S3Helper()
        self.ffmpeg_worker = FFmpegWorker()
        self.cache_helper = CacheHelper()
        self.notification_helper = NotificationHelper()
    
    def create_reel(self, reel: ReelCreate, user_id: int) -> Optional[ReelResponse]:
        """Create a new reel"""
        # Process video with FFmpeg
        video_url, thumbnail_url, audio_url, video_info = self.ffmpeg_worker.process_reel_video(reel.video_url)
        
        if not video_url:
            return None
        
        # Create reel data
        reel_data = ReelCreate(
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            audio_url=audio_url,
            duration=int(video_info.get('duration', 0))
        )
        
        db_reel = self.reel_repo.create_reel(reel_data, user_id)
        
        # Invalidate cache
        self.cache_helper.invalidate_reel_feed()
        
        return ReelResponse.from_orm(db_reel)
    
    def get_reel(self, reel_id: int) -> Optional[ReelResponse]:
        """Get reel by ID"""
        db_reel = self.reel_repo.get_reel_by_id(reel_id)
        if db_reel:
            return ReelResponse.from_orm(db_reel)
        return None
    
    def get_user_reels(self, user_id: int, page: int = 1, size: int = 20) -> ReelFeedResponse:
        """Get user's reels with pagination"""
        skip = (page - 1) * size
        
        # Try cache first
        cache_key = f"user_reels:{user_id}:{page}:{size}"
        cached_reels = self.cache_helper.get_cache(cache_key)
        if cached_reels:
            return ReelFeedResponse(**cached_reels)
        
        reels = self.reel_repo.get_user_reels(user_id, skip, size)
        reel_responses = [ReelResponse.from_orm(reel) for reel in reels]
        
        # Cache the result
        response_data = {
            "reels": [reel.dict() for reel in reel_responses],
            "total": len(reel_responses),
            "page": page,
            "size": size,
            "has_next": len(reel_responses) == size
        }
        self.cache_helper.set_cache(cache_key, response_data, ttl=300)  # 5 minutes
        
        return ReelFeedResponse(**response_data)
    
    def get_reel_feed(self, page: int = 1, size: int = 20) -> ReelFeedResponse:
        """Get reel feed"""
        skip = (page - 1) * size
        
        # Try cache first
        cache_key = f"reel_feed:{page}:{size}"
        cached_feed = self.cache_helper.get_reel_feed()
        if cached_feed and page == 1:
            return ReelFeedResponse(**cached_feed)
        
        reels = self.reel_repo.get_reel_feed(skip, size)
        reel_responses = [ReelResponse.from_orm(reel) for reel in reels]
        
        # Cache the result
        response_data = {
            "reels": [reel.dict() for reel in reel_responses],
            "total": len(reel_responses),
            "page": page,
            "size": size,
            "has_next": len(reel_responses) == size
        }
        
        if page == 1:
            self.cache_helper.cache_reel_feed(response_data)
        
        return ReelFeedResponse(**response_data)
    
    def update_reel(self, reel_id: int, reel_update: ReelUpdate, user_id: int) -> Optional[ReelResponse]:
        """Update reel"""
        db_reel = self.reel_repo.update_reel(reel_id, reel_update, user_id)
        if db_reel:
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
            return ReelResponse.from_orm(db_reel)
        return None
    
    def delete_reel(self, reel_id: int, user_id: int) -> bool:
        """Delete reel"""
        success = self.reel_repo.delete_reel(reel_id, user_id)
        if success:
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
        return success
    
    def like_reel(self, reel_id: int, user_id: int) -> bool:
        """Like a reel"""
        # Check if already liked
        if self.like_repo.is_liked(user_id, reel_id=reel_id):
            return False
        
        # Create like
        success = self.like_repo.create_like(user_id, reel_id=reel_id)
        if success:
            # Update like count
            self.reel_repo.increment_like_count(reel_id)
            
            # Send notification (async)
            # self._send_like_notification(reel_id, user_id, "reel")
            
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
        
        return success
    
    def unlike_reel(self, reel_id: int, user_id: int) -> bool:
        """Unlike a reel"""
        success = self.like_repo.remove_like(user_id, reel_id=reel_id)
        if success:
            # Update like count
            self.reel_repo.decrement_like_count(reel_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
        
        return success
    
    def view_reel(self, reel_id: int) -> bool:
        """Record reel view"""
        self.reel_repo.increment_view_count(reel_id)
        return True
    
    def create_reel_comment(self, comment: ReelCommentCreate, user_id: int) -> Optional[ReelCommentResponse]:
        """Create a reel comment"""
        db_comment = self.reel_comment_repo.create_comment(comment, user_id)
        if db_comment:
            # Update comment count
            self.reel_repo.increment_comment_count(comment.reel_id)
            
            # Send notification (async)
            # self._send_comment_notification(comment.reel_id, user_id, "reel")
            
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
            
            return ReelCommentResponse.from_orm(db_comment)
        return None
    
    def get_reel_comments(self, reel_id: int, page: int = 1, size: int = 20) -> List[ReelCommentResponse]:
        """Get reel comments"""
        skip = (page - 1) * size
        comments = self.reel_comment_repo.get_reel_comments(reel_id, skip, size)
        return [ReelCommentResponse.from_orm(comment) for comment in comments]
    
    def delete_reel_comment(self, comment_id: int, user_id: int) -> bool:
        """Delete reel comment"""
        # Get comment to find reel_id
        comment = self.reel_comment_repo.get_reel_comments(comment_id, 0, 1)
        if not comment:
            return False
        
        success = self.reel_comment_repo.delete_comment(comment_id, user_id)
        if success:
            # Update comment count
            self.reel_repo.decrement_comment_count(comment[0].reel_id)
            
            # Invalidate cache
            self.cache_helper.invalidate_reel_feed()
        
        return success

