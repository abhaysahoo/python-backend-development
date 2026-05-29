from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app import models, oauth2, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    # prefix="/posts",
    tags=["Authentication"]
)

# login without OAuth2PasswordRequestForm
# @router.post("/login", status_code=status.HTTP_200_OK)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
#     if user == None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     # password verification
#     if not utils.verify_password(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     # create a token
#     access_token = oauth2.create_access_token(data = {
#         "user_id": user.id
#     })
    
#     # return token
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # password verification
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # create a token
    access_token = oauth2.create_access_token(data = {
        "user_id": user.id
    })

    token = schemas.Token(
        access_token=access_token,
        token_type="bearer"
    )
    
    # return token
    # return {"access_token": access_token, "token_type": "bearer"}
    return token

    