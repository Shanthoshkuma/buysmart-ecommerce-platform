from sqlalchemy import Column , Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, DECIMAL,DateTime
from sqlalchemy.orm import relationship 
from app.database import Base
from sqlalchemy.sql import func

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable = False)
    total_amount = Column(DECIMAL(10,2),nullable=False)
    status= Column(String(20),default='pending')
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    payment = relationship("Payment", back_populates="order", uselist=False) 