from fastapi import FastAPI, APIRouter, status,HTTPException ,Request ,Depends
from sqlalchemy.orm import Session
from app.models.products import Product 
from app.database import SessionLocal
from typing import Annotated

from fastapi.templating import Jinja2Templates 



router = APIRouter(prefix="/user", tags=["Products"])

templates = Jinja2Templates(directory="app/templates")  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/")
def home_product(request:Request, db: db_dependency,page: int = 1,):
    sample_products = db.query(Product).all()

    if not sample_products:
        raise HTTPException(status_code = 404, detail ="Not Found")
    
    return templates.TemplateResponse("home.html",{"request":request,"products":sample_products})


@router.get("/{id}")
def get_product(request:Request,id:int,db:db_dependency):

    get_product = db.query(Product).filter(Product.id == id).first()

    if not get_product:
        raise HTTPException(status_code =404,detail ="Not Found")
    
    return templates.TemplateResponse("product_detail.html",{"request":request,"show_product":get_product})

