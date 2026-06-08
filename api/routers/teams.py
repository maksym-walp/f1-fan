from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import TeamCreate, TeamUpdate, TeamRead

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamRead])
def list_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db)


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(body: TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db, name=body.name, country=body.country, director=body.director)


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)):
    obj = crud.get_team(db, team_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return obj


@router.put("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, body: TeamUpdate, db: Session = Depends(get_db)):
    obj = crud.update_team(db, team_id, name=body.name, country=body.country, director=body.director)
    if obj is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return obj


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    if not crud.delete_team(db, team_id):
        raise HTTPException(status_code=404, detail="Team not found")
