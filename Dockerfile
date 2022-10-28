FROM python:3.8-slim-buster

ARG port

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV PORT=$port

COPY . .

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT app:app --preload
