import random
import numpy as np
import settings
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten


def create_model():
    model = Sequential([
        Embedding(3, 2, input_length=24),
        Flatten(),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(8, activation='sigmoid'),
    ])
    model.compile(optimizer='rmsprop', loss="categorical_crossentropy")
    return model