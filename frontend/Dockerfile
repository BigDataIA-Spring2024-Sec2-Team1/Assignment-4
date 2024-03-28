FROM python:3.9

WORKDIR /app

RUN pip install streamlit

COPY ./ /app/frontend/

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
