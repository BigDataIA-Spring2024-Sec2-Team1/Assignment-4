FROM python:3.9-slim

WORKDIR /app

COPY ./ /app/frontend/

COPY requirements.txt /app/requirements.txt

COPY .env /app/frontend/.env

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "/app/frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
