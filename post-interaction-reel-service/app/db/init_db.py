from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base
from app.config.settings import settings
from app.model.post_model import Post, Comment, Like
from app.model.reel_model import Reel, ReelComment
from app.model.notification_model import Notification

def init_db():
    """Initialize database with tables"""
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_db():
    """Drop all database tables"""
    engine = create_engine(settings.DATABASE_URL)
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")

def reset_db():
    """Reset database (drop and recreate all tables)"""
    drop_db()
    init_db()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "drop":
            drop_db()
        elif command == "reset":
            reset_db()
        else:
            print("Usage: python init_db.py [init|drop|reset]")
    else:
        print("Usage: python init_db.py [init|drop|reset]")
