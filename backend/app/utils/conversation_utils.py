from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database.models.users import Users
from database.models.conversations import Conversation, Messages
from app.input_schemas.creating_conversation import ConversationCreate
from fastapi import HTTPException, status

def get_conversation_id(session: Session, conversation_id: int):
    return session.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()


def start_new_conversation(conversation: ConversationCreate, session: Session):
    try:
        # Check if the user exists
        user = session.get(Users, conversation.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to call user. User not found!")

        # Validate the model name
        valid_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini"]  # Add more models as needed
        if conversation.model not in valid_models:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid model name")
        
        # Create a new conversation
        new_conversation = Conversation(user_id=conversation.user_id, model = conversation.model)

        # Add the new conversation to the session
        session.add(new_conversation)

        # Commit the changes
        session.commit()

        # Refresh the new conversation with the database values
        session.refresh(new_conversation)

        # Load related data (messages)
        loaded_messages = session.query(Messages).options(joinedload(Messages.conversation)).filter(
            Messages.conversation_id == new_conversation.conversation_id
        ).all()
        

        return {"conversation_id": new_conversation.conversation_id, "messages": loaded_messages}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating the conversation: {str(e)}")
