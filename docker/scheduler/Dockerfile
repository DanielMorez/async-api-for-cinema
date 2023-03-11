FROM python:3.9.1-slim

ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app

RUN mkdir $ROOT_APP

COPY scheduler/requirements.txt $ROOT_APP/requirements.txt


WORKDIR $ROOT_APP
RUN pip install -r requirements.txt

COPY scheduler/src $ROOT_APP/

CMD python main.py