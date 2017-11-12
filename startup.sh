#!/bin/bash

wget -c http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
bash Miniconda-latest-Linux-x86_64.sh
echo "export PATH=~/miniconda2/bin:$PATH" >> ~/.bashrc
source ~/.bashrc

conda install cherrypy
conda install numpy==1.11.1
conda install pysam
sudo apt-get install gcc
easy_install msbwt

sudo mkdir /playpen
sudo chmod 777 /playpen
cd /playpen
echo -n "Enter [server]:[bwt_location] [ENTER]: "
read bwt_location
scp -r $bwt_location .

mkdir ~/msbwtCloud
cd ~/msbwtCloud
wget https://raw.githubusercontent.com/mnajarian/msbwtCloud/master/core.py

