## This is a main file that starts fastapi
import sys
sys.path.insert(0, r"D:\Python\Agent\backend") 
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Depends
from database.models import users
from database.db_setup import init_db
from contextlib import asynccontextmanager
from app.core import users, conversation
from dotenv import load_dotenv


#Load environmental variables in Agent folder
dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

@asynccontextmanager
async def lifespan( app: FastAPI):
    init_db()
    yield

# Starting an app
app = FastAPI(
    title = "Agent API",
    description = "API for communicating with AI models",
    version = "0.0.1"
)

app.include_router(users.router)
app.include_router(conversation.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Agent API"}


if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)