# Etapa 1: Usar uma imagem oficial do Python
FROM python:3.9-slim

# Etapa 2: Definir o diretório de trabalho
WORKDIR /app

# Etapa 3: Copiar os arquivos da aplicação para o container
COPY . /app/

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Expor a porta padrão da FastAPI
EXPOSE 8000

# Etapa 6: Rodar a aplicação FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
