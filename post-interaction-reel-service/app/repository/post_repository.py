from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from app.model.post_model import Post
from app.schema.post_schema import PostCreate, PostUpdate

class PostRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, post: PostCreate, user_id: int) -> Post:
        db_post = Post(
            user_id=user_id,
            content=post.content,
            media_url=post.media_url,
            type=post.type
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
    
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Post]:
        return self.db.query(Post).filter(Post.user_id == user_id).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    
    def get_feed_posts(self, user_ids: List[int], skip: int = 0, limit: int = 20) -> List[Post]:
        return self.db.query(Post).filter(Post.user_id.in_(user_ids)).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    
    def get_global_feed(self, skip: int = 0, limit: int = 20) -> List[Post]:
        return self.db.query(Post).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    
    def update_post(self, post_id: int, post_update: PostUpdate, user_id: int) -> Optional[Post]:
        db_post = self.db.query(Post).filter(and_(Post.id == post_id, Post.user_id == user_id)).first()
        if db_post:
            if post_update.content is not None:
                db_post.content = post_update.content
            if post_update.media_url is not None:
                db_post.media_url = post_update.media_url
            self.db.commit()
            self.db.refresh(db_post)
        return db_post
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        db_post = self.db.query(Post).filter(and_(Post.id == post_id, Post.user_id == user_id)).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False
    
    def increment_like_count(self, post_id: int) -> None:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.like_count += 1
            self.db.commit()
    
    def decrement_like_count(self, post_id: int) -> None:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post and post.like_count > 0:
            post.like_count -= 1
            self.db.commit()
    
    def increment_comment_count(self, post_id: int) -> None:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.comment_count += 1
            self.db.commit()
    
    def decrement_comment_count(self, post_id: int) -> None:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post and post.comment_count > 0:
            post.comment_count -= 1
            self.db.commit()

