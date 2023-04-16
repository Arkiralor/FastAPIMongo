from fastapi import FastAPI

from controllers import authentication, users, default

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(default.router)




