from pydantic import BaseModel
from typing import Dict, Any, List

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    scores: Dict[str, int]
    highlights: Dict[str, List[str]]
    corrected: str
    sources: List[Dict[str, str]]
