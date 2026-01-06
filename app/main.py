from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.database import engine
from app.models import Base

from app.routers.product_router import router as product_router
from app.routers.auth_router import router as auth_router
from app.routers.cart_router import router as cart_router
from app.routers.order_router import router as order_router
from app.routers.user_router import router as user_router
from app.routers.admin_router import router as admin_router
from app.routers.admin_product_router import router as admin_product_router
from app.routers.admin_order_router import router as admin_order_router

app = FastAPI(title="ecommerce")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return RedirectResponse(url="/products/", status_code=307)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 🔥 ROUTER ORDER
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(admin_product_router)
app.include_router(admin_order_router)
