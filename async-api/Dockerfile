FROM python:3.9.15

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
COPY .env .env

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt
     
COPY . .