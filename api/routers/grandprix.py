from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import GrandPrixCreate, GrandPrixUpdate, GrandPrixRead

router = APIRouter(prefix="/grandprix", tags=["grandprix"])


@router.get("/", response_model=list[GrandPrixRead])
def list_grand_prixs(db: Session = Depends(get_db)):
    return [GrandPrixRead.from_orm_full(gp) for gp in crud.get_grand_prixs(db)]


@router.post("/", response_model=GrandPrixRead, status_code=status.HTTP_201_CREATED)
def create_grand_prix(body: GrandPrixCreate, db: Session = Depends(get_db)):
    gp = crud.create_grand_prix(db, name=body.name, season_id=body.season_id, circuit_id=body.circuit_id, date=body.date)
    return GrandPrixRead.from_orm_full(gp)


@router.get("/{gp_id}", response_model=GrandPrixRead)
def get_grand_prix(gp_id: int, db: Session = Depends(get_db)):
    gp = crud.get_grand_prix(db, gp_id)
    if gp is None:
        raise HTTPException(status_code=404, detail="Grand Prix not found")
    return GrandPrixRead.from_orm_full(gp)


@router.put("/{gp_id}", response_model=GrandPrixRead)
def update_grand_prix(gp_id: int, body: GrandPrixUpdate, db: Session = Depends(get_db)):
    gp = crud.update_grand_prix(db, gp_id, name=body.name, season_id=body.season_id, circuit_id=body.circuit_id, date=body.date)
    if gp is None:
        raise HTTPException(status_code=404, detail="Grand Prix not found")
    return GrandPrixRead.from_orm_full(gp)


@router.delete("/{gp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grand_prix(gp_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grand_prix(db, gp_id):
        raise HTTPException(status_code=404, detail="Grand Prix not found")
