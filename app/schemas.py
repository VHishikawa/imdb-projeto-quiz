# 4. app/schemas.py
from pydantic import BaseModel
from typing import List

class QuestionSchema(BaseModel):
    id: str
    text: str
    correct_answer: str

class QuizSchema(BaseModel):
    id: str
    title: str
    questions: List[QuestionSchema]

class HistorySchema(BaseModel):
    user_id: str
    quiz_id: str
    question_id: str
    user_answer: str
    is_correct: bool

class StatisticsSchema(BaseModel):
    quiz_id: str
    total_questions: int
    correct_answers: int
    wrong_answers: int
    accuracy: float