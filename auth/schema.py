from bson import ObjectId
from datetime import datetime
from schema import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BlacklistedToken(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    token: str
    created: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: str
        }

class TokenInput(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]

class LogoutResponse(BaseModel):
    error:Optional[str]
    message:Optional[str]
    data:Optional[dict]