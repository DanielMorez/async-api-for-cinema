FROM python:3.9.1-slim

ENV PYTHONUNBUFFERED 1

ARG UID=2000
ARG GID=2000
ARG USER=django
ARG GROUP=application
ARG ROOT_APP=/app/

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean

RUN groupadd -g $GID $GROUP && \
    useradd -u $UID -g $GID -m $USER && \
    mkdir -p $ROOT_APP/static && \
    mkdir $ROOT_APP/media

COPY admin/requirements.txt /app/requirements.txt

WORKDIR $ROOT_APP
RUN pip install -r requirements.txt

COPY admin/entrypoint.sh $ROOT_APP/entrypoint.sh
COPY admin/gunicorn.conf.py $ROOT_APP/gunicorn.conf.py
COPY admin/src $ROOT_APP

RUN chmod +x entrypoint.sh

USER $USER
ENTRYPOINT ["./entrypoint.sh"]