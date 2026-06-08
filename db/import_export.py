"""JSON import / export utilities (Lab 4).

Import reads data.json (teams, pilots, grandprix from the CLI app) and
upserts them into the database.

Export serialises all six tables to a JSON file.
"""

import json
from datetime import date
from sqlalchemy.orm import Session
from db import models


def import_json(path: str, db: Session) -> dict:
    """Load data from a JSON file and upsert into the database."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    counts = {"teams": 0, "pilots": 0, "grand_prixs": 0}

    for t in data.get("teams", []):
        existing = db.query(models.Team).filter(models.Team.name == t["name"]).first()
        if existing is None:
            db.add(models.Team(name=t["name"], country=t.get("country")))
            counts["teams"] += 1

    for p in data.get("pilots", []):
        existing = db.query(models.Pilot).filter(models.Pilot.name == p["name"]).first()
        if existing is None:
            db.add(models.Pilot(name=p["name"], country=p.get("country")))
            counts["pilots"] += 1

    db.flush()

    for gp in data.get("grand_prixs", []):
        # Grand Prix requires a season and circuit — skip if not resolvable
        existing = db.query(models.GrandPrix).filter(models.GrandPrix.name == gp["name"]).first()
        if existing is None:
            season = db.query(models.Season).first()
            circuit = db.query(models.Circuit).filter(models.Circuit.name == gp.get("circuit", "")).first()
            if season and circuit:
                gp_date = date.fromisoformat(gp["date"]) if gp.get("date") else date.today()
                db.add(models.GrandPrix(
                    name=gp["name"],
                    season_id=season.id,
                    circuit_id=circuit.id,
                    date=gp_date,
                ))
                counts["grand_prixs"] += 1

    db.commit()
    return counts


def export_json(path: str, db: Session) -> None:
    """Serialise all tables to a JSON file."""

    def _season(s: models.Season):
        return {"id": s.id, "year": s.year, "regulation": s.regulation}

    def _team(t: models.Team):
        return {"id": t.id, "name": t.name, "country": t.country, "director": t.director}

    def _pilot(p: models.Pilot):
        return {"id": p.id, "name": p.name, "country": p.country, "photo_url": p.photo_url, "team_id": p.team_id}

    def _circuit(c: models.Circuit):
        return {"id": c.id, "name": c.name, "country": c.country, "length_km": str(c.length_km) if c.length_km else None}

    def _gp(g: models.GrandPrix):
        return {"id": g.id, "name": g.name, "season_id": g.season_id, "circuit_id": g.circuit_id, "date": str(g.date)}

    def _result(r: models.Result):
        return {
            "id": r.id,
            "grand_prix_id": r.grand_prix_id,
            "pilot_id": r.pilot_id,
            "finish_position": r.finish_position,
            "points": str(r.points) if r.points else None,
            "fastest_lap": r.fastest_lap,
        }

    payload = {
        "seasons": [_season(s) for s in db.query(models.Season).all()],
        "teams": [_team(t) for t in db.query(models.Team).all()],
        "pilots": [_pilot(p) for p in db.query(models.Pilot).all()],
        "circuits": [_circuit(c) for c in db.query(models.Circuit).all()],
        "grand_prixs": [_gp(g) for g in db.query(models.GrandPrix).all()],
        "results": [_result(r) for r in db.query(models.Result).all()],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
