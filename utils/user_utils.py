from datetime import datetime

from fastapi import status

from auth.hashing import Hashing
from database import db
from settings.constants import GlobalConstants
from schema.user_schema import ShowUserSchema
from schema.user_choices import UserModelChoices
from templates.func_responses import Resp

from utils import logger

class UserModelUtils:

    DEFAULT_LIST_SIZE:int = 10_000

    @classmethod
    async def create_user(cls, data:dict=None, *args, **kwargs):
        resp = Resp()

        email = data.get("email")
        existing_users = await cls.find_user(email=email)
        if existing_users:
            resp.error = "User Exists."
            resp.message = f"User with email: '{email}' already exists."
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)

            return resp


        data["password"] = Hashing.bcrypt(password=data.get('password'))
        data["date_of_joining"] = datetime.now()


        new_user = await db[UserModelChoices.COLLECTION].insert_one(data)
        created_user = await db[UserModelChoices.COLLECTION].find_one(
            {
                "_id": new_user.inserted_id
            }
        )

        if not created_user:
            resp.error = "Could not create user."
            resp.message = f"Could not create a new user with details {data}."
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)

            return resp

        resp.message = f"User {data.get('username')} created for email: {data.get('email')}."
        resp.data = created_user
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp
    
    @classmethod
    async def find_user(cls, pk:str=None, username:str=None, email:str=None, *args, **kwargs)->dict:
        if not pk and username and not email:
            user = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "username": username
                }
            )
        elif not pk and not username and email:
            user = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "email": email
                }
            )

        elif pk and not username and not email:
            user = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "_id": pk
                }
            )

        else:
            user = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "username": username,
                    "email": email
                }
            )

        return user
    
    @classmethod
    async def list_all(cls, user=None, list_size:int=None):
        resp = Resp()
        if not user.get("_id"):
            resp.error = "Unauthorised"
            resp.message = "You need to be logged-in to view this."
            resp.status_code = status.HTTP_401_UNAUTHORIZED

            return resp
        
        if not list_size:
            list_size = cls.DEFAULT_LIST_SIZE
        users = await db[UserModelChoices.COLLECTION].find().to_list(list_size)

        resp.data = users
        resp.status_code = status.HTTP_200_OK

        return resp

    @classmethod
    async def show_self(cls, auth_user:ShowUserSchema, *args, **kwargs):
        resp = Resp()
        self_user = await cls.find_user(email=auth_user.email)

        if not self_user:
            resp.error = "Not Found"
            resp.message = f"User with email: '{auth_user.email}' not found."
            resp.status_code = status.HTTP_404_NOT_FOUND

            logger.warn(resp.message)
            return resp
        
        resp.message = f"User: '{self_user.get('email')}' found."
        resp.data = self_user
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp
        

