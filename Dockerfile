FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN apt-get update

RUN apt-get install -y gdal-bin

RUN apt-get install -y libmariadb-dev build-essential
RUN pip3 install -r requirements.txt

EXPOSE 8000