from fastapi import FastAPI, APIRouter
import os


# prefix : /api/v1 this use for versioning of the API. It allows you to group related endpoints under a common path, making it easier to manage and maintain different versions of your API.

# tags : ["api_v1"] this is used for documentation purposes. It allows you to categorize and group related endpoints together in the automatically generated API documentation (e.g., Swagger UI). This makes it easier for developers to understand the purpose and functionality of different endpoints within your API.
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)



# Async : is used to define an asynchronous function. Asynchronous functions allow for non-blocking operations, which can improve the performance of your application, especially when dealing with I/O-bound tasks like database queries or network requests. In this case, the welcome function is defined as an asynchronous function to handle incoming requests without blocking the event loop.


@base_router.get("/")
async def welcome():
    app_name = os.getenv('APP_NAME')
    app_version  = os.getenv('APP_VERSION')

    return {
        "app_name": app_name,
        "app_version": app_version,
    }