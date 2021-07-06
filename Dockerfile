FROM python:3.9-alpine

LABEL Description="Python application that executes a 'chaos monkey' methodology over an specified k8s namespace"
LABEL Maintainer="Luis Miguel Sáez Martín"

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN adduser -h /app -D -H -u 1000 executor
RUN mkdir /app
WORKDIR /app
ADD code/ /app

RUN chown -R executor.executor /app
USER executor

ENTRYPOINT ["python","main.py"]
