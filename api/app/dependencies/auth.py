from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from passlib.context import CryptContext
from app.crud.users import get_user_by_username
from app.schemas.token import TokenData
from app.dependencies.db_connect import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    if not user.is_active:
        # You can either return False or raise an HTTP exception here
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"JWT payload: {payload}")
        username: str = payload.get("sub")

        if username is None:
            print("Username not found in token")
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        print(f"User with username {token_data.username} not found")
        raise credentials_exception

    print(f"Authenticated user: {user.username}")
    return user


async def get_current_superuser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    superuser_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions"
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"JWT payload: {payload}")
        username: str = payload.get("sub")

        if username is None:
            print("Username not found in token")
            raise credentials_exception

        # Create TokenData object
        token_data = TokenData(username=username)
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

    # Retrieve user from database
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        print(f"User with username {token_data.username} not found")
        raise credentials_exception

    # Check if the user is a superuser
    if not user.is_superuser:
        print(f"User {user.username} is not a superuser")
        raise superuser_exception

    print(f"Authenticated superuser: {user.username}")
    return user