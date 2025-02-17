from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base


# class Post(BaseModel):  # Pydantic model to standardize user input (Schema)
#     title: str
#     content: str
#     published: bool = True  # If user doesn't published, default to True
#     # rating: Optional[int] = None (removed as PostgreSQL applies default value)

# Post Stuff
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    # We mention this line to convert pydantic model into sqlalchemy model
    class Config:
        orm_mode = True

# class CreatePost(BaseModel):
#     # You can add/remove variables here just like in UpdatePost to
#     # Send or receive certain info to/from database. Eg, 'password'
#     # since the user already knows their password, and so on.
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     # You can add or remove variables in this class to allow how much a user
#     # can change their post. You can decide to only allow 'published' to change
#     # or only 'content' to change, and so on.
#     title: str
#     content: str
#     published: bool

# User Stuff


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# OAuth2 Stuff


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
