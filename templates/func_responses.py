from fastapi.exceptions import HTTPException
from fastapi.responses import Response

class Resp:
    error:str=None
    message:str=None
    data:dict or str or int or bool=None
    status_code:int=None

    def __init__(self, error:str=None, message:str=None, data:dict or str or int or bool=None, status_code:int=None):
        if error:
            self.error = error
        if message:
            self.message = message
        if data:
            self.data=data
        if status_code:
            self.status_code = status_code

    def to_json(self):
        """
        Method to return the contents of the object as a JSON-like dictionary.
        """
        if type(self.data) == dict and not self.error:
            return self.data
        
        return {
            "error": self.error,
            "message": self.message,
            "data": self.data
        }
    
    def to_response(self):
        """
        Method to construct a framework `response` from the contents of the object.
        """
        return Response(
            content=self.to_json(),
            status_code=self.status_code
        )
    
    def text(self):
        """
        Method to contrustc a plaintext `response` from the contents of the object.
        To be used in cases of errors.
        """
        return Response(
            content=f"{self.error.upper()}:\t{self.message}",
            status_code=self.status_code,
            media_type="text/plain"
        )
    
    def exception(self):
        """
        Method to contruct a `HttpException` from the contents of the object.
        To be used in case of errors in FastApi, since it raises exceptions in case of errors and does not
        return a `HttpResponse`.
        """
        return HTTPException(
            status_code=self.status_code,
            detail=f"{self.error.upper()}:\t{self.message}"
        )
    

