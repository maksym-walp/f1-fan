from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import SeasonCreate, SeasonUpdate, SeasonRead

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("/", response_model=list[SeasonRead])
def list_seasons(db: Session = Depends(get_db)):
    # Повертає список усіх сезонів
    return crud.get_seasons(db)


@router.post("/", response_model=SeasonRead, status_code=status.HTTP_201_CREATED)
def create_season(body: SeasonCreate, db: Session = Depends(get_db)):
    # Створює новий сезон
    return crud.create_season(db, year=body.year, regulation=body.regulation)


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: int, db: Session = Depends(get_db)):
    # Повертає сезон за ID або 404
    obj = crud.get_season(db, season_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return obj


@router.put("/{season_id}", response_model=SeasonRead)
def update_season(season_id: int, body: SeasonUpdate, db: Session = Depends(get_db)):
    # Оновлює рік або регламент сезону
    obj = crud.update_season(db, season_id, year=body.year, regulation=body.regulation)
    if obj is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return obj


@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    # Видаляє сезон або повертає 404
    if not crud.delete_season(db, season_id):
        raise HTTPException(status_code=404, detail="Season not found")
