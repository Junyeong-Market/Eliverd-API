FROM python:3

WORKDIR /usr/src/app

COPY . .

# RUN add-apt-repository ppa:ubuntugis/ppa

RUN apt-get update

RUN apt-get install -y gdal-bin

RUN apt-get install -y libmariadb-dev python3-pip build-essential
RUN pip3 install -r requirements.txt