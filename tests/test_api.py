"""Lab 5 tests — FastAPI TestClient with in-memory SQLite."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from db.database import Base, get_db
from api.main import app


# StaticPool ensures all connections share the same in-memory DB instance.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_team_returns_201(client):
    res = client.post("/teams/", json={"name": "Ferrari", "country": "Italy"})
    assert res.status_code == 201
    assert res.json()["name"] == "Ferrari"


def test_list_teams(client):
    client.post("/teams/", json={"name": "Mercedes"})
    client.post("/teams/", json={"name": "Alpine"})
    res = client.get("/teams/")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_team_not_found_returns_404(client):
    res = client.get("/teams/9999")
    assert res.status_code == 404


def test_delete_pilot_not_found_returns_404(client):
    res = client.delete("/pilots/9999")
    assert res.status_code == 404


def test_create_season_and_retrieve(client):
    res = client.post("/seasons/", json={"year": 2024, "regulation": "Ground effect"})
    assert res.status_code == 201
    sid = res.json()["id"]
    res2 = client.get(f"/seasons/{sid}")
    assert res2.json()["year"] == 2024
