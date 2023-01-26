from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from util import get_db,verify_access_token
from models import Users

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(token: str = Depends(oauth2_schema),db: Session = Depends(get_db)):
    
    expection_cred = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    username = verify_access_token(token)

    if not username:
        raise expection_cred
    else:
        user = db.query(Users).filter(Users.email == username).first()

        if not user:
            raise expection_cred
        return user