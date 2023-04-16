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
        if type(self.data) == dict and not self.error:
            return self.data
        
        return {
            "error": self.error,
            "message": self.message,
            "data": self.data
        }
    
    def to_response(self):
        return Response(
            content=self.to_json(),
            status_code=self.status_code
        )
    
    def text(self):
        return Response(
            content=f"{self.error.upper()}:\t{self.message}",
            status_code=self.status_code,
            media_type="text/plain"
        )
    

