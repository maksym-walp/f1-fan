from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import PilotCreate, PilotUpdate, PilotRead

router = APIRouter(prefix="/pilots", tags=["pilots"])


@router.get("/", response_model=list[PilotRead])
def list_pilots(db: Session = Depends(get_db)):
    # Повертає всіх пілотів з іменем їхньої команди
    pilots = crud.get_pilots(db)
    return [PilotRead.from_orm_with_team(p) for p in pilots]


@router.post("/", response_model=PilotRead, status_code=status.HTTP_201_CREATED)
def create_pilot(body: PilotCreate, db: Session = Depends(get_db)):
    # Створює нового пілота
    pilot = crud.create_pilot(db, name=body.name, country=body.country, photo_url=body.photo_url, team_id=body.team_id)
    return PilotRead.from_orm_with_team(pilot)


@router.get("/{pilot_id}", response_model=PilotRead)
def get_pilot(pilot_id: int, db: Session = Depends(get_db)):
    # Повертає пілота за ID або 404
    pilot = crud.get_pilot(db, pilot_id)
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return PilotRead.from_orm_with_team(pilot)


@router.put("/{pilot_id}", response_model=PilotRead)
def update_pilot(pilot_id: int, body: PilotUpdate, db: Session = Depends(get_db)):
    # Оновлює поля пілота (тільки передані значення)
    pilot = crud.update_pilot(db, pilot_id, name=body.name, country=body.country, photo_url=body.photo_url, team_id=body.team_id)
    if pilot is None:
        raise HTTPException(status_code=404, detail="Pilot not found")
    return PilotRead.from_orm_with_team(pilot)


@router.delete("/{pilot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pilot(pilot_id: int, db: Session = Depends(get_db)):
    # Видаляє пілота або повертає 404
    if not crud.delete_pilot(db, pilot_id):
        raise HTTPException(status_code=404, detail="Pilot not found")
