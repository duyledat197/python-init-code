FROM python:3.7-alpine3.8
ENV PYTHONUNBUFFERED 1
ENV DOCKER 1

# Setup for psycopg2-binary and make
RUN apk update && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    apk add --no-cache make && \
    apk add --no-cache postgresql-libs libressl-dev musl-dev libffi-dev libxml2-dev libxslt-dev python-dev
WORKDIR /app

# Application Environment
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD . .
