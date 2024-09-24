from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.utils import get_db
from typing import List

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_name(db, name=event.name)
    if db_event:
        raise HTTPException(status_code=400, detail="Event already exists.")
    return crud.create_event(db=db, event=event)

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events
