from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from util import Base

class Users(Base):

    __tablename__ = "users"

    uid = Column(Integer,primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=False),default=func.now())
    articles = relationship("Articles",back_populates='users')

class Articles(Base):
    
    __tablename__ = "articles"

    article_id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    is_published = Column(Boolean)
    published_at = Column(DateTime(timezone=False),default=func.now())
    creator_id = Column(Integer,ForeignKey('users.uid'))
    users = relationship("Users",back_populates='articles') 