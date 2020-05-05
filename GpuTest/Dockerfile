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
        python3 \
        python3-dev \
        python3-numpy \
        python3-scipy \
        python3-opencv \
        python3-pip \
        python3-setuptools \
        rsync \
        wget \
        unzip

RUN wget https://nvidia.box.com/shared/static/ncgzus5o23uck9i5oth2n8n06k340l6k.whl -O torch-1.4.0-cp36-cp36m-linux_aarch64.whl 

RUN apt-get install python3-pip libopenblas-base libopenmpi-dev -y

RUN pip3 --no-cache-dir install cython numpy torch-1.4.0-cp36-cp36m-linux_aarch64.whl 

WORKDIR /GPUTest
# COPY /requirements.txt ./

COPY ./ ./

CMD ["python3", "gpuTest.py"]

