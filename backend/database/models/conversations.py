from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime, text
from sqlmodel import SQLModel, Field, Relationship
import datetime

class Conversation(SQLModel, table=True):
    # Define the model for the conversation table in database
    conversation_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    model: str
    started_at: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
    ended_at: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

    message: list["Message"] = Relationship(back_populates="conversation")


class Sender(Enum):
    # Define the Sender enum class for the sender of the message
    USER = "user"
    MODEL = "model"   

class Message(SQLModel, table=True):
    # Define the model for the message table in database
    message_id: int = Field(default=None, primary_key=True)
    sender: Sender
    content: str
    timestamp: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

    conversation_id: int = Field(foreign_key="conversation.conversation_id")
    conversation: Conversation = Relationship(back_populates="message")