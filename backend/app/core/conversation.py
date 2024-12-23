from fastapi import HTTPException, APIRouter, status, Depends
import logging
from sqlmodel import Session
from database.db_setup import get_session
from app.core.config import settings
from database.models.conversations import Conversation, Message
from database.models.conversations import Sender
from app.input_schemas.creating_conversation import ConversationCreate
from app.input_schemas.creating_messages import NewMessage
from app.utils.conversation_utils import start_new_conversation, get_conversation_id
from app.utils.messages_utils import add_new_message
from app.utils.open_ai_utils import answer_question


# Initialize the router
router = APIRouter()

# Import OpenAI API key
openai_api_key = settings.openai_api_key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GET method for receiving conversation by id
@router.get("/conversation/{conversation_id}", response_model=Conversation)
async def find_conversation_by_id(conversation_id: int, session: Session = Depends(get_session)):
    try:
        conversation = get_conversation_id(session = session, conversation_id = conversation_id)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to call conversation: {str(e)}")


@router.post("/conversation_create")
async def start_conversation(conversation_in: ConversationCreate, session: Session = Depends(get_session)):
    try:
        new_conversation = start_new_conversation(conversation=conversation_in, session = session)
        return new_conversation
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to start conversation: {str(e)}") 

@router.post("/conversation/{conversation_id}")
async def continue_conversation(new_message: NewMessage, session: Session = Depends(get_session)):
    try:
        question = Message(conversation_id=new_message.conversation_id, sender = Sender('user'), content= {"question": new_message.content})
        add_question = add_new_message(question, session)
        conversation = session.get(Conversation, question.conversation_id)
        response_LLM = answer_question(new_message.content, conversation.model)
        response = Message(conversation_id=new_message.conversation_id, sender = Sender('model'), content=response_LLM)
        add_response = add_new_message(response, session)
        return add_response
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to call conversation: {str(e)}")


