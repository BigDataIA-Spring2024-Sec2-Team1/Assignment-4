FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r /app/requirements.txt

COPY ./ /app/backend/

COPY .env /app/backend/.env

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
