FROM python:3.8.10-slim-buster
LABEL maintainer="netever"
COPY . /app
WORKDIR /app
RUN pip3 install -r reqirements.txt
RUN apt update -y
RUN apt-get install poppler-utils -y
CMD python send.py
