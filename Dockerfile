FROM python:3.10.7-slim-buster

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && \
  apt-get install -y python3-pip && \
  pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000