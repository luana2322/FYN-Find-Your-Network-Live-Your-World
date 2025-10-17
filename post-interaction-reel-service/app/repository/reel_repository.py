from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from app.model import Reel, ReelComment
from app.schema.reel_schema import ReelCreate, ReelUpdate, ReelCommentCreate

class ReelRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_reel(self, reel: ReelCreate, user_id: int) -> Reel:
        db_reel = Reel(
            user_id=user_id,
            video_url=reel.video_url,
            thumbnail_url=reel.thumbnail_url,
            audio_url=reel.audio_url,
            duration=reel.duration
        )
        self.db.add(db_reel)
        self.db.commit()
        self.db.refresh(db_reel)
        return db_reel
    
    def get_reel_by_id(self, reel_id: int) -> Optional[Reel]:
        return self.db.query(Reel).filter(Reel.id == reel_id).first()
    
    def get_user_reels(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Reel]:
        return self.db.query(Reel).filter(Reel.user_id == user_id).order_by(desc(Reel.created_at)).offset(skip).limit(limit).all()
    
    def get_reel_feed(self, skip: int = 0, limit: int = 20) -> List[Reel]:
        return self.db.query(Reel).order_by(desc(Reel.created_at)).offset(skip).limit(limit).all()
    
    def update_reel(self, reel_id: int, reel_update: ReelUpdate, user_id: int) -> Optional[Reel]:
        db_reel = self.db.query(Reel).filter(and_(Reel.id == reel_id, Reel.user_id == user_id)).first()
        if db_reel:
            if reel_update.thumbnail_url is not None:
                db_reel.thumbnail_url = reel_update.thumbnail_url
            if reel_update.audio_url is not None:
                db_reel.audio_url = reel_update.audio_url
            self.db.commit()
            self.db.refresh(db_reel)
        return db_reel
    
    def delete_reel(self, reel_id: int, user_id: int) -> bool:
        db_reel = self.db.query(Reel).filter(and_(Reel.id == reel_id, Reel.user_id == user_id)).first()
        if db_reel:
            self.db.delete(db_reel)
            self.db.commit()
            return True
        return False
    
    def increment_view_count(self, reel_id: int) -> None:
        reel = self.db.query(Reel).filter(Reel.id == reel_id).first()
        if reel:
            reel.view_count += 1
            self.db.commit()
    
    def increment_like_count(self, reel_id: int) -> None:
        reel = self.db.query(Reel).filter(Reel.id == reel_id).first()
        if reel:
            reel.like_count += 1
            self.db.commit()
    
    def decrement_like_count(self, reel_id: int) -> None:
        reel = self.db.query(Reel).filter(Reel.id == reel_id).first()
        if reel and reel.like_count > 0:
            reel.like_count -= 1
            self.db.commit()
    
    def increment_comment_count(self, reel_id: int) -> None:
        reel = self.db.query(Reel).filter(Reel.id == reel_id).first()
        if reel:
            reel.comment_count += 1
            self.db.commit()
    
    def decrement_comment_count(self, reel_id: int) -> None:
        reel = self.db.query(Reel).filter(Reel.id == reel_id).first()
        if reel and reel.comment_count > 0:
            reel.comment_count -= 1
            self.db.commit()

class ReelCommentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_comment(self, comment: ReelCommentCreate, user_id: int) -> ReelComment:
        db_comment = ReelComment(
            reel_id=comment.reel_id,
            user_id=user_id,
            parent_id=comment.parent_id,
            content=comment.content
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment
    
    def get_reel_comments(self, reel_id: int, skip: int = 0, limit: int = 20) -> List[ReelComment]:
        return self.db.query(ReelComment).filter(ReelComment.reel_id == reel_id).order_by(desc(ReelComment.created_at)).offset(skip).limit(limit).all()
    
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        db_comment = self.db.query(ReelComment).filter(and_(ReelComment.id == comment_id, ReelComment.user_id == user_id)).first()
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
            return True
        return False

