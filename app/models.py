# 3. app/models.py
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    questions = relationship("Question", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, index=True)
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    text = Column(String)
    correct_answer = Column(String)
    quiz = relationship("Quiz", back_populates="questions")

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    quiz_id = Column(String, index=True)
    question_id = Column(String, index=True)
    user_answer = Column(String)
    is_correct = Column(Boolean)
