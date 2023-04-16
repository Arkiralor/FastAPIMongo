from datetime import datetime

from fastapi import status

from auth.hashing import Hashing
from database import db
from settings.constants import GlobalConstants
from schema.user_choices import UserModelChoices
from templates.func_responses import Resp

class UserModelUtils:

    @classmethod
    async def create_user(cls, data:dict=None, *args, **kwargs):
        resp = Resp()

        username = data.get("username")
        email = data.get("email")
        existing_users = await cls.find_user(username=username, email=email)
        if existing_users:
            resp.error = "User Exists."
            resp.message = f"User with username: '{username}' and email: '{email}' already exists."
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

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

            return resp
        
        
        created_user["date_of_joining"] = created_user.get("date_of_joining").strftime("%Y-%m-%dT%H:%M:%S %Z%z")
        if "password" in created_user.keys():
            del created_user["password"]
        if created_user.get("regnal_number") and created_user.get("regnal_number") != 0:
            created_user["regnal_number"] = GlobalConstants.REGNAL_NUMBERS.get(created_user.get('regnal_number'))


        resp.message = f"User {data.get('username')} created for email: {data.get('email')}."
        resp.data = created_user
        resp.status_code = status.HTTP_201_CREATED

        return resp
    
    @classmethod
    async def find_user(cls, username:str=None, email:str=None, *args, **kwargs):
        if username and not email:
            users = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "username": username
                }
            )
        elif not username and email:
            users = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "email": email
                }
            )

        else:
            users = await db[UserModelChoices.COLLECTION].find_one(
                {
                    "username": username,
                    "email": email
                }
            )

        return users

