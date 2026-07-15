FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install openai python-dotenv flask flask-cors numpy
COPY . .
CMD ["python", "app.py"]