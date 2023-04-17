from datetime import datetime, timedelta
from fastapi import status, HTTPException
from typing import Optional
from jose import JWTError, jwt

from auth.schema import TokenData
from auth.utils import get_token_by_str
from settings.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(data:dict, expires_delta=timedelta(minutes=(settings.ACCESS_TOKEN_EXPIRE_MINUTES*338))):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    is_blacklisted = bool(get_token_by_str(token=token))
    if is_blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Blacklisted",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_email= payload.get('sub')
        
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(email=user_email)
        return token_data
    except JWTError:
        raise credentials_exception