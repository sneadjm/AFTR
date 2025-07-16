from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class FriendCreate(BaseModel):
    name: str
    birthday: date

class FriendOut(BaseModel):
    id: int
    name: str
    birthday: date
    photo_url: Optional[str]

    class Config:
        orm_mode = True

class PhotoOut(BaseModel):
    id: int
    filename: str
    taken_at: Optional[date]

    class Config:
        orm_mode = True