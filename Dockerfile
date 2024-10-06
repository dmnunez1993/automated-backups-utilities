FROM python:3.12-alpine

RUN apk add postgresql docker

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY *.py /app/

ENTRYPOINT [ "python3", "app.py" ]
