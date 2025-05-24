from fastapi import APIRouter
from app.api.v1.endpoints import users, appointments # appointments will be added soon

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
# TODO: Uncomment when appointments.py is created
# api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])