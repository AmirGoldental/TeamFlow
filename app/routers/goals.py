from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.utils import get_db
from typing import List

router = APIRouter(
    prefix="/goals",
    tags=["goals"],
)

@router.post("/", response_model=schemas.Goal)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    db_goal = crud.get_by_name(db, model=models.Goal, name=goal.name)
    if db_goal:
        raise HTTPException(status_code=400, detail="Goal already exists.")
    return crud.create(db=db, model=models.Goal, obj_in=goal)

@router.get("/", response_model=List[schemas.Goal])
def read_goals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_multi(db, model=models.Goal, skip=skip, limit=limit)
