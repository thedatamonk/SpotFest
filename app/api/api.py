from fastapi import APIRouter
from app.api.endpoints import login, events, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(events.router, tags=["events"])
api_router.include_router(users.router, tags=["users"])

# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])