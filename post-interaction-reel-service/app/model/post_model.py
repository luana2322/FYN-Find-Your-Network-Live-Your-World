from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'extend_existing': True}  # ✅ thêm dòng này
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    content = Column(Text)
    media_url = Column(ARRAY(String))
    type = Column(String(20), default="text")
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    parent_id = Column(BigInteger, ForeignKey("comments.id"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=True)
    reel_id = Column(BigInteger, ForeignKey("reels.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="likes")
    reel = relationship("Reel", back_populates="likes")

class Reel(Base):
    __tablename__ = "reels"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    video_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    audio_url = Column(String)
    duration = Column(Integer, nullable=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    likes = relationship("Like", back_populates="reel", cascade="all, delete-orphan")
    comments = relationship("ReelComment", back_populates="reel", cascade="all, delete-orphan")

class ReelComment(Base):
    __tablename__ = "reel_comments"
    
    id = Column(BigInteger, primary_key=True, index=True)
    reel_id = Column(BigInteger, ForeignKey("reels.id"), nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    parent_id = Column(BigInteger, ForeignKey("reel_comments.id"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reel = relationship("Reel", back_populates="comments")
    parent = relationship("ReelComment", remote_side=[id], backref="replies")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    actor_id = Column(BigInteger, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    reference_id = Column(BigInteger, nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
