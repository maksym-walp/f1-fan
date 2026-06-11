from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import CircuitCreate, CircuitUpdate, CircuitRead

router = APIRouter(prefix="/circuits", tags=["circuits"])


@router.get("/", response_model=list[CircuitRead])
def list_circuits(db: Session = Depends(get_db)):
    # Повертає список усіх трас
    return crud.get_circuits(db)


@router.post("/", response_model=CircuitRead, status_code=status.HTTP_201_CREATED)
def create_circuit(body: CircuitCreate, db: Session = Depends(get_db)):
    # Створює нову трасу
    return crud.create_circuit(db, name=body.name, country=body.country, length_km=body.length_km, photo_url=body.photo_url)


@router.get("/{circuit_id}", response_model=CircuitRead)
def get_circuit(circuit_id: int, db: Session = Depends(get_db)):
    # Повертає трасу за ID або 404
    obj = crud.get_circuit(db, circuit_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return obj


@router.put("/{circuit_id}", response_model=CircuitRead)
def update_circuit(circuit_id: int, body: CircuitUpdate, db: Session = Depends(get_db)):
    # Оновлює поля траси (тільки передані значення)
    obj = crud.update_circuit(db, circuit_id, name=body.name, country=body.country, length_km=body.length_km, photo_url=body.photo_url)
    if obj is None:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return obj


@router.delete("/{circuit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_circuit(circuit_id: int, db: Session = Depends(get_db)):
    # Видаляє трасу або повертає 404
    if not crud.delete_circuit(db, circuit_id):
        raise HTTPException(status_code=404, detail="Circuit not found")
