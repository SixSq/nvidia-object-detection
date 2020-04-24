import numpy as np
import tempfile
import uuid
from PIL import Image
# import matplotlib.pyplot as plt
from tensorflow import keras

def createTempFilepath():
    return '/tmp/{}.png'.format(str(uuid.uuid4()))

def arrayToImage(array, filepath=None):
    if filepath == None:
      filepath = createTempFilepath()
    img = Image.fromarray(array, 'P')
    img.save(filepath)
    return filepath

def imageToArray(filepath):
    im = Image.open(filepath)
    np_im = np.array(im)
    return np_im

def showImage(path):
    img = Image.open(path)
    img = img.resize((200,200))
    img.show()

def makeImages():
  fashion_mnist = keras.datasets.fashion_mnist
  test_images = fashion_mnist.load_data()[1][0]

  for i, v in enumerate(test_images[:100]):
      arrayToImage(v, './savedImages/{}.png'.format(i))

# def plot_image(i, predictions_array, true_label, img, class_names):
#   print("Entered plot image")
#   predictions_array, true_label, img = predictions_array, true_label[i], img[i]
#   plt.grid(False)
#   plt.xticks([])
#   plt.yticks([])

#   plt.imshow(img)

#   predicted_label = np.argmax(predictions_array)
#   if predicted_label == true_label:
#     color = 'blue'
#   else:
#     color = 'red'

#   plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
#                                 100*np.max(predictions_array),
#                                 class_names[true_label]),
#                                 color=color)

# def plot_value_array(i, predictions_array, true_label):
#   print('entered plot value array')
#   predictions_array, true_label = predictions_array, true_label[i]
#   plt.grid(False)
#   plt.xticks(range(10))
#   plt.yticks([])
#   thisplot = plt.bar(range(10), predictions_array, color="#777777")
#   plt.ylim([0, 1])
#   predicted_label = np.argmax(predictions_array)

#   thisplot[predicted_label].set_color('red')
#   thisplot[true_label].set_color('blue')
#   print('exited plot value array')

# def createModelAccuracyRepresentation(predictions, test_labels, test_images, class_names):
#     print('Entered Model Representation')
#     num_rows = 5
#     num_cols = 3
#     num_images = num_rows*num_cols
#     plt.figure(figsize=(2*2*num_cols, 2*num_rows))
#     for i in range(num_images):
#         plt.subplot(num_rows, 2*num_cols, 2*i+1)
#         plot_image(i, predictions[i], test_labels, test_images, class_names)
#         plt.subplot(num_rows, 2*num_cols, 2*i+2)
#         plot_value_array(i, predictions[i], test_labels)
#     plt.tight_layout()
#     plt.show()
