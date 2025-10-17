from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from app.model.comment_model import Comment
from app.schema.comment_schema import CommentCreate, CommentUpdate

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_comment(self, comment: CommentCreate, user_id: int) -> Comment:
        db_comment = Comment(
            post_id=comment.post_id,
            user_id=user_id,
            parent_id=comment.parent_id,
            content=comment.content
        )
        self.db.add(db_comment) 
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment
    
    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()
    
    def get_post_comments(self, post_id: int, skip: int = 0, limit: int = 20) -> List[Comment]:
        return self.db.query(Comment).filter(Comment.post_id == post_id).order_by(desc(Comment.created_at)).offset(skip).limit(limit).all()
    
    def update_comment(self, comment_id: int, comment_update: CommentUpdate, user_id: int) -> Optional[Comment]:
        db_comment = self.db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user_id)).first()
        if db_comment:
            db_comment.content = comment_update.content
            self.db.commit()
            self.db.refresh(db_comment)
        return db_comment
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        db_comment = self.db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user_id)).first()
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
            return True
        return False

class LikeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_like(self, user_id: int, post_id: Optional[int] = None, reel_id: Optional[int] = None) -> bool:
        # Check if like already exists
        existing_like = self.db.query(Like).filter(
            and_(
                Like.user_id == user_id,
                Like.post_id == post_id,
                Like.reel_id == reel_id
            )
        ).first()
        
        if existing_like:
            return False
        
        db_like = Like(
            user_id=user_id,
            post_id=post_id,
            reel_id=reel_id
        )
        self.db.add(db_like)
        self.db.commit()
        return True
    
    def remove_like(self, user_id: int, post_id: Optional[int] = None, reel_id: Optional[int] = None) -> bool:
        db_like = self.db.query(Like).filter(
            and_(
                Like.user_id == user_id,
                Like.post_id == post_id,
                Like.reel_id == reel_id
            )
        ).first()
        
        if db_like:
            self.db.delete(db_like)
            self.db.commit()
            return True
        return False
    
    def is_liked(self, user_id: int, post_id: Optional[int] = None, reel_id: Optional[int] = None) -> bool:
        like = self.db.query(Like).filter(
            and_(
                Like.user_id == user_id,
                Like.post_id == post_id,
                Like.reel_id == reel_id
            )
        ).first()
        return like is not None
