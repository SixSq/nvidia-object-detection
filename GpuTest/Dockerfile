FROM nvcr.io/nvidia/l4t-base:r32.2

WORKDIR /

RUN apt update && apt install -y --fix-missing make g++ git
RUN apt update && apt install -y --fix-missing python3-pip libhdf5-serial-dev hdf5-tools


RUN git clone https://github.com/pjreddie/darknet && cd darknet 

COPY Makefile .

RUN make


RUN mkdir weights && cd weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

RUN cd ..

CMD ['bash']