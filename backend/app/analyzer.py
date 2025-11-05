from typing import Dict
from .config import settings

def mock_rate_bias(text: str) -> Dict[str,int]:
    # Simple heuristic mock: counts certain keywords to simulate bias scoring 1-5
    lower = text.lower()
    scores = {"gender":1, "race":1, "age":1}
    if any(w in lower for w in ["only men", "guys", "he is better"]):
        scores["gender"] = 4
    if any(w in lower for w in ["immigrant", "illegal", "ethnic slur"]):
        scores["race"] = 5
    if any(w in lower for w in ["old people", "youngsters are lazy"]):
        scores["age"] = 3
    return scores

def mock_highlights(text: str, scores: Dict[str,int]) -> Dict[str,str]:
    hints = {}
    if scores["gender"]>2:
        hints["gender"] = "Contains gendered assertion such as 'only men' or stereotyping."
    if scores["race"]>2:
        hints["race"] = "Potentially racialized language or labels."
    if scores["age"]>2:
        hints["age"] = "Age-based generalizations found."
    return hints

def generate_correction(text: str, scores: Dict[str,int]) -> str:
    # Very simple correction: neutralize pronouns and remove slurs — expand for real system
    corrected = text.replace("only men", "people").replace("guys", "people")
    # More sophisticated correction can use LLM for paraphrase
    return corrected
