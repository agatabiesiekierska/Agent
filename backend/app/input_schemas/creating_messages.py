from sqlmodel import SQLModel

# from sqlalchemy.orm import registry
# mapper_registry = registry()
# @mapper_registry.mapped

class NewMessage(SQLModel, table=False):
    conversation_id: int
    sender: str
    content: str
    
