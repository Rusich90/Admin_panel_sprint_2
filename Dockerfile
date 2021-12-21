FROM python:3.9

LABEL author='rusich' version=1

RUN mkdir /code

COPY . /code

WORKDIR /code

RUN pip install -r requirements.txt
