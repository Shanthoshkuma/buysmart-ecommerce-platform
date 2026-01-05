from fastapi import FastAPI, APIRouter , HTTPException, status, Depends , Request
from app.auth.dependencies import admin_required
from app.models import User
from fastapi.templating import Jinja2Templates
from app.models.users import User
from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/admin",tags=["Admin"])

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/dashboard",status_code=status.HTTP_200_OK)
async def dashboard(request:Request,current_role : User = Depends(admin_required)):

    return templates.TemplateResponse("admin_dashboard.html",{"request":request,"admin":current_role})


@router.get("/manage_user")
async def manage_user(request:Request,db:db_dependency,current_role : User = Depends(admin_required)):

    show_user = db.query(User).all()

    return templates.TemplateResponse("admin_manage_user.html",{"request":request,"show_user":show_user})

@router.post("/manage_user/{user_id}")
def delete_user(request:Request,user_id:int,db:db_dependency,current_role : User = Depends(admin_required)):

    user = db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code = 400, detail ="User Not Found")
    
    db.delete(user)
    db.commit()

    return RedirectResponse(url=f"/admin/manage_user?msg=User {user.id} removed successfully",
            status_code=303
        )