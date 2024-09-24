from fastapi import FastAPI
from app.routers import scopes, goals, actions, events
from app.database import engine
from app import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Development Management API",
    description="API for managing scopes, goals, actions, and timelines",
    version="1.0.0",
)

# Include routers
app.include_router(scopes.router)
app.include_router(goals.router)
app.include_router(actions.router)
app.include_router(events.router)

