FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8002", "-k", "uvicorn.workers.UvicornWorker", "main:app"]