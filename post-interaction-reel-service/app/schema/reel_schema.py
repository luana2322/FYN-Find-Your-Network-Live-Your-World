from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReelCreate(BaseModel):
    video_url: str
    thumbnail_url: Optional[str] = None
    audio_url: Optional[str] = None
    duration: int

class ReelUpdate(BaseModel):
    thumbnail_url: Optional[str] = None
    audio_url: Optional[str] = None

class ReelResponse(BaseModel):
    id: int
    user_id: int
    video_url: str
    thumbnail_url: Optional[str]
    audio_url: Optional[str]
    duration: int
    view_count: int
    like_count: int
    comment_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReelFeedResponse(BaseModel):
    reels: List[ReelResponse]
    total: int
    page: int
    size: int
    has_next: bool

class ReelCommentCreate(BaseModel):
    reel_id: int
    content: str
    parent_id: Optional[int] = None

class ReelCommentResponse(BaseModel):
    id: int
    reel_id: int
    user_id: int
    parent_id: Optional[int]
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
