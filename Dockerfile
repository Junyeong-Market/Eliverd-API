FROM python:3 AS BUILDER
FROM osgeo/gdal

WORKDIR /usr/src/app

COPY . .

RUN apt update

RUN apt install python3

RUN pip install -r requirements.txt