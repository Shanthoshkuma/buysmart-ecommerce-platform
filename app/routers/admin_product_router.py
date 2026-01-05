from fastapi import FastAPI, APIRouter, status,HTTPException ,Request ,Depends, Form
from sqlalchemy.orm import Session
from app.models.products import Product 
from app.models.cart import Cart
from app.models.category import Category
from app.database import SessionLocal
from typing import Annotated
from fastapi.templating import Jinja2Templates 
from fastapi.responses import RedirectResponse
from app.auth.dependencies import admin_required
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/admin")

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/product")
def admin_product(request:Request,db:db_dependency,User = Depends(admin_required)):
    products = db.query(Product).all()

    return templates.TemplateResponse("admin_product.html",{"request":request,"products":products})

@router.get("/product/add")
def add_admin_product(request:Request,db:db_dependency,User = Depends(admin_required)):

    return templates.TemplateResponse("admin_add_product.html",{"request":request})

@router.post("/product/add")
def add_product(db:db_dependency,
                name : str= Form(...), 
                description: str = Form(...),
                price: float = Form(...), 
                stock: int = Form(...),
                cat_name: str = Form(...),
                image_url: str = Form(...),
                
                admin = Depends(admin_required)):

    category = db.query(Category).filter(Category.name == cat_name).first()

    
    if not category:
        category= Category(name = cat_name)
        db.add(category)
        db.flush()
   
    product = Product(
        name =name,
        description = description,
        price = price,
        stock = stock,
        image_url = image_url,
        category_id = category.id

    )

    db.add(product)
    db.commit()
    
    return RedirectResponse(
        url="/admin/product",
        status_code=303
    )

@router.get("/product/edit/{edit_id}")
def edit_product(request:Request,edit_id:int,db:db_dependency,admin= Depends(admin_required)):
    products = db.query(Product).filter(Product.id==edit_id).first()
    if not products:
        raise HTTPException(status_code = 400, detail ="Product Not Found")
    
    return templates.TemplateResponse("admin_edit_product.html",{"request":request,"product":products})

@router.post("/product/edit/{product_id}")
def admin_edit_product(product_id:int,db:db_dependency,
                       name: str = Form(...),
                       description:str=Form(...),
                       price:float=Form(...),
                       stock:int=Form(...),
                       image_url: str=Form(...),
                       admin=Depends(admin_required)):
    
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product :
        raise HTTPException(status_code = 400, detail ="Product Not Found")
    
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    product.image_url = image_url

    db.commit()

    return RedirectResponse(url="/admin/dashboard",status_code=303)

@router.post("/product/delete/{product_id}")
def delete_product(
    product_id: int,
    db: db_dependency,
    admin=Depends(admin_required)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404)

    db.delete(product)
    db.commit()

    return RedirectResponse(url="/admin/dashboard",status_code=303)