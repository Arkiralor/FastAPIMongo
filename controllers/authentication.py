from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from utils.authentication_utils import AutheticationUtils

router = APIRouter(
    tags=['authentication']
)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_controller(request: OAuth2PasswordRequestForm=Depends()):
    email = request.username
    password = request.password

    resp = await AutheticationUtils.login(email=email, password=password)

    if resp.error:
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.message
        )
    
    return resp.data