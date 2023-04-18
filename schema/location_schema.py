from bson import ObjectId
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, List

from schema import PyObjectId


class CountrySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id")
    name: str = Field(...)
    official_name: str = Field(...)
    country_code: str = Field(...)
    internet_tld: str = Field(...)
    isd: str = Field(...)
    created: Optional[datetime]

    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }

        schema_extra = {
            "example": {
                "name": "India",
                "official_name": "The Republic of India",
                "country_code": "in",
                "internet_tld": ".in",
                "isd": "+91"
            }
        }


class UpdateCountrySchema(BaseModel):
    name: str = Field(...)
    official_name: str = Field(...)
    country_code: str = Field(...)
    internet_tld: str = Field(...)
    isd: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }


class CreateStateProvinceSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id")
    name: str = Field(...)
    state_code: Optional[str] = Field(...)
    country: str = Field(...)
    created: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }

        schema_extra = {
            "example": {
                "name": "Assam",
                "state_code": "as",
                "country": "India"
            }
        }

class ShowStateProvinceSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,
                           alias="_id")
    name: str = Field(...)
    state_code: Optional[str] = Field(...)
    country: CountrySchema = Field(...)
    created: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }

        schema_extra = {
            "example": {
                "name": "Assam",
                "state_code": "as",
                "country": "India"
            }
        }


class UpdateStateProvinceSchema(BaseModel):
    name: str = Field(...)
    state_code: str = Field(...)
    country: CountrySchema = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }
