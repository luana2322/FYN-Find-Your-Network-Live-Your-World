from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base

class Reel(Base):
    __tablename__ = "reels"
    __table_args__ = {'extend_existing': True}  # ✅ thêm dòng này
    
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
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reel = relationship("Reel", back_populates="comments")
    parent = relationship("ReelComment", remote_side=[id], backref="replies")
