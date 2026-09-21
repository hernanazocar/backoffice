from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentes.db")

# Para desarrollo local con SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )
else:
    # Para producción con PostgreSQL
    engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
