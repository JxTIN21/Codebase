from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    codebase_id: str
    query: str

class RelevantFile(BaseModel):
    file_path: str
    relevance_score: float
    snippet: str
    content: Optional[str] = None

class CodeExample(BaseModel):
    title: str
    code: str
    explanation: Optional[str] = None
    file_path: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    explanation: str
    relevant_files: List[RelevantFile]
    code_examples: List[CodeExample] = []