from fastapi import FastAPI

from .api import router

print("app")

app = FastAPI()
app.include_router(router)
