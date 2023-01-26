from shutil import copyfileobj
from typing import List,Union
from fastapi import APIRouter,Depends,Response,status,HTTPException,Form,UploadFile,File
from sqlalchemy.orm import Session
from util import Hash,get_db
from .schemas import UserResponse,User,UserDetailResponse
from models import Users

user_app = APIRouter(prefix="/users",tags=["users",])

@user_app.post("/",response_model=UserResponse)
def create_user(request: User,db: Session = Depends(get_db)):
    """
    This controller function creates user
    """
    new_user = Users(
        firstname = request.firstname,
        lastname = request.lastname,
        email = request.email,
        password = Hash.encrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_app.get("/",response_model=List[UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    return db.query(Users).all()

@user_app.get("/{uid}",
    response_model=Union[UserDetailResponse,None],
    responses={
    400:{
        "content":{
            "application/json" :{
                "example": "User with id <id number> not found"
            }
        },
        "description":"400 bad request"
    }
})
def get_user_with_id(uid:int,db: Session = Depends(get_db)):
    usr = db.query(Users).filter(Users.uid == uid).first()
    if usr is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= f"User with id {uid} not found")
    return usr

@user_app.put("/{uid}/update")
def update_user(uid: int,request: User,response: Response,db: Session = Depends(get_db)):
    try:
        obj = db.query(Users).filter(Users.uid == uid).first()
        obj.firstname = request.firstname
        obj.lastname = request.lastname
        obj.email = request.email
        obj.password = Hash.encrypt(request.password)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "failed!!")
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="failed!! check server logs")

@user_app.delete("/{uid}/delete")
def delete_a_user(uid: int,response: Response,db: Session = Depends(get_db)):
    try:
        db.query(Users).filter(Users.uid == uid).delete()
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        response.status_code = status.HTTP_400_BAD_REQUEST


@user_app.post("/profile")
def user_profile(
    name: str = Form(min_length=2),
    age: int = Form(gt=0),
    phone_number: str = Form(min_length=10,regex="^\d*$"),
    profile_pic: UploadFile = File(...)
):
    filename = f"{profile_pic.filename}"
    filepath = f"media/{filename}"
    with open(filepath,"wb") as buffer:
        copyfileobj(profile_pic.file,buffer)
    
    return {
        "name": name,
        "age": age,
        "phone_number": phone_number,
        "profile_pic": filename
    }