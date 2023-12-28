FROM python:3.13.0a2-alpine3.18


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt .
RUN pip install -r requirements.txt


RUN mkdir /api
WORKDIR /api
COPY . /api

EXPOSE 8000
