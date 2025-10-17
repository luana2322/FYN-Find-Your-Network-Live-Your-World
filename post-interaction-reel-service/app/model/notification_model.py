from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}  # ✅ thêm dòng này
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    actor_id = Column(BigInteger, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    reference_id = Column(BigInteger, nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
