from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        """Get the file extension for a given file ID."""
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self , file_id: str):
        """Get the appropriate file loader based on the file extension."""
        
        file_extension = self.get_file_extension(file_id)

        file_path = os.path.join(self.project_path, file_id)

        if file_extension == ProcessingEnum.TEXT.value:
            return TextLoader(file_path ,encoding= "utf-8")
        elif file_extension in [ProcessingEnum.PDF.value]:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

    def get_file_content(self , file_id:str):
        laoder = self.get_file_loader(file_id= file_id)
        return laoder.lazy_load()

    def process_file_content(self , file_content:list  , file_id : str , chunk_size:int = 100 , overlap_size:int = 20):
        """Process the file content by splitting it into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        file_content_texts =[
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata =[
            rec.metadata
            for rec in file_content
        ]


        chunks = text_splitter.create_documents(
            file_content_texts ,
            metadatas= file_content_metadata
        )
        return chunks