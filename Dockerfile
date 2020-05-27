FROM python:3.8-slim-buster

EXPOSE 5000 8000 8080

ADD requirements.txt /requirements.txt
RUN pip3.8 install -r /requirements.txt

ADD sphere /sphere