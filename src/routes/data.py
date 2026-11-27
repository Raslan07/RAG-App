import logging

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from routes.schemes.data import ProcessRequest
from controllers import DataController, ProjectController , ProcessController
from helpers.config import get_settings, Settings
from models import ResponseSignal

logger = logging.getLogger("uvicorn.error")

# Upload API, mounted at /api/v1/data/*
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    """Upload a file for a given project.

    Steps: validate the file -> compute a unique destination path
    -> stream the file to disk in chunks.
    """
    data_controller = DataController()

    # 1. Reject bad files before they touch the disk
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )

    if file.filename is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": "Uploaded file has no filename"}
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    # 2. Build the unique save path (also creates the project folder if needed)
    generated_filename = data_controller.generate_unique_filepath(
        original_filename=file.filename, 
        project_id=project_id
        )
    
    if isinstance(generated_filename, JSONResponse):
        return generated_filename

    file_path, file_id = generated_filename

    # 3. Stream to disk chunk by chunk so large files never sit fully in memory
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
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value ,
            "file_id": file_id}
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, request: ProcessRequest):
    """Endpoint to trigger processing of a file for a given project.

    This is a placeholder for the actual processing logic.
    """
    # Here you would implement the logic to process the file based on the request parameters.
    # For now, we just return a success response with the received parameters.

    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size
    if chunk_size is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value}
        )
    if overlap_size is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"signal": ResponseSignal.PROCESSING_FAILED.value}
            )

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)

    if file_content is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value}
        )
    file_chunks = process_controller.process_file_content(
        file_content=list(file_content),
        file_id =file_id,
         chunk_size=chunk_size,
          overlap_size=overlap_size )



    if file_chunks is None or len(file_chunks) == 0 :
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content ={
                "signal" : ResponseSignal.PROCESSING_FAILED.value
            }
        )
    
    return file_chunks