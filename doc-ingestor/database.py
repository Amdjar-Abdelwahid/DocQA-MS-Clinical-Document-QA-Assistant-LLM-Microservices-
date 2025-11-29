from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion au Postgres défini dans le Docker Compose
# On remplace 5432 par 5433
SQLALCHEMY_DATABASE_URL = "postgresql://admin:adminpassword@127.0.0.1:5433/ingestion_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()