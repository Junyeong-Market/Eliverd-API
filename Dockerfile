FROM python:3 AS BUILDER
FROM osgeo/gdal

WORKDIR /usr/src/app

COPY . .

RUN apt-get update

RUN apt-get install -y libmysqlclient-dev python3-pip build-essential
RUN pip3 install -r requirements.txt