FROM python:3.8-slim-buster

EXPOSE 5000 8000 8080

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD sphere /sphere