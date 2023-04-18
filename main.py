from fastapi import FastAPI

from controllers import authentication, users, default, locations

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(default.router)
app.include_router(locations.router)




