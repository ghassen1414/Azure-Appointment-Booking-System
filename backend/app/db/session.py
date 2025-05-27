from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# For Azure SQL (SQL Server)
# Ensure you have pyodbc installed and the correct ODBC driver
# Example: settings.DATABASE_URL = "mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(settings.DATABASE_URL) # Add pool_pre_ping=True for production
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()