from typing import Optional, List

from exceptiongroup import catch
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from enum import Enum
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor # this is so that queries return column names as well
import time

from app import utils, models, schemas

from .database import Base, engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings


# once alembic is setup - alembic takes care of any migration changes (including table creation)
# so below command is no longer needed as this command is mostly responsible for creating tables in database by sqlalchemy
# models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# check if configs are okay on startup - temporary
# print(settings)


# GET operation
# @app.get("/")
# async def root():
#     return {"message": "Hello World man"}



# GET operation
# @app.get("/posts")
# def get_posts():
#     return {"data": "this is your posts"}



# Path parameter
# @app.get("/posts/{post_id}")
# def get_post(post_id: int):
#     return {"post_id": post_id}



# enumerated path parameter example
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}



# POST request
# @app.post("/posts/create")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"data": "successfully created posts"}



# POST request with Pydantic model - data validation
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # optional with a default value set in backend
#     rating: Optional[int] = None # optional with no default value set

# @app.post("/posts")
# def create_post(new_post: Post):
#     # new_post is a class instance (Pydantic model)
#     print(new_post)
#     print(new_post.dict())
#     print(new_post.content)
#     print(new_post.title)
#     print(new_post.published)
#     print(new_post.rating)
#     # return {"data": "successfully created post"}
#     # return {"data": new_post.dict()}
#     return {"data": new_post}



# making requests with in memory storage
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "title of post 2", "content": "content of post 2", "id": 2}]

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # optional with a default value set in backend
#     rating: Optional[int] = None # optional with no default value set

# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts}

# @app.post("/posts", status_code = status.HTTP_201_CREATED) # to set a default status_code use the path operation decorator
# def create_post(new_post: Post):
#     post_dict = new_post.model_dump()
#     post_dict["id"] = randrange(0, 10000000)
#     my_posts.append(post_dict)
#     # usually you send the newly created post with id
#     return {"data": post_dict}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response): # type annotation of path parameter is important otherwise fastapi will convert it into a string by default
#     # print(type(id))
#     post = None

#     for p in my_posts:
#         if p["id"] == id:
#             post = p
#             # print(post)

#     if not post:
#         # 1st solution
#         # response.status_code = 404

#         # 2nd solution
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return { "detail": f"post with id: {id} not found"}

#         # 3rd solution
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

#     return {"data": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
# def delete_post(id: int):
#     index = None

#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             index = i
    
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")

#     my_posts.pop(index)
    
#     return {"data": f"post with id: {id} deleted successfully"}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = None

#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             index = i
    
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     my_posts.pop(index)

# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_post(id: int, post: Post):
#     index = None
    
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             index = i
    
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     post_dict = post.model_dump()
#     post_dict["id"] = randrange(0, 100000000)
#     my_posts[index] = post_dict

#     return { "data": post_dict}



# making requests with a database connection
# this method does not use any ORM. It uses a basic adapter for Postgres called psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(database="fastapi", user="postgres", password="password", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("db connection setup complete")
#         break
#     except Exception as error:
#         print("db connection setup failed")
#         print("Error: ", error)
#         time.sleep(2)


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # optional with a default value set in backend

# @app.get("/posts")
# def get_posts():
#     # posts = cursor.execute("""SELECT * FROM posts""") # cursor.execute() doesn't return anything, it just executes the SQL command
#     cursor.execute("""
#                    SELECT * FROM posts
#                    """)
#     posts = cursor.fetchall()

#     # print(posts)

#     return {"data": posts}

# @app.post("/posts", status_code = status.HTTP_201_CREATED) # to set a default status_code use the path operation decorator
# def create_post(post: Post):
#     cursor.execute("""
#             INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
#         """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()

#     # to commit the changes into database
#     conn.commit()

#     return {"data": new_post}

# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
#     post = cursor.fetchone()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

#     return {"data": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
#     deleted_post = cursor.fetchone()

#     conn.commit()
    
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                    (post.title, post.content, post.published, id, ))
#     updated_post = cursor.fetchone()

#     conn.commit()
    
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")

#     return { "data": updated_post}



# making requests using ORM for database connection - SQLAlchemy
# class Post(BaseModel):
#     title: str
#     content: str
#     published: Optional[bool] = None

# # GET operation for ORM testing
# @app.get("/sqlalchemy")
# async def root(db: Session = Depends(get_db)):
#     # posts = db.query(models.Post)
#     # print(posts) # prints sql query

#     # return {"data": "successful"}

#     posts = db.query(models.Post).all()
#     return {"data": posts}

# @app.get("/posts")
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

# @app.post("/posts", status_code = status.HTTP_201_CREATED)
# def create_post(post: Post, db: Session = Depends(get_db)):
#     # new_post = models.Post(
#     #     title = post.title,
#     #     content = post.content,
#     #     published = post.published
#     # )

#     new_post = models.Post(**post.model_dump())

#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return {"data": new_post}

# @app.get("/posts/{id}")
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

#     return {"data": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     db.delete(post)
#     db.commit()

# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_post(id: int, post: Post, db: Session = Depends(get_db)):
#     post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if post_to_update == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     post_to_update.title = post.title
#     post_to_update.content = post.content
#     post_to_update.published = post.published

#     db.commit()
#     db.refresh(post_to_update)

#     return { "data": post_to_update}




# Request and Response schemas with Pydantic models
# @app.get("/posts", response_model = List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

# @app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     new_post = models.Post(**post.model_dump())

#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# @app.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

#     return post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     db.delete(post)
#     db.commit()

# @app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#     post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if post_to_update == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     post_to_update.title = post.title
#     post_to_update.content = post.content
#     post_to_update.published = post.published

#     db.commit()
#     db.refresh(post_to_update)

#     return post_to_update




# using router for better organization of path operation
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}