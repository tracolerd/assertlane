from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
SQLALCHEMY_DATABASE_URL = "sqlite:///./assertlane.db"
# SQLite-এর জন্য check_same_thread=False প্রয়োজন হয়, Postgres-এ লাগবে না
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
