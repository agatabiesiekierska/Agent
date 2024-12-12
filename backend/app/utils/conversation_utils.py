from sqlmodel import Session, select
from database.models.users import Users
from database.models.conversations import Conversation
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

        # Create a new conversation
        new_conversation = Conversation(user_id=conversation.user_id)

        # Add the new conversation to the session
        session.add(new_conversation)

        # Commit the changes
        session.commit()

        # Refresh the new conversation with the database values
        session.refresh(new_conversation)

        # Load related data (messages)
        query = (
            select(Conversation.messages)
            .join(Conversation)
            .where(Conversation.conversation_id == new_conversation.id)
        )
        loaded_messages = session.exec(query).all()

        return {"conversation": new_conversation, "messages": loaded_messages}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating the conversation: {str(e)}")