from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from api.schemas import ResultCreate, ResultRead

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/", response_model=list[ResultRead])
def list_results(grand_prix_id: int | None = None, db: Session = Depends(get_db)):
    # Повертає результати; можна фільтрувати за grand_prix_id
    results = crud.get_results(db, grand_prix_id=grand_prix_id)
    return [ResultRead.from_orm_full(r) for r in results]


@router.post("/", response_model=ResultRead, status_code=status.HTTP_201_CREATED)
def create_result(body: ResultCreate, db: Session = Depends(get_db)):
    # Записує результат пілота в гонці
    r = crud.create_result(
        db,
        grand_prix_id=body.grand_prix_id,
        pilot_id=body.pilot_id,
        finish_position=body.finish_position,
        points=body.points,
        fastest_lap=body.fastest_lap,
    )
    return ResultRead.from_orm_full(r)


@router.get("/{result_id}", response_model=ResultRead)
def get_result(result_id: int, db: Session = Depends(get_db)):
    # Повертає результат за ID або 404
    r = crud.get_result(db, result_id)
    if r is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultRead.from_orm_full(r)


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(result_id: int, db: Session = Depends(get_db)):
    # Видаляє результат або повертає 404
    if not crud.delete_result(db, result_id):
        raise HTTPException(status_code=404, detail="Result not found")
