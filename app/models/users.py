from sqlalchemy import Column , Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "public"}


    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(100), nullable = False)
    email = Column(String(255), nullable = False)
    password_hash = Column(String(200), nullable = False)
    role = Column(String(100),default='customer')
    is_active = Column(Boolean,default=True)
    created_at = Column(TIMESTAMP)

    orders = relationship("Order", back_populates="user", cascade="all, delete")
    cart_items = relationship(
    "Cart",
    back_populates="user",
    cascade="all, delete"
)