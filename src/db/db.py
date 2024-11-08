from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_path = "my_database.db"
db_uri = f"sqlite:///{db_path}"

engine = create_engine(db_uri, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()