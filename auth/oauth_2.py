from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.jwt import verify_token
from schema.user_schema import ShowUserSchema
from utils.user_utils import UserModelUtils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        token_data = verify_token(token=token)
        user_dict = UserModelUtils.get_user(email=token_data.email)
        user_obj = ShowUserSchema(**user_dict)
        return user_obj
    except Exception:
        raise credentials_exception
    