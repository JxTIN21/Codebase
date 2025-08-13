from pydantic import BaseModel
from typing import Optional

class CodebaseCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CodebaseResponse(BaseModel):
    codebase_id: str
    status: str
    files_processed: int
    total_files: int
    message: str