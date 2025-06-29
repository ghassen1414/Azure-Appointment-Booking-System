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
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# ---- START CORS DEBUG ----
print("--- app/main.py: Initializing CORS Middleware ---")
print(f"Raw settings.BACKEND_CORS_ORIGINS from config: {settings.BACKEND_CORS_ORIGINS}")
print(f"Type of settings.BACKEND_CORS_ORIGINS: {type(settings.BACKEND_CORS_ORIGINS)}")

processed_origins = []
if settings.BACKEND_CORS_ORIGINS:
    if isinstance(settings.BACKEND_CORS_ORIGINS, list):
        # This branch should be hit if you used Option 1 (JSON string in .env)
        # and removed the custom validator in config.py
        processed_origins = [str(origin).rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS]
        print(f"Processing BACKEND_CORS_ORIGINS as a list of Pydantic AnyHttpUrl objects.")
    elif isinstance(settings.BACKEND_CORS_ORIGINS, str):
        # This branch would be hit if BACKEND_CORS_ORIGINS was still a plain string
        # (e.g., if Option 2 validator wasn't fully working or removed,
        # and .env had comma-separated string)
        print(f"Processing BACKEND_CORS_ORIGINS as a string: '{settings.BACKEND_CORS_ORIGINS}' - This might be incorrect if it's not a list of URLs.")
        # Attempt to split if it looks like a comma-separated list
        if ',' in settings.BACKEND_CORS_ORIGINS:
             processed_origins = [origin.strip().rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS.split(',')]
        elif settings.BACKEND_CORS_ORIGINS.strip(): # Single origin string
             processed_origins = [settings.BACKEND_CORS_ORIGINS.strip().rstrip('/')]

print(f"Final processed_origins for CORSMiddleware: {processed_origins}")
print(f"Types in processed_origins: {[type(o) for o in processed_origins]}")
print("--- END CORS DEBUG ---")
# ---- END CORS DEBUG ----

# Set all CORS enabled origins
# Ensure processed_origins is not empty if it's critical, or handle default
if processed_origins: # Only add middleware if we have valid origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=processed_origins,
        allow_credentials=True,
        allow_methods=["*"], 
        allow_headers=["*"], 
    )
else:
    print("WARNING: No valid CORS origins processed. CORSMiddleware NOT added or using default restrictive behavior.")

@app.on_event("startup")
async def startup_event():
    create_tables() # Create tables on startup

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/") # Root path for basic health check or info
async def root():
    return {"message": "Welcome to the Appointment Booking System API!"}