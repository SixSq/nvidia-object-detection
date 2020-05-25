from imutils.video import VideoStream
import cv2
import numpy as np

def imageGenerator():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    ret, jpeg = cv2.imencode('.jpg', frame,
                                 (cv2.IMWRITE_JPEG_QUALITY, self.quality))
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')


if __name__ == "__main__":
    pass        
