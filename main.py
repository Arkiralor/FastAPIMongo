from fastapi import FastAPI, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from schema.user_schema import RegisterUserSchema, ShowUserSchema
from settings.config import settings
from utils.user_utils import UserModelUtils

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Hello world."}

@app.get("/api/config/")
async def read_config():
    return settings

@app.post("/api/user/signup/", response_model=ShowUserSchema, response_description="User created successfully.")
async def create_user(user:RegisterUserSchema=Body(...)):
    user = jsonable_encoder(user)
    resp = await UserModelUtils.create_user(data=user)

    if resp.error:
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.message
        )

    return JSONResponse(
            content=resp.data,
            status_code=resp.status_code
        )


