from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr


# class Post(BaseModel):
#     title: str
#     content: str
#     published: Optional[bool] = None

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: Optional[bool] = None

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: Optional[bool] = None

# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: Optional[bool] = None

# class PostCreate(PostBase):
#     pass

# class Post(PostBase):
#     model_config = ConfigDict(from_attributes=True) # orm objects are converted into python dictionaries to run validation

#     id: int
#     created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None



# pydantic schema with relational mapping
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True) # orm objects are converted into python dictionaries to run validation

    id: int
    created_at: datetime
    user_id: int
    user: UserOut





class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]




# post response schema with number of votes for a post
class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Post: Post
    votes: int