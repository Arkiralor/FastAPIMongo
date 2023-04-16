from logging import exception
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from auth.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    return verify_token(token)