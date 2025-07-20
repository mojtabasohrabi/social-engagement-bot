from fastapi import APIRouter
from app.api.v1.endpoints import users, profiles, alerts

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
