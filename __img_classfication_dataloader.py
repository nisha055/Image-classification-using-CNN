# -*- coding: utf-8 -*-
"""img_classfication_dataloader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x51XUamNHraoPktrsOVOSJQ9soaud_12
"""

import keras
import os
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from keras.layers import Input, Lambda
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.models import Sequential
import numpy as np
import random
from keras.preprocessing.image import load_img

dataset_path = 'seg_train/seg_train'
valid_path = 'seg_test/seg_test'


def data_reading(dataset_path):
    all_labels = {}
    all_images = []
    for folders in os.listdir(dataset_path):
        if folders != ".DS_Store":
            folder_path = os.path.join(dataset_path, folders)
            all_labels[folders] = len(all_labels)
            for images in os.listdir(folder_path):
                if images != ".DS_Store":
                    image_path = os.path.join(folder_path, images)
                    all_images.append(image_path)

    rev_labels = {}
    for key, labels in all_labels.items():
        rev_labels[labels] = key

    return all_images, all_labels, rev_labels


def data_loader(bs, data, y_lab, image_input_shape):
    while True:
        images = []
        labels = []
        while len(images) < bs:
            indice = random.randint(0, len(data) - 1)
            target = data[indice].split("/")[-2]
            labels.append(y_lab[target])

            test_img = np.asarray(
                load_img(data[indice], target_size=image_input_shape))
            img = np.divide(test_img, 255.0)
            images.append(img)

        yield np.asarray(images), np.asarray(labels)


def model_arc(y_labels, image_inp_shape):
    inp_layer_images = Input(shape=image_inp_shape)

    conv_layer = Conv2D(filters=64, kernel_size=(2, 2), activation="relu")(
        inp_layer_images
    )
    flatten_layer = Flatten()(conv_layer)
    out_layer = Dense(len(y_labels), activation="softmax")(flatten_layer)
    model = Model(inp_layer_images, out_layer)
    model.summary()
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def train(dataset_path, batch_size, epochs, input_shape):
    all_images, all_labels, rev_labels = data_reading(
        dataset_path=dataset_path)

    print("target_encodings: ", all_labels)
    print("Number of training images: ", len(all_images))

    train_generator = data_loader(
        bs=batch_size, y_lab=all_labels, image_input_shape=input_shape, data=all_images
    )

    model = model_arc(y_labels=all_labels, image_inp_shape=input_shape)

    history = model.fit_generator(
        generator=train_generator,
        steps_per_epoch=(len(all_images) // batch_size),
        epochs=epochs,
    )
    print('Training Accuracy = ' +
          str(max(history.history['accuracy'])*100) + '%')


batch_size = 8
epochs = 10
input_shape = (100, 100, 3)
train(
    dataset_path=dataset_path,
    batch_size=batch_size,
    epochs=epochs,
    input_shape=input_shape,
)