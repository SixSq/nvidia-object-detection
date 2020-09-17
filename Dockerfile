FROM toolboc/jetson-nano-l4t-cuda-cudnn-opencv-darknet

WORKDIR darknet/

COPY entry.sh .

CMD ["./entry.sh"]
