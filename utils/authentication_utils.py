from fastapi import status

from auth.hashing import Hashing
from auth.jwt import create_access_token
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

        resp.message = f"User: {email} authenticated successfully."
        resp.data = {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        resp.status_code = status.HTTP_200_OK

        return resp
