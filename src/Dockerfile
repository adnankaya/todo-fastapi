FROM python:3.9.4-alpine

# set work directory
WORKDIR /home/adnan/webdev/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /home/adnan/webdev/app/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /home/adnan/webdev/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /home/adnan/webdev/app/