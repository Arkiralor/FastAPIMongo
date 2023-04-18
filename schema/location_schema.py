from bson import ObjectId
from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, List

from schema import PyObjectId


class CountrySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id", allow_mutation=False)
    name: str = Field(...)
    official_name: str = Field(...)
    internet_tld: str = Field(...)
    isd: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }


class UpdateCountrySchema(BaseModel):
    name: str = Field(...)
    official_name: str = Field(...)
    internet_tld: str = Field(...)
    isd: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }


class StateProvinceSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id", allow_mutation=False)
    name: str = Field(...)
    country: CountrySchema = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }


class UpdateStateProvinceSchema(BaseModel):
    name: str = Field(...)
    country: CountrySchema = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }
