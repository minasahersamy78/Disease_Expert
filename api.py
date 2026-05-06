"""
FastAPI layer for the disease expert system.

Run (from project directory):
  uvicorn api:app --reload --host 127.0.0.1 --port 8000

Or:
  python api.py
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from interface import DiseaseExpertSystem


WEB_DIR = Path(__file__).resolve().parent / "web"
ASSETS_DIR = WEB_DIR / "assets"


class SymptomItem(BaseModel):
    index: int = Field(..., ge=1, description="1-based index as in the CLI list")
    key: str
    label: str


class SymptomsResponse(BaseModel):
    symptoms: list[SymptomItem]


class DiagnoseRequest(BaseModel):
    indices: list[int] = Field(..., min_length=1, description="1-based symptom indices")


class DiagnoseResponse(BaseModel):
    symptoms: list[str]
    symptoms_display: list[str]
    exact_rule_match: bool
    diagnoses: list[dict[str, str]]
    no_match: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.expert = DiseaseExpertSystem(quiet=True)
        app.state.expert_error = None
    except FileNotFoundError as e:
        app.state.expert = None
        app.state.expert_error = str(e)
    yield


app = FastAPI(
    title="Disease Expert System",
    description="Prolog-backed expert system via PySwip",
    lifespan=lifespan,
)

if ASSETS_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/")
def web_home():
    index_path = WEB_DIR / "index.html"
    if not index_path.is_file():
        raise HTTPException(500, detail="web/index.html missing")
    return FileResponse(index_path)


@app.get("/api/symptoms", response_model=SymptomsResponse)
def api_symptoms():
    expert: DiseaseExpertSystem | None = getattr(app.state, "expert", None)
    if expert is None:
        raise HTTPException(503, detail=getattr(app.state, "expert_error", "Expert system unavailable"))
    keys = expert.get_available_symptoms()
    items = [
        SymptomItem(index=i + 1, key=str(k), label=str(k).replace("_", " ").title())
        for i, k in enumerate(keys)
    ]
    return SymptomsResponse(symptoms=items)


@app.post("/api/diagnose", response_model=DiagnoseResponse)
def api_diagnose(req: DiagnoseRequest):
    expert: DiseaseExpertSystem | None = getattr(app.state, "expert", None)
    if expert is None:
        raise HTTPException(503, detail=getattr(app.state, "expert_error", "Expert system unavailable"))
    available = expert.get_available_symptoms()
    n = len(available)
    for i in req.indices:
        if i < 1 or i > n:
            raise HTTPException(400, detail=f"Index {i} out of range (1–{n})")
    selected = [str(available[i - 1]) for i in req.indices]
    results = expert.diagnose(selected)
    payload = expert.diagnosis_payload(results, selected)
    return DiagnoseResponse(**payload)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    ns = parser.parse_args()
    import uvicorn

    uvicorn.run(app, host=ns.host, port=ns.port)
