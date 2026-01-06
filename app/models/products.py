from sqlalchemy import Column , Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base
class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {"schema": "public"}


    id = Column(Integer, primary_key=True,index=True)
    category_id = Column(Integer,ForeignKey("public.categories.id"),nullable = False)
    name = Column(String(150), nullable = False)
    description = Column(Text)
    price = Column(DECIMAL(10,2),nullable = False)
    stock = Column(Integer,default=0)
    image_url = Column(String(400))
    is_active = Column(Boolean,default = True)
    created_at = Column(TIMESTAMP)

    order_items = relationship("OrderItem", back_populates="product")
    category = relationship("Category", back_populates="products")
    cart_items = relationship(
    "Cart",
    back_populates="product",
    cascade="all, delete"
)
