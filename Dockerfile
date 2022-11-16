FROM python:3.8

WORKDIR /python-docker

RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN python -m nltk.downloader stopwords

COPY backend ./backend/
COPY app.py .

CMD python3 -m flask run --host=0.0.0.0
