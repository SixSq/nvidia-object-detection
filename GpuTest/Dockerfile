FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libhdf5-dev \
        libpng-dev \
        libzmq3-dev \
        pkg-config \
        python3-dev \
        python3-numpy \
        python3-scipy \
        python3-opencv \
        python3-pip \
        rsync \
        unzip

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install \
        matplotlib ipykernel Pillow paho-mqtt jupyter && \
        python -m ipykernel.kernelspec

ADD tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl ./

RUN pip3 install tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl

WORKDIR /GPUTest
# COPY /requirements.txt ./

COPY ./ ./

CMD ["python", "gpuTest.py"]
