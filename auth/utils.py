from datetime import datetime

from fastapi.exceptions import HTTPException

from database.collections import DatabaseCollections
from database.direct_driver import py_db

def get_token_by_str(token:str=None)->dict:
    """
    Searches the database for a blacklisted token.
    """
    token = py_db[DatabaseCollections.blacklisted_tokens].find_one(
        {
            "token": token
        }
    )

    return token

def blacklist_token(token:str=None):
    blacklisted_exception = HTTPException(
            status_code=400,
            detail=f"Could not blacklist token."
        )
    if not token:
        return False
    
    if get_token_by_str(token=token):
        return True
    
    token_dict = {
        "token": token,
        "created": datetime.now()
    }

    try:
        blacklisted = py_db[DatabaseCollections.blacklisted_tokens].insert_one(token_dict)
        if not blacklisted.inserted_id:
            raise blacklisted_exception
        return True
    except Exception as ex:
        raise blacklisted_exception
