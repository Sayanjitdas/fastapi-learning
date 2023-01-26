from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):

    firstname: str
    lastname: str
    email: str
    password: str

class UserResponse(BaseModel):

    uid: int
    email: str

    class Config:
        orm_mode = True

class ArticleList(BaseModel):

    article_id: int
    title: str
    is_published: bool
    published_at: datetime

    class Config:
        orm_mode = True

class UserDetailResponse(BaseModel):

    uid: int
    email: str
    firstname: str
    lastname: str
    articles: List[ArticleList] = []

    class Config:
        orm_mode = True
