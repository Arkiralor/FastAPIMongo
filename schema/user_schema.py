from bson import ObjectId
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

from schema import PyObjectId
from settings.constants import GlobalConstants

class RegisterUserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id",
                           description="User's unique ObjectId as defined as the DB.")

    username: str = Field(..., regex=GlobalConstants.USERNAME_REGEX_STR, description="User's username to be used in the system.")
    email: EmailStr = Field(..., description="User's email used for authentication and official communication.")
    password: str = Field(..., description="User's password, used for authentication.")

    first_name: Optional[str] = Field(..., description="User's IRL legal first name.")
    middle_name: Optional[List[str]] = Field(..., min_items=0, max_items=16, description="User's IRL legal middle name(s).")
    last_name: Optional[str] = Field(..., description="User's IRL legal last/sur/family name.")
    regnal_number: Optional[int] = Field(...)
    date_of_birth: Optional[date] = Field(...)

    # date_of_joining: Optional[datetime] = Field(...)

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
                "username": "arkiralor92",
                "email": "blake@example.com",
                "password": "Som3R4nd0mP4$$word",
                "first_name": "Blakely",
                "middle_name": [
                    "Philip",
                    "Dominique"
                ],
                "last_name": "Dohearthy",
                "regnal_number": 3,
                "date_of_birth": "1992-02-14"
            }
        }


class UpdateUserSchema(BaseModel):
    first_name:Optional[str]
    midlle_name:Optional[List[str]]
    last_name:Optional[str]
    regnal_number:Optional[int]
    date_of_birth:Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }

        schema_extra = {
            "example": {
                "first_name": "Blakely",
                "middle_name": [
                    "Philip",
                    "Dominique"
                ],
                "last_name": "Dohourthy",
                "regnal_number": 3,
                "date_of_birth": "1992-02-14"
            }
        }


class ShowUserSchema(BaseModel):
    username:str
    email:str
    first_name:Optional[str]
    midlle_name:Optional[List[str]]
    last_name:Optional[str]
    regnal_number:Optional[int]
    date_of_birth:Optional[date]
    date_of_joining:Optional[datetime]