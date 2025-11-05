from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalyzeRequest, AnalyzeResponse
from .analyzer import mock_rate_bias, mock_highlights, generate_correction
from .rag_store import retrieve_sources
from .config import settings

app = FastAPI(title="ConscienceAI - Ethics Auditor (mock)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    text = req.text
    if not text or len(text.strip())==0:
        raise HTTPException(status_code=400, detail="Text is required")
    scores = mock_rate_bias(text)
    highlights = mock_highlights(text, scores)
    sources = retrieve_sources(scores)
    corrected = generate_correction(text, scores)
    return {"scores": scores, "highlights": highlights, "corrected": corrected, "sources": sources}
