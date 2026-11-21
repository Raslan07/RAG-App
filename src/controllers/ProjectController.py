import os

from .BaseController import BaseController


class ProjectController(BaseController):
    """Owns the per-project folder layout under assets/files.

    Relies on BaseController for file_dir.
    """

    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str) -> str:
        """Return assets/files/<project_id>, creating the folder if it does not exist yet."""
        project_dir = os.path.join(self.file_dir, project_id)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir
