# 7. app/routers/statistics.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import History
from app.schemas import StatisticsSchema

router = APIRouter()

@router.get("/quiz/statistics/", response_model=StatisticsSchema)
def get_statistics(quiz_id: str, db: Session = Depends(get_db)):
    total_questions = db.query(History).filter_by(quiz_id=quiz_id).count()
    correct_answers = db.query(History).filter_by(quiz_id=quiz_id, is_correct=True).count()
    wrong_answers = total_questions - correct_answers
    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return {
        "quiz_id": quiz_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "accuracy": accuracy
    }
    