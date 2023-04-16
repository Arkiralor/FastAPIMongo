from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.exceptions import HTTPException

from auth.oauth_2 import get_current_user
from schema.user_schema import ShowUserSchema
from settings.config import settings
from utils.user_utils import UserModelUtils


router = APIRouter(
    prefix='/test',
    tags=['test']
)

@router.get("/")
async def index():
    return {"message": "Hello world."}

@router.get("/config/")
async def read_config(current_user: ShowUserSchema = Depends(get_current_user)):
    active_user:ShowUserSchema = await UserModelUtils.find_user(email=current_user.email)
    if not active_user.get('username').lower().startswith("arkiralor"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only arkiralor and his accounts can view this."
        )
    return settings