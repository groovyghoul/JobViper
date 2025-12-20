from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path for the database file relative to the script's location
DATABASE_URL = f"sqlite:///{os.path.join(script_dir, 'jobviper.db')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
