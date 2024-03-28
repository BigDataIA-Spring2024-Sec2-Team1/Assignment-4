FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r /app/requirements.txt

COPY ./ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD ["streamlit", "run", "frontend/main.py"]