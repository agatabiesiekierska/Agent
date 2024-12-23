from sqlmodel import SQLModel

class NewUser(SQLModel):
    # Define the model for new message
    username: str
    email: str