## This is a router with all functions realted to conversationm with OpenAi models

from fastapi import HTTPException, APIRouter, status, Depends
import logging
from pydantic import BaseModel
from scripts.completion import Completion
from app.core.config import settings

# Initialize the router
router = APIRouter()

# Import OpenAI API key
openai_api_key = settings.openai_api_key


# class for input of the user to "/generate script" endpoint
class script_instructions(BaseModel):
    instructions: str 
    language: str | None = 'Python'
   

# class for input of the user to "/summary" endpoint
class User_command_input(BaseModel):
    user_input: str

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


## POST method for summary of the given text
@router.post("/summary")
async def start_conversation(data: User_command_input):
    # Log the received data
    logging.info(f"Received user input: {data.user_input}")
    

## POST method for generating programming script
@router.post("/generate_script")
async def generate_script(data: script_instructions):
    # Log the received data
    logging.info(f"Received user input: {data.instructions}")
    
    # Generate the Completion object and call the generate_script method
    completion = Completion(openai_api_key)
    answer = completion.generate_script(data.instructions, data.language)
    
    # Log the output of the LLM
    logger.info(f"LLM response {answer}")
    return answer