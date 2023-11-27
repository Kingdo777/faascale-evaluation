# Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install flask gunicorn

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
