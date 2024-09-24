from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.utils import get_db
from typing import List

router = APIRouter(
    prefix="/scopes",
    tags=["scopes"],
)

@router.post("/", response_model=schemas.Scope)
def create_scope(scope: schemas.ScopeCreate, db: Session = Depends(get_db)):
    db_scope = crud.get_by_name(db, model=models.Scope, name=scope.name)
    if db_scope:
        raise HTTPException(status_code=400, detail="Scope already exists.")
    return crud.create(db=db, model=models.Scope, obj_in=scope)

@router.get("/", response_model=List[schemas.Scope])
def read_scopes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_multi(db, model=models.Scope, skip=skip, limit=limit)
