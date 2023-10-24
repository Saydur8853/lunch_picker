FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD ./ /app

RUN apk update

RUN pip install --upgrade pip

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk del build-deps

RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt --verbose

