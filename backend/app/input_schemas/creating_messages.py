from sqlmodel import SQLModel
class NewMessage(SQLModel):
    # Define the model for new message
    conversation_id: int
    content: str
    
