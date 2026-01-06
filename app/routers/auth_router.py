## This auth_router will do Authentication process Registering and login creating access token


from fastapi import FastAPI, APIRouter , status, HTTPException, Depends, Request , Form
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserRegister, UserLogin
from app.models import User
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


router = APIRouter(prefix="/auth",tags=["Authentication"])

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register",status_code= status.HTTP_201_CREATED) 
async def register(request:Request, db:db_dependency, name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)): 

    validate_user = db.query(User).filter(User.email == email).first()
    if validate_user:
        raise HTTPException(status_code = 400, detail ="Email already registered")
    
    create_user = User(
        name = name,
        email = email,
        password_hash= hash_password(password),
        role = role
    )

    db.add(create_user)
    db.commit()
    db.refresh(create_user)

    return templates.TemplateResponse("login.html",{"request":request})


@router.post("/login",status_code=status.HTTP_200_OK)
async def login(form_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):

    validate_user = db.query(User).filter(User.email == form_data.username).first()
    if not validate_user or not verify_password(form_data.password,validate_user.password_hash,) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Email ID or Passwordwas not Registered")
    
 
    access_token = create_access_token(data = {'sub':validate_user.email})

    response = RedirectResponse(url= "/admin/dashboard" if validate_user.role == "admin" else "/products",status_code=HTTP_303_SEE_OTHER)

    response.set_cookie(key = "access_token", value = access_token, httponly = True)

    return response


###HTML PAGE

@router.get("/login")
def login(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})



@router.get("/register_account")
def register_account(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})
