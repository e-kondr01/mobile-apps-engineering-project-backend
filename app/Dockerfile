FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip wheel setuptools
COPY requirements/production.txt requirements.txt
RUN pip install -r requirements.txt

# копируем проект
COPY . .
