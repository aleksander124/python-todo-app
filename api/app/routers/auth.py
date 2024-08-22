import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from dependencies.auth import get_current_user, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from crud.users import create_user, get_user as crud_get_user, get_users as crud_get_users, delete_user as crud_delete_user
from schemas.users import UserCreate, User
from schemas.token import Token
from dependencies.db_connect import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Authenticating user")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info("User authenticated successfully")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create-user/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if "@" not in user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
    logger.info("Creating new user")
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/users/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching items with skip={skip} and limit={limit}")
    users = crud_get_users(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting user with id {user_id}")
    db_user = crud_delete_user(db=db, user_id=user_id)
    if db_user is None:
        logger.error("User not found for deletion", extra={"user_id": user_id})
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
