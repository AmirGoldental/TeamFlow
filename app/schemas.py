from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import enum

class ActionStatus(str, enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class EventBase(BaseModel):
    event_description: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ActionBase(BaseModel):
    description: str
    status: ActionStatus = ActionStatus.TODO
    is_must_do: bool = False

class ActionCreate(ActionBase):
    pass

class Action(ActionBase):
    id: int
    timeline_events: List[Event] = []

    class Config:
        orm_mode = True

class GoalBase(BaseModel):
    name: str

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    actions: List[Action] = []

    class Config:
        orm_mode = True

class ScopeBase(BaseModel):
    name: str

class ScopeCreate(ScopeBase):
    pass

class Scope(ScopeBase):
    id: int
    goals: List[Goal] = []

    class Config:
        orm_mode = True
