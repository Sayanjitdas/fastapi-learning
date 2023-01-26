from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .oauth2 import oauth2_schema
from util import get_db,Hash,create_access_token
from models import Users


auth_router = APIRouter(tags=["authentication",])

@auth_router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect Password")
    
    access_token = create_access_token({"user":user.email})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user_id": user.uid,
        "username": user.email
    }