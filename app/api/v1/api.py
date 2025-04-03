from fastapi import APIRouter

from app.api.v1.endpoints import users

api_router = APIRouter()

# Import and include other routers here
# Example:
# from app.api.v1.endpoints import users
# api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(users.router, prefix="/users", tags=["users"])
