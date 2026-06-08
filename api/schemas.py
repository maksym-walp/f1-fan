from datetime import date as Date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ── Season ───────────────────────────────────────────────────────────────────

class SeasonBase(BaseModel):
    year: int
    regulation: str | None = None


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    year: int | None = None
    regulation: str | None = None


class SeasonRead(SeasonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Team ─────────────────────────────────────────────────────────────────────

class TeamBase(BaseModel):
    name: str
    country: str | None = None
    director: str | None = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    director: str | None = None


class TeamRead(TeamBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Pilot ────────────────────────────────────────────────────────────────────

class PilotBase(BaseModel):
    name: str
    country: str | None = None
    photo_url: str | None = None
    team_id: int | None = None


class PilotCreate(PilotBase):
    pass


class PilotUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    photo_url: str | None = None
    team_id: int | None = None


class PilotRead(PilotBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    team_name: str | None = None

    @classmethod
    def from_orm_with_team(cls, pilot):
        data = {
            "id": pilot.id,
            "name": pilot.name,
            "country": pilot.country,
            "photo_url": pilot.photo_url,
            "team_id": pilot.team_id,
            "team_name": pilot.team.name if pilot.team else None,
        }
        return cls(**data)


# ── Circuit ───────────────────────────────────────────────────────────────────

class CircuitBase(BaseModel):
    name: str
    country: str | None = None
    length_km: Decimal | None = None
    photo_url: str | None = None


class CircuitCreate(CircuitBase):
    pass


class CircuitUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    length_km: Decimal | None = None
    photo_url: str | None = None


class CircuitRead(CircuitBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── GrandPrix ─────────────────────────────────────────────────────────────────

class GrandPrixBase(BaseModel):
    name: str
    season_id: int
    circuit_id: int
    date: Date


class GrandPrixCreate(GrandPrixBase):
    pass


class GrandPrixUpdate(BaseModel):
    name: Optional[str] = None
    season_id: Optional[int] = None
    circuit_id: Optional[int] = None
    date: Optional[Date] = None


class GrandPrixRead(GrandPrixBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    season_year: Optional[int] = None
    circuit_name: Optional[str] = None

    @classmethod
    def from_orm_full(cls, gp):
        return cls(
            id=gp.id,
            name=gp.name,
            season_id=gp.season_id,
            circuit_id=gp.circuit_id,
            date=gp.date,
            season_year=gp.season.year if gp.season else None,
            circuit_name=gp.circuit.name if gp.circuit else None,
        )


# ── Result ────────────────────────────────────────────────────────────────────

class ResultBase(BaseModel):
    grand_prix_id: int
    pilot_id: int
    finish_position: int | None = None
    points: Decimal | None = None
    fastest_lap: bool = False


class ResultCreate(ResultBase):
    pass


class ResultRead(ResultBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pilot_name: str | None = None

    @classmethod
    def from_orm_full(cls, r):
        return cls(
            id=r.id,
            grand_prix_id=r.grand_prix_id,
            pilot_id=r.pilot_id,
            finish_position=r.finish_position,
            points=r.points,
            fastest_lap=r.fastest_lap,
            pilot_name=r.pilot.name if r.pilot else None,
        )
