from fastapi import FastAPI
from users import user_app
from articles import article_app
from auth import auth_router
from models import Base
from util import engine

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_app)
app.include_router(article_app)

