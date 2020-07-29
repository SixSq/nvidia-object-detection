#!/bin/bash

cd darknet

make && ./darknet detect cfg/yolov3-tiny.cfg weights/yolov3-tiny.weights data/dog.jpg

python3 app.py