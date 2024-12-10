from sqlmodel import SQLModel, Session, create_engine
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


engine = create_engine(
    os.getenv("SQL_DATABASE_URL"), echo = True
    )

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
