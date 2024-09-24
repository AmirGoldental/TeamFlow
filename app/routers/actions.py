from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.utils import get_db
from typing import List

router = APIRouter(
    prefix="/actions",
    tags=["actions"],
)

@router.post("/", response_model=schemas.Action)
def create_action(action: schemas.ActionCreate, db: Session = Depends(get_db)):
    db_action = crud.get_by_name(db, model=models.Action, name=action.name)
    if db_action:
        raise HTTPException(status_code=400, detail="Action already exists.")
    return crud.create(db=db, model=models.Action, obj_in=action)

@router.get("/", response_model=List[schemas.Action])
def read_actions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_multi(db, model=models.Action, skip=skip, limit=limit)
