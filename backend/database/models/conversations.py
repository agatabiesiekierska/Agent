import datetime
from sqlmodel import SQLModel, Column, DateTime, Relationship, Field, text 
from typing import Optional
from database.models.users import Users


class Conversation(SQLModel, table=True):
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

    messages: list["Messages"] = Relationship(back_populates="conversation")
    # user: Users = Relationship(back_populates="Conversation")


class Messages(SQLModel, table=True):
    message_id: int = Field(default=None, primary_key=True)
    sender: str
    content: str
    timestamp: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )

    conversation_id: int = Field(foreign_key="conversation.conversation_id")
    conversation: Conversation = Relationship(back_populates="messages")