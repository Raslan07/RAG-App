import string

from fastapi.responses import JSONResponse
from .ProjectController import ProjectController
from .BaseController import BaseController
from fastapi import  UploadFile
from models import ResponseSignal
import re
import os
# use dot before BaseController to indicate that it is in the same package as DataController. This is a relative import, which is a way to import modules that are in the same package or directory. It helps to avoid naming conflicts and makes the code more organized.

# if i wanna to call constructor of BaseController in DataController, i can use super().__init__() to call the constructor of the parent class (BaseController) and initialize the app_settings attribute.

# this is a good practice to use inheritance and create a base controller class that contains common functionality and attributes that can be shared across multiple controllers. This way, you can avoid code duplication and make your code more maintainable.

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self , file: UploadFile):

        # Validate the uploaded file's type and size based on the settings defined in the BaseController.
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            # raise ValueError(f"File type {file.content_type} is not allowed. Allowed types are: {self.app_settings.FILE_ALLOWED_TYPES}")
            return False , ResponseSignal.FILE_TYPE_NOT_ALLOWED.value

        # Check if the file size exceeds the maximum allowed size. Note that UploadFile does not have a size attribute by default, so you might need to read the file to determine its size. Here, we assume that the file object has a size attribute for demonstration purposes.

        if file.size is not None and file.size > self.app_settings.FILE_MAX_SIZE_MB * 1024 * 1024:
            # raise ValueError(f"File size {file.size} exceeds the maximum allowed size of {self.app_settings.FILE_MAX_SIZE_MB} MB")
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True , ResponseSignal.FILE_VALIDATION_SUCCESS.value

    def generate_unique_filename(self , original_filename:str , project_id:str):
        random_filename = self.generate_random_string(original_filename = original_filename , project_id = project_id)
        project_path = ProjectController().get_project_path(project_id = project_id)

        cleaned_filename = self.get_clean_filename(original_filename = original_filename)

        new_file_path = os.path.join(project_path , random_filename + "_" + cleaned_filename)

        try:
            while os.path.exists(new_file_path):
                random_filename = self.generate_random_string(original_filename = original_filename , project_id = project_id)
                new_file_path = os.path.join(
                    project_path , random_filename + "_" + cleaned_filename
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"signal": ResponseSignal.FILE_GENERATION_ERROR.value}
            )
        return new_file_path


    def get_clean_filename(self , original_filename:str):
        # Remove any unwanted characters from the filename to ensure it's safe for use in file paths.
        # You can customize this function based on your requirements.
        cleaned_file_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', original_filename)

        cleaned_file_name = cleaned_file_name.strip()  # Remove leading and trailing whitespace
        
        return cleaned_file_name
