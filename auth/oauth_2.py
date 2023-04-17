import asyncio
from logging import exception
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from auth.jwt import verify_token
from database import db
from schema.user_schema import ShowUserSchema
from schema.user_choices import UserModelChoices
from utils.user_utils import UserModelUtils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        return verify_token(token)
    except Exception:
        raise credentials_exception
    