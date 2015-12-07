#!/bin/bash

sudo apt-get update

# Install python dependencies
sudo apt-get install build-essential python-dev python-pip nginx

# Install Pillow dependencies
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

# Install project dependencies
pip install -r requirements.txt
