from datetime import timedelta

from fastapi import status

from auth.hashing import Hashing
from auth.jwt import create_access_token, create_refresh_token
from auth.oauth_2 import get_current_user
from auth.utils import blacklist_token
from settings.config import settings
from schema.user_schema import ShowUserSchema
from templates.func_responses import Resp
from utils.user_utils import UserModelUtils

class AutheticationUtils:

    @classmethod
    async def login(cls, email:str=None, password:str=None, *args, **kwargs):
        resp = Resp()

        found_user = await UserModelUtils.find_user(email=email)

        if not found_user:
            resp.error = "Not Found"
            resp.message = f"User with email: '{email}' not found."
            resp.data = {
                "email": email
            }
            resp.status_code = status.HTTP_404_NOT_FOUND

            return resp
        
        if not Hashing.verify(password, found_user.get('password')):
            resp.error = "Incorrect Password"
            resp.message = f"Incorrect password for User: '{email}'."
            resp.data = {
                "email": email,
                "password": password
            }
            resp.status_code = status.HTTP_401_UNAUTHORIZED

            return resp
        
        access_token = create_access_token(
            data={
                "sub": found_user.get("email")
            }
        )
        refresh_token = create_refresh_token(
            data={
                "sub": found_user.get("email")
            }
        )

        resp.message = f"User: {email} authenticated successfully."
        resp.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
        resp.status_code = status.HTTP_200_OK

        return resp
    
    @classmethod
    async def logout(cls, user:ShowUserSchema, refresh:str, access:str):
        resp = Resp()
        access_check = blacklist_token(token=access)
        refresh_check = blacklist_token(token=refresh)

        if not access_check and not refresh_check:
            resp.error = "Could Not Blacklist Tokens"
            resp.message = f"Access: {access_check}; Refresh: {refresh_check}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return resp
        
        resp.message = "Tokens blacklisted successfully."
        resp.status_code = status.HTTP_200_OK

        return resp

    @classmethod
    async def refresh(cls, access_token:str=None, refresh_token:str=None, *args, **kwargs):
        resp = Resp()

        try:
            token_user = get_current_user(token=refresh_token)

            new_access_token = create_access_token(
                data={
                    "sub": token_user.email
                }
            )
            new_refresh_token = create_refresh_token(
                data={
                    "sub": token_user.email
                }
            )
        except Exception as ex:
            resp.error = "Could Not Refresh Tokens."
            resp.message = f"{ex}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return resp
        
        if access_token:
            access_check = blacklist_token(token=access_token)
            if not access_check:
                resp.error = "Could Not Blacklist Tokens"
                resp.message = f"Access: {access_check};"
                resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                return resp
            
        refresh_check = blacklist_token(token=refresh_token)
        if not refresh_check:
            resp.error = "Could Not Blacklist Tokens"
            resp.message = f"Refresh: {refresh_check}"
            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return resp

        resp.message = f"User: {token_user.email} authenticated successfully."
        resp.data = {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer"
        }
        resp.status_code = status.HTTP_200_OK

        return resp