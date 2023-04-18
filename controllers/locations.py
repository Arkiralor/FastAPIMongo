from typing import List

from fastapi import APIRouter, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.responses import Response, JSONResponse

from auth.oauth_2 import get_current_user
from schema.user_schema import ShowUserSchema
from schema.location_schema import CountrySchema, UpdateCountrySchema, ShowStateProvinceSchema, UpdateStateProvinceSchema, CreateStateProvinceSchema
from utils.location_utils import CountryUtils, StateProvinceUtils

router = APIRouter(
    prefix='/location',
    tags=['locations']
)

@router.get("/country/{term}/{term_type}/", response_model=CountrySchema, status_code=status.HTTP_200_OK)
async def get_one_country(term:str, term_type:str, user:ShowUserSchema=Depends(get_current_user)):
    if term_type == "id":
        resp = await CountryUtils.get(id=term)
    elif term_type == "name":
        resp = await CountryUtils.get(name=term)
    elif term_type == "official_name":
        resp = await CountryUtils.get(official_name=term)
    else:
        resp = {
                "_id": None,
                "name": None,
                "official_name": None,
                "country_code": None,
                "internet_tld": None,
                "isd": None
            }
        
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found."
        )
        
    return resp

@router.post("/country/add/", response_model=CountrySchema, status_code=status.HTTP_201_CREATED)
async def create_country(data:CountrySchema = Body(...), user:ShowUserSchema=Depends(get_current_user)):
    data = jsonable_encoder(data)
    resp = await CountryUtils.create(data=data, user=user)

    if resp.error:
        raise resp.exception()
    
    return resp.data

@router.post("/state/add/", response_model=ShowStateProvinceSchema, status_code=status.HTTP_201_CREATED)
async def create_state(data:CreateStateProvinceSchema = Body(...), user:ShowUserSchema=Depends(get_current_user)):
    data = jsonable_encoder(data)
    resp = await StateProvinceUtils.create(data=data, user=user)

    if resp.error:
        raise resp.exception()
    
    return resp.data