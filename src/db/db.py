# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Set up the SQLite database URI
db_path = "my_database.db"
db_uri = f"sqlite:///{db_path}"

# Initialize the engine
engine = create_engine(db_uri, connect_args={"check_same_thread": False})

# Create a base class for models
Base = declarative_base()

# Set up the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database tables
def init_db():
    import models  # Import models to ensure they are registered with Base
    Base.metadata.create_all(bind=engine)


