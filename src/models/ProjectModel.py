from typing import Any , cast

from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DatabaseEnum import DatabaseEnum
class ProjectDataModel(BaseDataModel):
    def __init__(self, db_clint: Any):
        super().__init__(db_clint=db_clint)
        self.collection = cast(Any, self.db_clint)[DatabaseEnum.COLLECTION_PROJECT_NAME.value]

# Old (Pydantic v1 - deprecated)
# result = project.dict()

# New (Pydantic v2)
# result = project.model_dump()

    async def create_project(self, project : Project ):
        result = await self.collection.insert_one(project.model_dump())
        project._id = result.inserted_id
        return project

    async def get_project_or_create_one(self,project_id:str):
    
