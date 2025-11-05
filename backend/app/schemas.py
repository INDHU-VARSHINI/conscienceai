from pydantic import BaseModel
from typing import Dict, Any

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    scores: Dict[str, int]   # e.g., {"gender":3, "race":2, "age":1}
    highlights: Dict[str,str] # highlight text explaining issues
    corrected: str
    sources: list
