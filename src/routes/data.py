from fastapi import FastAPI, APIRouter ,Depends , UploadFile , status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController
from models import ResponseSignal
import aiofiles
import logging

logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1" , "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    # Here, you can implement the logic to handle the uploaded file and associate it with the specified project_id.
    # For example, you might want to save the file to a specific location or process its contents.
    
    # For demonstration purposes, let's just return some information about the uploaded file and project_id.
    data_controller = DataController()
    is_valid , result_signal = data_controller.validate_uploaded_file(file = file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )

    project_dir_path = ProjectController().get_project_path(project_id = project_id)


    if file.filename is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": "Uploaded file has no filename"}
        )

    file_path = data_controller.generate_unique_filename(original_filename = file.filename , project_id = project_id)
    if isinstance(file_path, JSONResponse):
        return file_path
    try:
         async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error occurred while saving the file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_GENERATION_ERROR.value}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value}
    )

