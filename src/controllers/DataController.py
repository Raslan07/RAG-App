import os
import re

from fastapi import UploadFile
from fastapi.responses import JSONResponse

from models import ResponseSignal

from .BaseController import BaseController
from .ProjectController import ProjectController


class DataController(BaseController):
    """Upload concerns: file validation and unique destination paths.

    Relies on BaseController for settings, file_dir and random strings,
    and on ProjectController for the per-project directory.
    """

    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        """Check content type and (when known) size against settings.

        Returns a (is_valid, signal) tuple so the route can answer with a signal.
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED.value

        # UploadFile.size is None unless the client sent a Content-Length,
        # so this only guards when the size is actually known.
        if file.size is not None and file.size > self.app_settings.FILE_MAX_SIZE_MB * 1024 * 1024:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value

    def generate_unique_filename(self, original_filename: str, project_id: str):
        """Compute the full save path for a file inside its project folder.

        Regenerates the random prefix until the path does not exist on disk,
        so re-uploads never overwrite each other.
        """
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_filename(original_filename=original_filename)

        random_filename = self.generate_random_string(original_filename=original_filename, project_id=project_id)
        new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_filename)

        try:
            while os.path.exists(new_file_path):
                random_filename = self.generate_random_string(original_filename=original_filename, project_id=project_id)
                new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_filename)
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"signal": ResponseSignal.FILE_GENERATION_ERROR.value}
            )
        return new_file_path

    def get_clean_filename(self, original_filename: str) -> str:
        """Replace path-unsafe characters with '_' so the name is safe on disk."""
        cleaned_file_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', original_filename)
        return cleaned_file_name.strip()
