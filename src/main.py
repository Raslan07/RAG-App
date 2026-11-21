from fastapi import FastAPI
from routes import base, data

app = FastAPI()

# Mount both routers: base_router serves /api/v1/, data_router serves /api/v1/data/*
app.include_router(base.base_router)
app.include_router(data.data_router)
