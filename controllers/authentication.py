from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from auth.schema import Token
from utils.authentication_utils import AutheticationUtils

router = APIRouter(
    tags=['authentication']
)


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=Token)
async def login_controller(request: OAuth2PasswordRequestForm=Depends()):
    email = request.username
    password = request.password

    resp = await AutheticationUtils.login(email=email, password=password)

    if resp.error:
        raise resp.exception()
    
    return resp.data