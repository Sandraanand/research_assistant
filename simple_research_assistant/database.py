"""
Simple Database Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import config

Base = declarative_base()


class PaperSubmission(Base):
    """Store paper submissions"""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True)
    submission_id = Column(String(50), unique=True, index=True)
    title = Column(String(500))
    authors = Column(Text)
    content = Column(Text)
    professor_email = Column(String(255))
    status = Column(String(50), default="submitted")
    feedback = Column(Text)
    submitted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Database setup
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Initialize database"""
    Base.metadata.create_all(engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
