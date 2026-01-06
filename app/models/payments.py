from sqlalchemy import Column , Integer, String, Boolean, TIMESTAMP, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship 
from app.database import Base
class Payment(Base):
    __tablename__ = "payments"
    

    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"),nullable=False)
    payment_method = Column(String(50))
    payment_status = Column(String(20),default='pending')
    transaction_id= Column(String(225))
    paid_at = Column(TIMESTAMP)

    order = relationship("Order", back_populates="payment")
