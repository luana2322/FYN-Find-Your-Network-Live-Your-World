from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[List[str]] = None
    type: str = "text"

class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[List[str]] = None

class PostResponse(BaseModel):
    id: int
    user_id: int
    content: Optional[str]
    media_url: Optional[List[str]]
    type: str
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostFeedResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    size: int
    has_next: bool
