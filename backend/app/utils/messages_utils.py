from sqlmodel import Session
from database.models.conversations import Conversation, Message
from fastapi import HTTPException, status
from app.input_schemas.creating_messages import NewMessage


def get_message_id(session: Session, message_id: int):
    # Function that gets a message by its id
    return session.query(Message).filter(Message.message_id == message_id).first()


def add_new_message(message: Message, session: Session):
    """
    Adds a new message to the database.
    Args:
        message (NewMessage): The message object containing the details of the new message.
        session (Session): The database session used to interact with the database.
    Returns:
        dict: A dictionary containing the conversation ID, sender and content of the new message.
    Raises:
        HTTPException: If the conversation is not found or if an error occurs while creating the message.
    """
    try:
        # Check if the conversation exists
        conversation = session.get(Conversation, message.conversation_id)
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to find conversation. Conversation not found!")
        
        # Create a new message
        #new_message = Message(conversation_id=message.conversation_id, sender = message.sender,  content=message.content)

        # Add the new message to the database
        session.add(message)
        session.commit()
        session.refresh(message)
        
        return {"conversation_id": message.conversation_id, "sender": message.sender, "content": message.content}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating the message: {str(e)}")

