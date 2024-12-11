from sqlmodel import Session
from database.models.users import Users
from database.models.conversations import Conversation
from app.input_schemas.creating_conversation import ConversationCreate
from fastapi import HTTPException

def get_conversation_id(session: Session, conversation_id: int):
    return session.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()


def start_new_conversation(conversation: ConversationCreate, session: Session):
    # Check if the user exists
    user = session.get(Users, conversation.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Failed to call user")

    # Create a new conversation
    new_conversation = Conversation(user_id=conversation.user_id)

    # Add the new conversation to the session
    session.add(new_conversation)

    # Commit the changes
    session.commit()

    # Refresh the new conversation with the database values
    session.refresh(new_conversation)

    # Load related data (messages)
    session.exec(select(Conversation.messages).where(Conversation.conversation_id == new_conversation.id))

    return new_conversation