if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt install wget
elif [[ "$OSTYPE" == "darwin"* ]]; then
  brew install wget
else
  echo "PLATFORM NOT SUPPORTED"
  return
fi

# install GeoDjango Related stuff
wget https://download.osgeo.org/geos/geos-3.8.1.tar.bz2
tar xjf geos-3.8.1.tar.bz2

cd geos-3.8.1 || exit
./configure
make
sudo make install