from sqlalchemy import Column , String, Integer, Boolean, Text , TIMESTAMP,func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    products = relationship("Product", back_populates="category", cascade="all, delete")