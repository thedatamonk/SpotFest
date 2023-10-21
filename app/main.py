from app.api.api import api_router
from fastapi import FastAPI
from decouple import config

app = FastAPI(title=config("PROJECT_NAME"))

app.include_router(api_router, prefix="/api_v1")

