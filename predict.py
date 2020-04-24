from __future__ import absolute_import, division, print_function, unicode_literals

import os

import tensorflow as tf
import numpy as np
import random
from utils import arrayToImage, showImage, imageToArray
from flask import Flask, request, url_for, redirect
import json
import paho.mqtt.client as mqtt
import namegenerator

app = Flask(__name__)

CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def predict(model, image):
    """Returns the predicted value.

    Arguments:
        model {string} -- Path to the model used for prediction
        image {Numpy Array} -- Array containing the image to be predicted.
    """
    image = np.reshape(image, [1, 28, 28])
    # The predict function is expecting an array of images.
    # When we iterate over that array, or when we just pass one single image, we need to convert the 2D array
    #   to 3D, indicating there is only one image.
    loaded_model = tf.keras.models.load_model(model)
    prediction = loaded_model.predict(image)
    predictionClass = np.argamax(prediction)
    if prediction.max() < np.float(0.6):
        name = namegenerator.gen() + '.png'
        imagePath = './savedImages/' + name
        os.system('s3cmd put {imagePath} s3://{s3Name}/{bucketName}/{fileName}'.format(imagePath= imagePath, s3Name=os.environ['S3_NAME'], bucketName='images', fileName=name))
    return predictionClass


def randomPrediction(model):
    """Takes a random image from the test images and predicts it.
    Used in the website.

    Arguments:
        model {string} -- Path to the model used for prediction
    """
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (test_images, test_labels) = fashion_mnist.load_data()[1]
    a = list(zip(test_images, test_labels)) # First elem the image, second the label
    randomChoice = random.choice(a)
    return randomChoice, predict(model, randomChoice[0])


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connection Successful! Returned code =",rc)
    else:
        print("Unable to Connect. Returned code =", rc)

def on_message(client, userdata, msg):
    if msg.topic == 'newModel':
        name = str(msg.payload.decode('utf-8'))
        os.system('s3cmd get s3://{}/{}/{} ./model/{}'.format(os.environ['S3_NAME'], 'model', name, name))
        for i in os.listdir('./model/'):
            os.rename('./model/' + i, './savedModels/' + i)

if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # TODO: Change the IP for a ENV Variable.
    client.connect('194.182.182.137', 1883, 60)
    client.subscribe('newModel')
    client.loop_start()
    # app.run(host="0.0.0.0", port=5000)