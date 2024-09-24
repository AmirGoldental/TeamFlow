from sqlalchemy.orm import Session
from typing import TypeVar, Type, List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app import models, schemas

ModelType = TypeVar('ModelType', bound=models.Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=schemas.BaseModel)


def get_by_id(db: Session, model: Type[ModelType], id: int) -> Optional[ModelType]:
    return db.query(model).filter(model.id == id).first()

def get_by_name(db: Session, model: Type[ModelType], name: str) -> Optional[ModelType]:
    return db.query(model).filter(model.name == name).first()

def get_multi(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100) -> List[ModelType]:
    return db.query(model).offset(skip).limit(limit).all()


def create(db: Session, model: Type[ModelType], obj_in: CreateSchemaType) -> ModelType:
    obj_data = obj_in.dict()
    db_obj = model(**obj_data)
    db.add(db_obj)
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        db.rollback()
        raise e


def update(db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
    for key, value in obj_in.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: ModelType) -> ModelType:
    db.delete(db_obj)
    db.commit()
    return db_obj

## Specific CRUD operations can be added if needed, but for most cases, the generic functions above will suffice.
#
## Example usage for Scope
#def get_scope_by_name(db: Session, name: str) -> Optional[models.Scope]:
#    return db.query(models.Scope).filter(models.Scope.name == name).first()
#
## Additional functions for specific queries
#def get_goals_by_scope_id(db: Session, scope_id: int) -> List[models.Goal]:
#    return db.query(models.Goal).filter(models.Goal.scope_id == scope_id).all()
#
#def get_actions_by_goal_id(db: Session, goal_id: int) -> List[models.Action]:
#    return db.query(models.Action).filter(models.Action.goal_id == goal_id).all()
#
#def get_timeline_events_by_action_id(db: Session, action_id: int) -> List[models.TimelineEvent]:
#    return db.query(models.TimelineEvent).filter(models.TimelineEvent.action_id == action_id).all()
#
## Functions for weekly planning
#def set_weekly_plan(db: Session, must_do_action_ids: List[int], optional_action_ids: List[int]) -> None:
#    # Reset is_must_do for all actions
#    db.query(models.Action).update({models.Action.is_must_do: False})
#    # Set is_must_do for must-do actions
#    db.query(models.Action).filter(models.Action.id.in_(must_do_action_ids)).update({models.Action.is_must_do: True}, synchronize_session=False)
#    db.commit()
#
## Functions to retrieve timelines
#def get_goal_timeline(db: Session, goal_id: int) -> List[models.TimelineEvent]:
#    goal = get_by_id(db, models.Goal, goal_id)
#    if not goal:
#        return []
#    timeline_events = []
#    for action in goal.actions:
#        timeline_events.extend(action.timeline_events)
#    timeline_events.sort(key=lambda x: x.timestamp)
#    return timeline_events
#