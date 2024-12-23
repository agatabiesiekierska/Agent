from sqlmodel import Session
from database.models.users import Users
from app.input_schemas.creating_users import NewUser


def get_user(session: Session, user_id: int):
    return session.query(Users).filter(Users.user_id == user_id).first()

def get_user_by_username(session: Session, username: str):
    return session.query(Users).filter(Users.username == username).first()

def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(Users).offset(skip).limit(limit).all()

def create_user(session: Session, user: NewUser):

    # Create a new user object
    new_user = Users(username=user.username, email=user.email)
            
    # Add the user to the session
    session.add(new_user)
            
    # Commit the changes to the database
    session.commit()
            
    # Refresh the user object with the database values
    session.refresh(new_user)
            
    return new_user
        