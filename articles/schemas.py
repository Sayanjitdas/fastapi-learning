from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):

    creator_id: int
    title: str
    content: str
    is_published: bool = True

class ArticleResponse(BaseModel):

    creator_id: int
    article_id: int
    title: str
    is_published: bool
    published_at: datetime

    class Config:
        orm_mode = True