import datetime
from sqlmodel import SQLModel, Column, DateTime, Relationship, Field, text 
from typing import Optional
from conversations import Conversation

class Messages(SQLModel, table=True):
    message_id: int = Field(default=None, primary_key=True)
    sender: str
    content: str
    timestamp: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

    conversation_id: int = Field(foreign_key="Conversation.conversation_id")
    conversation: Conversation = Relationship(back_populates="messages")