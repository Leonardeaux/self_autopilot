import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization, Input, concatenate
from keras.optimizers import SGD


def AlexNet_model(input_shape, n_class, learning_rate) -> Sequential:
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

    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(learning_rate=learning_rate),
                  metrics=['accuracy'])
    model.summary()

    return model


def AlexNet_model_with_additional_data(input_shape, additional_info_dim, n_class, learning_rate) -> Sequential:
    image_input = Input(shape=input_shape)
    x = Conv2D(filters=128, kernel_size=(11, 11), strides=(4, 4), activation='relu')(image_input)
    x = BatchNormalization()(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = Conv2D(filters=256, kernel_size=(5, 5), strides=(1, 1), activation='relu', padding="same")(x)
    x = BatchNormalization()(x)
    x = MaxPool2D(pool_size=(3, 3))(x)
    x = Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding="same")(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=256, kernel_size=(1, 1), strides=(1, 1), activation='relu', padding="same")(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=256, kernel_size=(1, 1), strides=(1, 1), activation='relu', padding="same")(x)
    x = BatchNormalization()(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = Flatten()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    image_model = Model(inputs=image_input, outputs=x)

    additional_input_1 = Input(shape=(additional_info_dim,))
    y = Dense(32, activation='relu')(additional_input_1)
    y = Dropout(0.5)(y)
    additional_model = Model(inputs=additional_input_1, outputs=y)

    additional_input_2 = Input(shape=(additional_info_dim,))
    y2 = Dense(32, activation='relu')(additional_input_2)
    y2 = Dropout(0.5)(y2)
    additional_model_2 = Model(inputs=additional_input_2, outputs=y2)

    additional_input_3 = Input(shape=(additional_info_dim,))
    y3 = Dense(32, activation='relu')(additional_input_3)
    y3 = Dropout(0.5)(y3)
    additional_model_3 = Model(inputs=additional_input_3, outputs=y3)

    combined = concatenate(
        [image_model.output, additional_model.output, additional_model_2.output, additional_model_3.output]
    )
    z = Dense(256, activation='relu')(combined)
    z = Dropout(0.5)(z)
    z = Dense(n_class, activation='softmax')(z)

    model = Model(
        inputs=[image_model.input, additional_model.input, additional_model_2.input, additional_model_3.input],
        outputs=z)

    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(learning_rate=learning_rate),
                  metrics=['accuracy'])
    model.summary()

    return model
