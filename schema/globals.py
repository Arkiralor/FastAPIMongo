from bson import ObjectId
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List

from schema.user_schema import ShowUserSchema

class DatabaseDumpSchema(BaseModel):
    users:Optional[List[ShowUserSchema]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            date: str,
            datetime: str
        }