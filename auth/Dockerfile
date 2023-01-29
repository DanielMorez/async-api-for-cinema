FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=wsgi_app

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5001 'app:create_app()'
