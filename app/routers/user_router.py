from fastapi import APIRouter, FastAPI,status,HTTPException,Depends
from app.auth.dependencies import get_current_user_token
from app.models import User
router = APIRouter(prefix='/user',tags=['user'])

@router.get("/profile",status_code=status.HTTP_200_OK)
async def profile(current_user: User = Depends(get_current_user_token)):

    return {"id":current_user.id,"name":current_user.name,"role":current_user.role}