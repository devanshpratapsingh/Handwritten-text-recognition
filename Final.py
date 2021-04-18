#Importing required libraries, i.e. OpenCV, Numpy and Tensor Flow
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image

#importing the dataset form mnist
mnist=tf.keras.datasets.mnist
#splitting the data in training and testing datasets
(x_train, y_train), (x_test, y_test) = mnist.load_data() 

#scaling down the training and test datasets
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

#defining the model, which'll have a input layer, two hidden layers and an output layer
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28,28)))  #flatten means it's a simple feet forwaed neural network
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))  #dense means all the neurons are connected to
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))#previous and the next layer
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
loss, accuracy= model.evaluate(x_test, y_test)
print(accuracy)
print(loss)

model.save('model.h5')

''' Testing with different inputs '''
for x in range(1,6):
    image = Image.open(str(x)+'.jpeg')
    image = np.array(image.resize((28, 28), Image.ANTIALIAS))
    image = np.array(image, dtype='uint8' )
    image = image[:,:,0]
    image = np.invert(np.array([image]))
    prediction = model.predict(image)
    print(f'Probably the result is: {np.argmax(prediction)}')
    plt.imshow(image[0], cmap=plt.cm.binary)
    plt.show()