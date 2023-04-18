from datetime import datetime, date, timedelta

from fastapi import status

from database import db
from database.collections import DatabaseCollections
from schema.location_schema import CountrySchema, UpdateCountrySchema, ShowStateProvinceSchema, UpdateStateProvinceSchema
from schema.user_choices import UserModelChoices
from schema.user_schema import ShowUserSchema
from templates.func_responses import Resp


class CountryUtils:

    ITEMS_PER_PAGE: int = 10
    MAX_RESULTS: int = 10_000

    @classmethod
    async def get(cls, id: str = None, name: str = None, official_name: str = None, *args, **kwargs) -> dict:
        if id and not name and not official_name:
            country = await db[DatabaseCollections.countries].find_one(
                {
                    "_id": id
                }
            )
        elif not id and name and not official_name:
            country = await db[DatabaseCollections.countries].find_one(
                {
                    "name": name.title()
                }
            )
        elif not id and not name and official_name:
            country = await db[DatabaseCollections.countries].find_one(
                {
                    "official_name": official_name
                }
            )
        else:
            country = None

        return country

    @classmethod
    async def create(cls, data: dict = None, user: ShowUserSchema = None, *args, **kwargs)->Resp:
        resp = Resp()

        if not user.user_type == UserModelChoices.admin:
            resp.error = "Unauthorised"
            resp.message = "Only admins are allowed to do this."
            resp.status_code = status.HTTP_401_UNAUTHORIZED

            return resp

        existing_country = await cls.get(official_name=data.get('official_name'))
        if existing_country:
            resp.error = "Duplicate Entity"
            resp.message = f"Country with name: '{data.get('name')}' and official name: '{data.get('official_name')}' already exists."
            resp.data = existing_country
            resp.status_code = status.HTTP_400_BAD_REQUEST

            return resp
        data["created"] = datetime.now()
        new_country = await db[DatabaseCollections.countries].insert_one(data)
        created_country = await cls.get(id=new_country.inserted_id)

        resp.message = f"New country {created_country.get('_id')}. '{created_country.get('official_name')}' created successfully."
        resp.data = created_country
        resp.status_code = status.HTTP_201_CREATED

        return resp

    @classmethod
    async def search(cls, name: str, official_name: str, country_code: str, internet_tld: str, isd: str, page: int, term: str, *args, **kwargs) -> list:

        if term and term != "":
            countries = await db[DatabaseCollections.countries].find(
                {
                    "$or": [
                        {
                            "name": term
                        },
                        {
                            "official_name": term
                        },
                        {
                            "country_code": term
                        },
                        {
                            "internet_tld": term
                        },
                        {
                            "isd": term
                        }
                    ]
                }
            ).skip(cls.ITEMS_PER_PAGE*(page-1) if (page-1) <= 0 else 0).limit(cls.ITEMS_PER_PAGE).to_list(cls.MAX_RESULTS)
        else:
            countries = await db[DatabaseCollections.countries].find(
                {
                    "$or": [
                        {
                            "name": name
                        },
                        {
                            "official_name": official_name
                        },
                        {
                            "country_code": country_code
                        },
                        {
                            "internet_tld": internet_tld
                        },
                        {
                            "isd": isd
                        }
                    ]
                }
            ).skip(cls.ITEMS_PER_PAGE*(page-1) if (page-1) <= 0 else 0).limit(cls.ITEMS_PER_PAGE).to_list(cls.MAX_RESULTS)

        return countries


class StateProvinceUtils:
    ITEMS_PER_PAGE: int = 10
    MAX_RESULTS: int = 10_000

    @classmethod
    async def get(cls, pk:str=None, name:str=None, *args, **kwargs)->dict:
        if pk and not name:
            state = await db[DatabaseCollections.states].find_one(
                {
                    "_id": pk
                }
            )
        elif not pk and name:
            state = await db[DatabaseCollections.states].find_one(
                {
                    "name": name.title()
                }
            )
        else:
            state = None

        return state
    
    @classmethod
    async def create(cls, data:dict, user:ShowUserSchema=None, *args, **kwargs):
        resp = Resp()

        if not user.user_type == UserModelChoices.admin:
            resp.error = "Unauthorised"
            resp.message = "Only admins are allowed to do this."
            resp.status_code = status.HTTP_401_UNAUTHORIZED

            return resp
        
        country = await CountryUtils.get(name=data.get('country'))
        if not country:
            resp.error = "Country Invalid"
            resp.message = "This country is not recorded in our systems. Please create a new record for the country first."
            resp.status_code = status.HTTP_404_NOT_FOUND

            return resp
        
        existing_state = await cls.get(name=data.get('name'))
        if existing_state:
            resp.error = "Duplicate Entity"
            resp.message = f"Country with name: '{data.get('name')}' in: '{data.get('country')}' already exists."
            resp.data = existing_state
            resp.status_code = status.HTTP_400_BAD_REQUEST

            return resp
        
        data['country'] = country
        data['created'] = datetime.now()

        new_state = await db[DatabaseCollections.states].insert_one(data)
        created_state = await cls.get(pk=new_state.inserted_id)

        resp.message = f"New state: '{data.get('name')}' created for country: '{data.get('country', {}).get('name', '')}'."
        resp.data = created_state
        resp.status_code = status.HTTP_201_CREATED

        return resp        
        
        

    