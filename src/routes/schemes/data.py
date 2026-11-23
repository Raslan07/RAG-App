from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    signal: str
    file_id: str
    process_type: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[bool] = False
    