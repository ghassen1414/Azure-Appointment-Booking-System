from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine # For table creation
from app.db.base_class import Base # For table creation

# This is a simple way to create tables for development.
# For production, you'd typically use Alembic for migrations.
def create_tables():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Consider whether to raise the error or just log it,
        # depending on whether app startup should fail if DB is not ready.

app = FastAPI(
    title="Appointment Booking System API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    create_tables() # Create tables on startup

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/") # Root path for basic health check or info
async def root():
    return {"message": "Welcome to the Appointment Booking System API!"}