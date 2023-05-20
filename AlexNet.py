import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.optimizers import SGD


def AlexNet_model(input_shape, n_class, learning_rate, validation_split_value, exp_name) -> Sequential:
    model = Sequential([
        Conv2D(filters=128, kernel_size=(11, 11), strides=(4, 4), activation='relu',
               input_shape=input_shape),
        BatchNormalization(),
        MaxPool2D(pool_size=(2, 2)),
        Conv2D(filters=256, kernel_size=(5, 5), strides=(1, 1), activation='relu', padding="same"),
        BatchNormalization(),
        MaxPool2D(pool_size=(3, 3)),
        Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding="same"),
        BatchNormalization(),
        Conv2D(filters=256, kernel_size=(1, 1), strides=(1, 1), activation='relu', padding="same"),
        BatchNormalization(),
        Conv2D(filters=256, kernel_size=(1, 1), strides=(1, 1), activation='relu', padding="same"),
        BatchNormalization(),
        MaxPool2D(pool_size=(2, 2)),
        Flatten(),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(n_class, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=SGD(learning_rate=learning_rate),
                  metrics=['accuracy'])
    model.summary()

    return model
