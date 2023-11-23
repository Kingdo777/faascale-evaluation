FROM ubuntu:latest
LABEL authors="kingdo"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gunicorn \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    pip3 install asyncio aiohttp datetime requests flask boto3

COPY ./* /app/

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

ENV PORT=8080

ENTRYPOINT ["sh", "-c", "gunicorn --bind :$PORT --workers 8 --threads 8 --timeout 0 app:app"]

