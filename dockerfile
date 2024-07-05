FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 8000
ENTRYPOINT ["uvicorn", "--app-dir", "src/", "--host", "0.0.0.0", "--port", "8000", "main:app"]
