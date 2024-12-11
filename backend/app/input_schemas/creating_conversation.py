from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class ConversationCreate(SQLModel, table=False):
    user_id: int
    