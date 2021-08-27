#!/bin/sh

apt-get update
apt-get install cmake libopenblas-dev liblapack-dev
#apt-get install libjpeg-dev　python-setuptools　python3-dev　python3-pip
pip3 install --upgrade pip

wget http://dlib.net/files/dlib-19.17.tar.bz2
tar jxvf dlib-19.17.tar.bz2
cp -f shared_data/cudnn_dlibapi.cpp dlib-19.17/dlib/cuda
cd dlib-19.17
python3 setup.py install

pip3 install imutils

cd ..