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
        python3-setuptools \
        rsync \
        unzip

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install \
        matplotlib ipykernel Pillow paho-mqtt jupyter && \
        python3 -m ipykernel.kernelspec

RUN curl -L https://github.com/lherman-cs/tensorflow-aarch64/releases/download/r1.4/tensorflow-1.4.0rc0-cp35-cp35m-linux_aarch64.whl > /tmp/tensorflow-1.4.0rc0-cp35-cp35m-linux_aarch64.whl

RUN pip3 install /tmp/tensorflow-1.4.0rc0-cp35-cp35m-linux_aarch64.whl

WORKDIR /GPUTest
# COPY /requirements.txt ./

COPY ./ ./

CMD ["python3", "gpuTest.py"]

