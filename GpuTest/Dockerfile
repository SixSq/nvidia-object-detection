FROM raspbian/stretch

RUN apt-get update && yes | apt-get upgrade

RUN apt-get install -y --no-install-recommends libatlas-base-dev python3 \
			python3-dev python3-pip python3-setuptools \
			python-tk libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
			libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
			libxvidcore-dev libx264-dev qt4-dev-tools protobuf-compiler \
			libilmbase-dev libopenexr-dev libgstreamer1.0-dev libqt4-test && \
	apt-get clean && \
 	rm -rf /var/lib/apt/lists/*
 
RUN pip3 install --no-cache-dir absl-py
RUN pip3 install --default-timeout=3000 --no-cache-dir tensorflow 
RUN pip3 install --default-timeout=3000 ipython==7.7.0 

RUN pip3 install --default-timeout=3000 --no-cache-dir pillow lxml jupyter matplotlib numpy cython flask_opencv_streamer 

RUN mkdir -p /tensorflow1

COPY models/ /tensorflow1/models

ENV PYTHONPATH $PYTHONPATH:/tensorflow1/models/research:/tensorflow1/models/research/slim

RUN cd /tensorflow1/models/research &&  protoc object_detection/protos/*.proto --python_out=.

WORKDIR /tensorflow1/models/research/object_detection

RUN wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz && \
	tar -xzvf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz

RUN mkdir -p templates

COPY templates templates
COPY gpuTest.py .

CMD ["python3", "gpuTest.py"]

