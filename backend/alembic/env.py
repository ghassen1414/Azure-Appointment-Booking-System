import os
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine # Added create_engine
from sqlalchemy import pool

from alembic import context

# Import your Base from your application
from app.db.base_class import Base

# --- Load .env file ---
# Construct path to .env file from the location of env.py
# env.py is in backend/alembic, .env is in backend/
DOTENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(DOTENV_PATH):
    print(f"Alembic env.py: Loading .env from {DOTENV_PATH}")
    load_dotenv(DOTENV_PATH)
else:
    print(f"Alembic env.py: .env file not found at {DOTENV_PATH}, ensure DATABASE_URL is set in environment.")

# Retrieve the database URL from environment variables
# This variable MUST be set in your .env file or system environment
ACTUAL_DATABASE_URL = os.getenv("DATABASE_URL")
if not ACTUAL_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please define it in your .env file or environment.")
# --- End .env loading ---

config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata for autogenerate
target_metadata = Base.metadata

# Ensure your models are imported so Base.metadata is populated
from app.models.user import User
from app.models.appointment import Appointment
# ... any other models ...

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Use the ACTUAL_DATABASE_URL loaded from environment
    context.configure(
        url=ACTUAL_DATABASE_URL,  # <<< USE THE LOADED URL
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create engine directly with the ACTUAL_DATABASE_URL
    connectable = create_engine(ACTUAL_DATABASE_URL) # <<< USE THE LOADED URL

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()