import argparse
import sys
import os

model_path = 'model-dropout'

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", help="Dataset file", required=True)
args = parser.parse_args()

if os.path.exists(args.dataset):
    print('Cannot find dataset!')
    sys.exit()

from keras.models import Sequential
from keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import Dense
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
import pickle
import numpy as np
from keras.layers import Dropout
import keras.backend as K

def euclidean_distance_loss(y_true, y_pred):
    """
    Euclidean distance loss
    https://en.wikipedia.org/wiki/Euclidean_distance
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    return K.sqrt(K.sum(K.square(y_pred - y_true), axis=-1))


resnet = ResNet50(include_top=False, pooling='avg')
model = Sequential()
model.add(resnet)
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))
model.layers[0].trainable = False
print(model.summary())

sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='kld', optimizer=sgd, metrics=['accuracy'])

lable_distribution = pickle.load(open(args.dataset, 'rb'))

train_X = np.array([x[1] for x in lable_distribution[0:len(lable_distribution)]])
train_Y = np.array([x[2] for x in lable_distribution[0:len(lable_distribution)]])

earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='auto')

history = model.fit(
    x=train_X,
    y=train_Y,
    batch_size=32,
    callbacks=[earlyStopping],
    epochs=100,
    verbose=1,
    validation_split=0.1
)

model_name = '{}/model-ldl-resnet.h5'.format(model_path)
model.save_weights(model_name)
print('Data training is completed, your model is saved to {}'.format(model_name))
