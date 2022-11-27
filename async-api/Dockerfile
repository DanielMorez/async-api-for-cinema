FROM python:3.9.15

WORKDIR .

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt
     
COPY . .
