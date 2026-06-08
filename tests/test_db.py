"""Lab 4 tests — SQLite in-memory, no Postgres required."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from db import models, crud


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_and_list_teams(db):
    crud.create_team(db, name="Ferrari", country="Italy")
    crud.create_team(db, name="McLaren", country="UK")
    teams = crud.get_teams(db)
    assert len(teams) == 2
    assert teams[0].name == "Ferrari"


def test_update_team(db):
    team = crud.create_team(db, name="Williams", country="UK")
    updated = crud.update_team(db, team.id, director="James Vowles")
    assert updated.director == "James Vowles"
    assert updated.name == "Williams"


def test_delete_team(db):
    team = crud.create_team(db, name="Haas", country="USA")
    assert crud.delete_team(db, team.id) is True
    assert crud.get_team(db, team.id) is None


def test_create_pilot_with_team(db):
    team = crud.create_team(db, name="Red Bull", country="Austria")
    pilot = crud.create_pilot(db, name="Max Verstappen", country="Netherlands", team_id=team.id)
    fetched = crud.get_pilot(db, pilot.id)
    assert fetched.team_id == team.id
    assert fetched.name == "Max Verstappen"


def test_get_nonexistent_returns_none(db):
    assert crud.get_team(db, 9999) is None
    assert crud.get_pilot(db, 9999) is None
    assert crud.get_season(db, 9999) is None
