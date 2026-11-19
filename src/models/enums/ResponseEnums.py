from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATION_SUCCESS = "Successfully validated the uploaded file."
    FILE_VALIDATION_FAILURE = "Failed to validate the uploaded file."
    FILE_TYPE_NOT_ALLOWED = "File type is not allowed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size."
    FILE_UPLOAD_SUCCESS = "Successfully uploaded the file."
    FILE_FAILURE_SUCCESS = "Failed to upload the file."
    FILE_GENERATION_ERROR = "Error occurred while generating a unique filename."
