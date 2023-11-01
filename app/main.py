from app.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from decouple import config

app = FastAPI(title=config("PROJECT_NAME"))

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix="/api_v1")

