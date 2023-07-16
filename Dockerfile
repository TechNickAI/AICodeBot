FROM python:3.9-slim

RUN apt-get update && apt-get install -y git
COPY requirements/requirements.txt /
COPY requirements/requirements-test.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt -r /requirements-test.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

ENTRYPOINT ["pytest"]

