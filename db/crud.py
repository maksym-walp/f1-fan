from sqlalchemy.orm import Session
from db import models


# ── Season ──────────────────────────────────────────────────────────────────

def get_seasons(db: Session):
    return db.query(models.Season).all()


def get_season(db: Session, season_id: int):
    return db.query(models.Season).filter(models.Season.id == season_id).first()


def create_season(db: Session, year: int, regulation: str | None = None):
    obj = models.Season(year=year, regulation=regulation)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_season(db: Session, season_id: int, year: int | None = None, regulation: str | None = None):
    obj = get_season(db, season_id)
    if obj is None:
        return None
    if year is not None:
        obj.year = year
    if regulation is not None:
        obj.regulation = regulation
    db.commit()
    db.refresh(obj)
    return obj


def delete_season(db: Session, season_id: int):
    obj = get_season(db, season_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Team ─────────────────────────────────────────────────────────────────────

def get_teams(db: Session):
    return db.query(models.Team).all()


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def create_team(db: Session, name: str, country: str | None = None, director: str | None = None):
    obj = models.Team(name=name, country=country, director=director)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_team(db: Session, team_id: int, name: str | None = None, country: str | None = None, director: str | None = None):
    obj = get_team(db, team_id)
    if obj is None:
        return None
    if name is not None:
        obj.name = name
    if country is not None:
        obj.country = country
    if director is not None:
        obj.director = director
    db.commit()
    db.refresh(obj)
    return obj


def delete_team(db: Session, team_id: int):
    obj = get_team(db, team_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Pilot ────────────────────────────────────────────────────────────────────

def get_pilots(db: Session):
    return db.query(models.Pilot).all()


def get_pilot(db: Session, pilot_id: int):
    return db.query(models.Pilot).filter(models.Pilot.id == pilot_id).first()


def create_pilot(db: Session, name: str, country: str | None = None, photo_url: str | None = None, team_id: int | None = None):
    obj = models.Pilot(name=name, country=country, photo_url=photo_url, team_id=team_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_pilot(db: Session, pilot_id: int, name: str | None = None, country: str | None = None, photo_url: str | None = None, team_id: int | None = None):
    obj = get_pilot(db, pilot_id)
    if obj is None:
        return None
    if name is not None:
        obj.name = name
    if country is not None:
        obj.country = country
    if photo_url is not None:
        obj.photo_url = photo_url
    if team_id is not None:
        obj.team_id = team_id
    db.commit()
    db.refresh(obj)
    return obj


def delete_pilot(db: Session, pilot_id: int):
    obj = get_pilot(db, pilot_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Circuit ───────────────────────────────────────────────────────────────────

def get_circuits(db: Session):
    return db.query(models.Circuit).all()


def get_circuit(db: Session, circuit_id: int):
    return db.query(models.Circuit).filter(models.Circuit.id == circuit_id).first()


def create_circuit(db: Session, name: str, country: str | None = None, length_km=None, photo_url: str | None = None):
    obj = models.Circuit(name=name, country=country, length_km=length_km, photo_url=photo_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_circuit(db: Session, circuit_id: int, name: str | None = None, country: str | None = None, length_km=None, photo_url: str | None = None):
    obj = get_circuit(db, circuit_id)
    if obj is None:
        return None
    if name is not None:
        obj.name = name
    if country is not None:
        obj.country = country
    if length_km is not None:
        obj.length_km = length_km
    if photo_url is not None:
        obj.photo_url = photo_url
    db.commit()
    db.refresh(obj)
    return obj


def delete_circuit(db: Session, circuit_id: int):
    obj = get_circuit(db, circuit_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── GrandPrix ─────────────────────────────────────────────────────────────────

def get_grand_prixs(db: Session):
    return db.query(models.GrandPrix).all()


def get_grand_prix(db: Session, gp_id: int):
    return db.query(models.GrandPrix).filter(models.GrandPrix.id == gp_id).first()


def create_grand_prix(db: Session, name: str, season_id: int, circuit_id: int, date):
    obj = models.GrandPrix(name=name, season_id=season_id, circuit_id=circuit_id, date=date)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_grand_prix(db: Session, gp_id: int, name: str | None = None, season_id: int | None = None, circuit_id: int | None = None, date=None):
    obj = get_grand_prix(db, gp_id)
    if obj is None:
        return None
    if name is not None:
        obj.name = name
    if season_id is not None:
        obj.season_id = season_id
    if circuit_id is not None:
        obj.circuit_id = circuit_id
    if date is not None:
        obj.date = date
    db.commit()
    db.refresh(obj)
    return obj


def delete_grand_prix(db: Session, gp_id: int):
    obj = get_grand_prix(db, gp_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Result ────────────────────────────────────────────────────────────────────

def get_results(db: Session, grand_prix_id: int | None = None):
    q = db.query(models.Result)
    if grand_prix_id is not None:
        q = q.filter(models.Result.grand_prix_id == grand_prix_id)
    return q.all()


def get_result(db: Session, result_id: int):
    return db.query(models.Result).filter(models.Result.id == result_id).first()


def create_result(db: Session, grand_prix_id: int, pilot_id: int, finish_position: int | None = None, points=None, fastest_lap: bool = False):
    obj = models.Result(
        grand_prix_id=grand_prix_id,
        pilot_id=pilot_id,
        finish_position=finish_position,
        points=points,
        fastest_lap=fastest_lap,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_result(db: Session, result_id: int):
    obj = get_result(db, result_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
