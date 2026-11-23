from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Startup function
    settings = get_settings()
    mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)

    try:
        app.state.mongo_conn = mongo_conn
        app.state.dp_client = mongo_conn[settings.MONGODB_DATABASE]
        yield
        # shutdown function
    finally:
        mongo_conn.close()


app = FastAPI(lifespan=lifespan)

# Mount both routers: base_router serves /api/v1/, data_router serves /api/v1/data/*
app.include_router(base.base_router)
app.include_router(data.data_router)


