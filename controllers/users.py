from typing import List

from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.responses import Response, JSONResponse

from auth.oauth_2 import get_current_user
from schema.user_schema import ShowUserSchema, RegisterUserSchema
from utils.user_utils import UserModelUtils

from controllers import logger

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.get("/all/", response_model=List[ShowUserSchema], status_code=status.HTTP_200_OK)
async def get_all_users(current_user: ShowUserSchema = Depends(get_current_user)):
    active_user: ShowUserSchema = await UserModelUtils.find_user(email=current_user.email)

    logger.info(f" accessed by {active_user.get('email')}")

    resp = await UserModelUtils.list_all(user=active_user)

    if resp.error:
        raise resp.exception()

    return resp.data


@router.post("/signup/", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterUserSchema = Body(...)):
    user = jsonable_encoder(user)
    resp = await UserModelUtils.create_user(data=user)

    if resp.error:
        raise resp.exception()

    return resp.data


@router.get("/self/", response_model=ShowUserSchema, status_code=status.HTTP_200_OK)
async def get_self_user(current_user: ShowUserSchema = Depends(get_current_user)):
    resp = await UserModelUtils.show_self(auth_user=current_user)

    if resp.error:
        raise resp.exception()

    return resp.data
