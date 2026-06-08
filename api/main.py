import os
import tempfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db.database import get_db, init_db
from db.import_export import import_json, export_json
from api.routers import seasons, teams, pilots, circuits, grandprix, results


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="F1 Wiki API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(seasons.router)
app.include_router(teams.router)
app.include_router(pilots.router)
app.include_router(circuits.router)
app.include_router(grandprix.router)
app.include_router(results.router)


@app.get("/")
def root():
    return {"message": "F1 Wiki API", "docs": "/docs"}


@app.post("/import-json")
def import_data(path: str = "data.json", db: Session = Depends(get_db)):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    counts = import_json(path, db)
    return {"imported": counts}


@app.get("/export-json")
def export_data(db: Session = Depends(get_db)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
    tmp.close()
    export_json(tmp.name, db)
    return FileResponse(tmp.name, media_type="application/json", filename="f1_wiki_export.json")
