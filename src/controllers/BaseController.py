import os
import random
import string

from helpers.config import get_settings, Settings


class BaseController:
    """Shared base for all controllers: app settings and the file storage root.

    Subclasses (DataController, ProjectController) reuse app_settings, file_dir
    and generate_random_string() via inheritance instead of duplicating them.
    """

    def __init__(self):
        self.app_settings: Settings = get_settings()
        # The src/ directory (parent of controllers/)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        # All uploaded files are stored under src/assets/files/<project_id>/
        self.file_dir = os.path.join(self.base_dir, "assets/files")

    def generate_random_string(self, original_filename: str, project_id: str) -> str:
        """Build a filename stem: <8 random chars>_<project_id>_<original name>."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + f"_{project_id}_" + original_filename
