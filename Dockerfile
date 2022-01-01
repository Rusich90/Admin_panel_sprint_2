FROM python:3.9.9-slim-buster

LABEL author='rusich' version=1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . /code

WORKDIR /code

CMD gunicorn --bind 0.0.0.0:8000 config.wsgi