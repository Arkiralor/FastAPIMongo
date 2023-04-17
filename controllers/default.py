from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException

from auth.oauth_2 import get_current_user
from database import db
from schema.user_schema import ShowUserSchema
from schema.globals import DatabaseDumpSchema
from schema.user_choices import UserModelChoices
from settings.config import Settings, settings
from utils.user_utils import UserModelUtils


router = APIRouter(
    prefix='/test',
    tags=['test']
)

@router.get("/")
async def index():
    return {"message": "Hello world."}

@router.get("/config/", response_model=Settings, status_code=status.HTTP_200_OK)
async def read_config(current_user: ShowUserSchema = Depends(get_current_user)):
    active_user:dict = await UserModelUtils.find_user(email=current_user.email)
    active_user:ShowUserSchema = ShowUserSchema(**active_user)
    if not active_user.user_type == UserModelChoices.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only administrators can view this data."
            )
    return settings

@router.get("/database/dump", response_model=DatabaseDumpSchema, status_code=status.HTTP_202_ACCEPTED)
async def dump_database(current_user: ShowUserSchema = Depends(get_current_user)):
    active_user:dict = await UserModelUtils.find_user(email=current_user.email)
    active_user_obj:ShowUserSchema = ShowUserSchema(**active_user)
    if not active_user_obj.user_type == UserModelChoices.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only administrators can view this data."
        )
    users = await UserModelUtils.list_all(user=active_user, list_size=10_000)
    if users.error:
        raise users.exception()
    
    data = {
        "users": users.data
    }
    return data