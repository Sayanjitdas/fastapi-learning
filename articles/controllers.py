from typing import List
from fastapi import APIRouter,Depends,Response
from sqlalchemy.orm import Session

from .schemas import ArticleResponse,Article
from util import get_db
from models import Articles
from auth.oauth2 import get_current_user


article_app = APIRouter(prefix="/articles",tags=["articles",])


@article_app.get("/{creator_id}",response_model=List[ArticleResponse])
def get_articles_by_creator_id(creator_id: int,db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    print(current_user.email)
    return db.query(Articles).filter(Articles.creator_id == creator_id).all()

@article_app.post("/",response_model=ArticleResponse)
def create_article(request: Article,response: Response,db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):

    article_obj = Articles(
        creator_id = request.creator_id,
        title = request.title,
        content = request.content,
        is_published = request.is_published
    )

    db.add(article_obj)
    db.commit()
    db.refresh(article_obj)
    return article_obj