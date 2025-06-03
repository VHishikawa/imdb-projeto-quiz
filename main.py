from fastapi import FastAPI, HTTPException, Depends
import redis
import json
from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import JSONB
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuração do Redis
redis_client = redis.Redis(
    host='20.201.117.192',
    port=6379,
    decode_responses=True
)

# Configuração do PostgreSQL - USANDO DRIVER SÍNCRONO
DATABASE_URL = os.getenv("20.201.117.192", "postgresql://user:password@localhost/mydatabase")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Tabela associativa para votos
class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(String, index=True)
    question_id = Column(String, index=True)
    choice = Column(String)
    count = Column(Integer, default=0)

# Modelo de dados para quizzes
class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    questions = Column(JSONB)

# Criar tabelas se não existirem
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {str(e)}")

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/quizzes")
def get_quizzes():
    quizzes = redis_client.hgetall("quizzes")
    return [{"id": k, **json.loads(v)} for k, v in quizzes.items()]

@app.post("/quizzes")
def create_quiz(quiz: dict, db: Session = Depends(get_db)):
    try:
        # Salva no Redis
        quiz_id = str(redis_client.incr("quiz_id"))
        redis_client.hset("quizzes", quiz_id, json.dumps(quiz))
        
        # Salva no PostgreSQL
        db_quiz = Quiz(
            id=int(quiz_id),
            title=quiz.get("title", "Sem título"),
            questions=quiz.get("questions", [])
        )
        db.add(db_quiz)
        db.commit()
        
        return {"id": quiz_id, "message": "Quiz criado com sucesso!"}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar quiz")

@app.post("/vote/{quiz_id}/{question_id}")
def vote(quiz_id: str, question_id: str, choice: str, db: Session = Depends(get_db)):
    try:
        vote_key = f"quiz:{quiz_id}:question:{question_id}:votes"
        
        # Atualiza Redis
        redis_client.hincrby(vote_key, choice, 1)
        
        # Atualiza PostgreSQL
        vote_record = db.query(Vote).filter_by(
            quiz_id=quiz_id,
            question_id=question_id,
            choice=choice
        ).first()
        
        if vote_record:
            vote_record.count += 1
        else:
            vote_record = Vote(
                quiz_id=quiz_id,
                question_id=question_id,
                choice=choice,
                count=1
            )
            db.add(vote_record)
        
        db.commit()
        return {"message": "Voto registrado!"}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao registrar voto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao registrar voto")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)