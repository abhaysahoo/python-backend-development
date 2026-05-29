from typing import List, Optional
from fastapi import Depends, status, HTTPException, APIRouter
from app import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", # route prefix
    tags=["Posts"] # tags for grouping
)



# post routes without relational mapping with users table
# @router.get("", response_model = List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).all()
#     return posts

# @router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     new_post = models.Post(**post.model_dump())

#     # print(token_data) # TokenData pydantic model
#     # print(token_data.id) # user id stored in TokenData model
#     # print(current_user)
#     # print(current_user.id)
#     # print(current_user.email)

#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post

# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

#     return post

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     db.delete(post)
#     db.commit()

# @router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if post_to_update == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
#     post_to_update.title = post.title
#     post_to_update.content = post.content
#     post_to_update.published = post.published

#     db.commit()
#     db.refresh(post_to_update)

#     return post_to_update





# post routes with relational mapping with users table
# @router.get("", response_model = List[schemas.Post])
# def get_posts(
#     db: Session = Depends(get_db), 
#     current_user: models.User = Depends(oauth2.get_current_user), 
#     limit: Optional[int] = None, 
#     skip: Optional[int] = None,
#     search: Optional[str] = None
# ):
#     # print(limit)
#     # print(skip)
#     # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
#     # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).limit(limit).all()
#     # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).offset(skip).limit(limit).all()

#     query = db.query(models.Post).filter(models.Post.user_id == current_user.id)

#     if search is not None:
#         query = query.filter(models.Post.title.contains(search))

#     if limit is not None:
#         query = query.limit(limit)

#     if skip is not None:
#         query = query.offset(skip)

#     posts = query.all()

#     return posts

@router.post("", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), user_id = current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
#     if post.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"unauthorized access to post with id: {id}")

#     return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"unauthorized access to post with id: {id}")
    
    db.delete(post)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
    if post_to_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"unauthorized access to post with id: {id}")
    
    post_to_update.title = post.title
    post_to_update.content = post.content
    post_to_update.published = post.published
    post_to_update.user_id = current_user.id

    db.commit()
    db.refresh(post_to_update)

    return post_to_update




# post routes with relational mapping with users table and join operation with votes table
@router.get("", response_model = List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user), 
    limit: Optional[int] = None, 
    skip: Optional[int] = None,
    search: Optional[str] = None
):
    query = db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, 
            models.Post.id == models.Vote.post_id, 
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.user_id == current_user.id
        )

    if search is not None:
        query = query.filter(models.Post.title.contains(search))

    if limit is not None:
        query = query.limit(limit)

    if skip is not None:
        query = query.offset(skip)

    posts = query.all()

    return posts

# one post with total vote count
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, 
            models.Post.id == models.Vote.post_id, 
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id == id
        ).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"unauthorized access to post with id: {id}")

    return post
