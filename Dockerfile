FROM arm32v7/python:3.7

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
        rsync \
        unzip

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
        rm get-pip.py

RUN pip3 --no-cache-dir install \
        matplotlib ipykernel Pillow paho-mqtt jupyter && \
        python -m ipykernel.kernelspec

ADD tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl ./

RUN pip3 install tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl

WORKDIR /Classifier
# COPY /requirements.txt ./


COPY ./ ./

CMD ["python", "predict.py"]
