from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user), 
):
    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted for post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
           
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        db.delete(found_vote)
        db.commit()

        return {"message": "vote removed successfully"}