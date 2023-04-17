from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from auth.schema import Token, TokenInput, LogoutResponse
from auth.oauth_2 import get_current_user
from schema.user_schema import ShowUserSchema
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

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=LogoutResponse)
async def logout_controller(current_user: ShowUserSchema = Depends(get_current_user), data:TokenInput = Body(...)):
    data = jsonable_encoder(data)
    access = data.get("access_token", "")
    refresh = data.get("refresh_token", "")

    resp = await AutheticationUtils.logout(user=current_user, access=access, refresh=refresh)

    if resp.error:
        raise resp.exception()
    
    return resp.to_json()

@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
async def regenerate_tokens(data:TokenInput=Body(...)):
    data = jsonable_encoder(data)
    refresh = data.get("refresh_token", "")
    resp = await AutheticationUtils.refresh(refresh_token=refresh)

    if resp.error:
        raise resp.exception()
    
    return resp.data