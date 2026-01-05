from jose import jwt
from datetime import datetime, timedelta, timezone
SECRET_KEY ="424bd478f7dba3399ad5e0f0b3528fc077cf85f57f3bfd6cfed07159ad271402"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) 

    