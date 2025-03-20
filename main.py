from fastapi import FastAPI, HTTPException
import redis
import json

app = FastAPI()

# Configuração do Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/quizzes")
def get_quizzes():
    quizzes = redis_client.hgetall("quizzes")
    return [{"id": k, **json.loads(v)} for k, v in quizzes.items()]

@app.post("/quizzes")
def create_quiz(quiz: dict):
    quiz_id = str(redis_client.incr("quiz_id"))
    redis_client.hset("quizzes", quiz_id, json.dumps(quiz))
    return {"id": quiz_id, "message": "Quiz criado com sucesso!"}

@app.post("/vote/{quiz_id}/{question_id}")
def vote(quiz_id: str, question_id: str, choice: str):
    vote_key = f"quiz:{quiz_id}:question:{question_id}:votes"
    redis_client.hincrby(vote_key, choice, 1)
    return {"message": "Voto registrado!"}