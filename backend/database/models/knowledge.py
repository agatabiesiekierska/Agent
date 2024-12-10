import datetime
from sqlmodel import SQLModel, Column, DateTime, Field, text 
from typing import Optional


class Messages(SQLModel, table=True):
    article_id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    tags: str
    created_at: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )