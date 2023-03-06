FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app

COPY user_service/requirements.txt $ROOT_APP/requirements.txt

WORKDIR $ROOT_APP

RUN pip install -r requirements.txt

COPY user_service/src $ROOT_APP/

CMD uvicorn main:app --port 8002 --host 0.0.0.0

