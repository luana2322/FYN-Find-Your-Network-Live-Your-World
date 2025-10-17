from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    post_id: int
    content: str
    parent_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    parent_id: Optional[int]
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LikeRequest(BaseModel):
    post_id: Optional[int] = None
    reel_id: Optional[int] = None

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: Optional[int]
    reel_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
