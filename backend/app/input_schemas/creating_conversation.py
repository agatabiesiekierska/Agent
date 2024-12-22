from sqlmodel import SQLModel
class ConversationCreate(SQLModel, table=False):
    user_id: int
    model: str
    