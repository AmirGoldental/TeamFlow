from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class ActionStatus(enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Scope(Base):
    __tablename__ = 'scopes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    goals = relationship('Goal', back_populates='scope')

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    scope_id = Column(Integer, ForeignKey('scopes.id'))
    scope = relationship('Scope', back_populates='goals')
    actions = relationship('Action', back_populates='goal')

class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(Enum(ActionStatus), default=ActionStatus.TODO)
    is_must_do = Column(Boolean, default=False)
    goal_id = Column(Integer, ForeignKey('goals.id'))
    goal = relationship('Goal', back_populates='actions')
    timeline_events = relationship('TimelineEvent', back_populates='action')

class TimelineEvent(Base):
    __tablename__ = 'timeline_events'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_description = Column(String)
    action_id = Column(Integer, ForeignKey('actions.id'))
    action = relationship('Action', back_populates='timeline_events')
