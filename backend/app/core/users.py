## This is a router with all classes and methods realted to users
from fastapi import HTTPException, Depends, APIRouter
from database.models.users import Users
from typing import List
from sqlmodel import Session
from database.db_setup import get_session
from utils.user_utils import get_user, get_user_by_email, get_users, create_user

router = APIRouter()

# GET method for receiving user by id
@router.get("/users/{user_id}", response_model=Users)
async def call_user_by_id(user_id: int, session: Session = Depends(get_session)):
    try:
        user = get_user(session = session, user_id = user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to call user: {str(e)}")
    
# GET method for receiving list of users
@router.get("/users", response_model=List[Users])
async def call_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    try:    
        users = get_users(session = session, skip = skip, limit = limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to call user: {str(e)}")


# POST method for creating new user - if the user already exists, it will return an Exeption
@router.post("/users")
async def create_new_user(user: Users, session: Session = Depends(get_session)):
    try:
        if_user_exists = get_user_by_email(session=session, email = user.email)
        
        if if_user_exists:
            raise HTTPException(status_code=400, detail=f"User already exists!")
        
        return create_user(session=session, user=user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")
    


