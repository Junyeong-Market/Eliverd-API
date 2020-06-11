#!/bin/bash

# START: platform specific commands
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  apt install wget
elif [[ "$OSTYPE" == "darwin"* ]]; then
  brew install openssl
  export LDFLAGS=-L/usr/local/opt/openssl/lib
  brew install wget
  brew install libxml2
  ln -s /usr/local/opt/libxml2/include/libxml2/libxml /usr/local/include/libxml
else
  echo "PLATFORM NOT SUPPORTED"
  return
fi
# END

# START: install GeoDjango Related stuff - GEOS
wget https://download.osgeo.org/geos/geos-3.8.1.tar.bz2
tar xjf geos-3.8.1.tar.bz2
cd geos-3.8.1 || exit
./configure
make
make install
cd ..
rm -r geos-3.8.1
rm geos-3.8.1.tar.bz2
# END

# START: install GeoDjango Related stuff - PROJ
wget https://download.osgeo.org/proj/proj-6.3.2.tar.gz
wget https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz
tar xzf proj-6.3.2.tar.gz
cd proj-6.3.2 || exit
mkdir nad
# shellcheck disable=SC2164
cd nad
tar xzf ../../proj-datumgrid-1.8.tar.gz
cd ..
./configure
make
make install
cd ..
rm -r proj-6.3.2
rm proj-6.3.2.tar.gz
rm proj-datumgrid-1.8.tar.gz
# END

# START: install GeoDjango Related stuff - GDAL
wget https://download.osgeo.org/gdal/3.1.0/gdal-3.1.0.tar.gz
tar xzf gdal-3.1.0.tar.gz
cd gdal-3.1.0 || exit
./configure --without-pg
make
make install
cd ..
rm -r gdal-3.1.0
rm gdal-3.1.0.tar.gz
# END

pip3 install -r requirements.txt