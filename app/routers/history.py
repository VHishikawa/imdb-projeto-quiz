# 6. app/routers/history.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import History
from app.schemas import HistorySchema
from typing import List

router = APIRouter()

@router.get("/quiz/history/", response_model=List[HistorySchema])
def get_history(db: Session = Depends(get_db)):
    return db.query(History).all()