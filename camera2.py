from imutils.video import VideoStream
import cv2
import numpy as np

def imageGenerator():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


if __name__ == "__main__":
    pass        
