# 🚀 Projeto API Quiz (Python + Redis + Postgres)

API desenvolvida com **FastAPI** para gerenciar questões e respostas de quiz, utilizando o banco de dados em memória **Redis** e o banco de dados relacional **Postgres**.

---

## ⚙️ Configuração

1. **Suba um container Redis**  
   ```sh
   docker-compose up -d 
   ```

2. **Execute a aplicação**  
   ```sh
   uvicorn main:app --reload --log-level info
   ```

---

## 🧪 Testando a API

Acesse no navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

- Para acessar a documentação interativa (Swagger):  
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![Swagger UI](https://github.com/commithouse/apiQuestionRedis/blob/main/images/image.png?raw=true)


