import datetime
from sqlmodel import SQLModel, Column, DateTime, Field, text 
from typing import Optional


class Users(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    last_active: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
