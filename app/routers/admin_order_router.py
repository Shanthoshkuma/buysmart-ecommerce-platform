from fastapi import APIRouter, Request, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.products import Product
from app.auth.dependencies import admin_required
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.responses import RedirectResponse
router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/order")
def get_order(request:Request,db:db_dependency,admin=Depends(admin_required)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()

    return templates.TemplateResponse("admin_order.html",{"request":request,"orders":orders})

@router.get("/order/{order_id}")
def get_orderById(request:Request,order_id:int,db:db_dependency,admin=Depends(admin_required)):
    order = db.query(Order).filter(Order.id==order_id).first()

    if not order:
        raise HTTPException(status_code =404 , detail ="Order Not Found")
    
    items = db.query(OrderItem, Product).join(Product, OrderItem.product_id == Product.id).filter(OrderItem.order_id==order_id).all()
    
    return templates.TemplateResponse("admin_order_detail.html",{"request":request,"order":order,"items":items})


@router.post("/order/update/{order_id}")
def update_order_status(db: db_dependency ,
    order_id: int,
    status: str = Form(...),
    
    admin=Depends(admin_required)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()

    return RedirectResponse(
        url="/admin/order?msg=Order status updated successfully",
        status_code=303
    )