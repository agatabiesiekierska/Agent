## This is a router with all classes and methods realted to users
from fastapi import HTTPException, APIRouter, status, Depends
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to call user: {str(e)}")
    
# GET method for receiving list of users
@router.get("/users", response_model=List[Users])
async def call_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    try:    
        users = get_users(session = session, skip = skip, limit = limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to call user: {str(e)}")


# POST method for creating new user - if the user already exists, it will return an Exeption
@router.post("/users", status_code = status.HTTP_201_CREATED)
async def create_new_user(user: Users, session: Session = Depends(get_session)):
    try:
        if_user_exists = get_user_by_email(session=session, email = user.email)
        
        if if_user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists!")
        
        return create_user(session=session, user=user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create user: {str(e)}")

# DELETE method for deleting user with specific ID    
@router.post("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    try:
        # Find the user by ID
        user = get_user(session=session, user_id=user_id)
        
        # Delete the user
        session.delete(user)
        await session.commit()
        
        return {"message": f"User with ID {user_id} deleted successfully"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found or failed to delete: {str(e)}"
        )
