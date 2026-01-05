from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    name: str = Field(min_lenght =1)
    email: EmailStr
    password: str = Field(min_lenght =3)

class UserLogin(BaseModel):
    email: EmailStr
    password:str