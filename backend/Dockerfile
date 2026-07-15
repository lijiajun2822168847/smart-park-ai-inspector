FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install openai python-dotenv flask flask-cors numpy fastapi uvicorn python-multipart langchain langchain-community langchain-openai langchain-core
COPY . .
CMD ["python", "main.py"]