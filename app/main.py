## Estrutura do Backend - FastAPI com PostgreSQL e Redis

# 1. app/main.py
from fastapi import FastAPI
from app.routers import quiz, history, statistics
from app.database import engine, Base

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir os routers
app.include_router(quiz.router)
app.include_router(history.router)
app.include_router(statistics.router)



