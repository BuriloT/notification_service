FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir