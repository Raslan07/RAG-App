from fastapi import APIRouter, Depends

from helpers import get_settings, Settings

# Versioned API root: all endpoints live under /api/v1 and are grouped
# under the "api_v1" tag in the auto-generated Swagger docs.
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    """Simple info endpoint: reports the app name and version from settings."""
    return {
        "app_name": app_settings.APP_NAME,
        "app_version": app_settings.APP_VERSION,
    }
