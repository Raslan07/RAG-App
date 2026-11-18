from fastapi import FastAPI
from dotenv import load_dotenv

# load_dotenv is used to load environment variables from a .env file into the application. This allows you to manage configuration settings (like app name and version) in a separate file, making it easier to change these settings without modifying the code directly.
load_dotenv(".env")

from routes import base

app = FastAPI()

# include_router is used to include the routes defined in the base module into the main FastAPI application. This allows the endpoints defined in base.py to be accessible under the specified prefix ("/api/v1") and tags (["api_v1"]).

app.include_router(base.base_router)