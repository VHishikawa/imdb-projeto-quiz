# 5. app/routers/quiz.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Quiz
from app.schemas import QuizSchema

router = APIRouter()

@router.post("/quiz/")
def create_quiz(quiz: QuizSchema, db: Session = Depends(get_db)):
    new_quiz = Quiz(id=quiz.id, title=quiz.title)
    db.add(new_quiz)
    db.commit()
    return {"message": "Quiz criado com sucesso"}
