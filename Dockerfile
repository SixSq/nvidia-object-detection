FROM nvcr.io/nvidia/l4t-base:r32.2

WORKDIR /darknet

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --fix-missing make g++ git
RUN apt update && apt install -y --fix-missing python3-pip libhdf5-serial-dev hdf5-tools
RUN apt update && apt install -y python3-opencv

RUN pip3 install flask imutils numpy

RUN git clone https://github.com/pjreddie/darknet && cd darknet && mkdir weights && cd weights && wget https://pjreddie.com/media/files/yolov3-tiny.weights

COPY Makefile ./darknet

COPY darknetInstall.sh ./darknet

COPY app.py .

ADD templates ./templates

ADD static ./static

COPY ./ ./darknet

# RUN ./darknetInstall.sh

CMD [""]