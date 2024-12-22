from sqlmodel import Session
from database.models.users import Users
from database.models.conversations import Conversation, Messages
from app.input_schemas.creating_messages import NewMessage
from fastapi import HTTPException, status


def get_message_id(session: Session, message_id: int):
    return session.query(Messages).filter(Messages.message_id == message_id).first()


def add_new_message(message: NewMessage, session: Session):
    try:
        # Check if the conversation exists
        conversation = session.get(Conversation, message.conversation_id)
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to find conversation. Conversation not found!")
        
        # Check if the sender of the message is either LLM or user.
        user = session.get(Users, conversation.user_id)
        if message.sender != conversation.model and message.sender != user.username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown sender of the message!")
        
        # Create a new message
        new_message = NewMessage(conversation_id=message.conversation_id, sender = message.sender,  content=message.content)

        # Add the new message to the database
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        
        return {"conversation_id": new_message.conversation_id, "sender": new_message.sender, "content": new_message.content, "model": conversation.model}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating the message: {str(e)}")

