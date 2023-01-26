from typing import Optional,Union
from datetime import timedelta,datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt,JWTError

################### DB INITIALIZATION #################################
engine = create_engine('sqlite:///fastapi-user.sqlite',connect_args = {
    "check_same_thread": False
})

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()
    try:
        yield db
    except Exception as err:
        raise err
    finally:
        db.close()
#######################################################################

############### PASSWORD ENCODING/HASHING/VERIFYING ###################
class Hash:

    pwd_ctx = CryptContext(schemes='bcrypt',deprecated='auto')

    @classmethod
    def encrypt(cls,raw_str:str):

        return cls.pwd_ctx.hash(raw_str)
    
    @classmethod
    def verify(cls,raw_str:str, hashed_str:str):

        return cls.pwd_ctx.verify(raw_str,hashed_str)
#######################################################################

############# Authentication Token ####################################
SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 15

def create_access_token(data: dict ,expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username: str = payload.get("user")
        if not username:
            return None
    except JWTError as err:
        print(err)
        return None
    return username
#######################################################################