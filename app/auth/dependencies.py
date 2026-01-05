### After Authentication(Login) process JWT Token created this file will process authorization process(decoing jwt) whether the user is valid or not 

from fastapi import FastAPI , Depends , HTTPException, status , Request
from sqlalchemy.orm import Session
from jose import jwt , JWTError
from typing import Annotated
from app.database import SessionLocal 
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from .jwt import SECRET_KEY,ALGORITHM
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


     
    

## authrization and reterival user information from token using oauthform
#def get_current_user_token(token:str = Depends(oauth2_scheme),db: db_dependency): # type: ignore

#def get_current_user_token(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)): 

## authrization and reterival user information from token using htmlform
def get_current_user_token(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM]) 
        email : str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invaild Token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invaild Token")
    
    validate_user = db.query(User).filter(User.email == email).first()

    if not validate_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return validate_user

### From Autharaization user information admin security 
### it Autharaized token and returns user info from db
#def admin_required(token:str=Depends(get_current_user_token)):

def admin_required(
    current_user: User = Depends(get_current_user_token)
) :

    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user





    
    

