import cv2
import numpy as np
import imutils
import datetime
import matplotlib.pyplot as plt
import pathlib
from PIL import Image


def saveImage(path):
    cap = cv2.VideoCapture('http://192.168.40.68:8082/?action=snapshot')
    ret, f = cap.read()
    plt.imsave(path, f, cmap='Greys')


def openImage(path):
    return np.asarray(Image.open(path))

def get_img_contour_thresh(img):
    print(img.shape)
    x, y, w, h = (200, 20, 600, 1000)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)
    ret, thresh1 = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresh1 = thresh1[y:y + h, x:x + w]
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    return img, contours, thresh1


def extractNumbers(imagePath, save=False, savePath=None, show=False):
    frame = openImage(imagePath)

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(imgray, (35, 35), 0)


    # The threshold is really high to improve number recognition.
    # If the threshold was lower, small imperfection in the number might become false detections.
    thresh = cv2.threshold(blur, 255, 255,  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    imgID = 0

    filepath = 'testOut_{}.png'

    for c in contours:

        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        newImage = thresh[y:y + h, x:x + w]
        newImage = cv2.resize(newImage, (28, 28))
        newImage = np.array(newImage)
        if save:
            plt.imsave(filepath.format(str(imgID)), newImage, cmap='Greys')
            imgID += 1
        if show:
            cv2.imshow('Number', newImage)
            cv2.waitKey()
        yield newImage



if __name__ == "__main__":
    imagePath = 'test4.png'
    saveImage(imagePath)

    savePath = 'test-{}.png'

    extractNumbers(imagePath, show=True)
