import numpy as np
import pandas as pd
import tensorflow as tf
from collections import Counter
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split
from utils import load_images
from dataset_management import balance_data, balance_data_v2, charge_train_dataset
from typing import Tuple
from AlexNet import AlexNet_model, AlexNet_model_with_additional_data
from ast import literal_eval


def AlexNet_training(input_shape: Tuple[int, int, int],
                     n_class: int, epochs: int = 10,
                     learning_rate: float = 0.001,
                     validation_split_value: float = 0.2) -> None:
    model_name = f'AlexNet_model_epochs_{epochs}_lr_{learning_rate}'

    final_data, max_nb_target = balance_data('training_data.npy')

    model = AlexNet_model(input_shape=input_shape, n_class=n_class, learning_rate=learning_rate)

    nb_test_values = int(max_nb_target * validation_split_value)

    train = final_data[:-nb_test_values]
    test = final_data[-nb_test_values:]

    train_x = np.array([i[0] for i in train]).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    train_y = np.array([i[1] for i in train])

    test_x = np.array([i[0] for i in test]).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    test_y = np.array([i[1] for i in test])

    model.fit(train_x, train_y,
              epochs=epochs,
              validation_data=(test_x, test_y),
              callbacks=[
                  tf.keras.callbacks.TensorBoard("tensorboard_logs/alexnet/" + model_name)
              ])

    model.save("models/" + model_name)


def AlexNet_training_with_class_weights(input_shape: Tuple[int, int, int],
                                        n_class: int, epochs: int = 10,
                                        learning_rate: float = 0.001,
                                        validation_split_value: float = 0.2) -> None:
    model_name = f'AlexNet_model_with_class_weights_epochs_{epochs}_lr_{learning_rate}'

    final_data = charge_train_dataset('training_data.npy')

    df = pd.DataFrame(final_data)

    nb_targets = Counter(df[1].apply(str))

    min_target = np.min(list(nb_targets.values()))

    model = AlexNet_model(input_shape=input_shape,
                          n_class=n_class,
                          learning_rate=learning_rate)

    nb_test_values = int(min_target * validation_split_value)

    train = final_data[:-nb_test_values]
    test = final_data[-nb_test_values:]

    train_x = np.array([i[0] for i in train]).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    train_y = np.array([i[1] for i in train])

    test_x = np.array([i[0] for i in test]).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    test_y = np.array([i[1] for i in test])

    # Convert one-hot encoded targets to integer labels
    y_integers = np.argmax(train_y, axis=1)

    # Calculate class weights
    class_weights = compute_class_weight(class_weight='balanced',
                                         classes=np.unique(y_integers),
                                         y=y_integers)
    class_weights = dict(enumerate(class_weights))

    print(class_weights)

    model.fit(train_x, train_y,
              epochs=epochs,
              validation_data=(test_x, test_y),
              class_weight=class_weights,
              callbacks=[
                  tf.keras.callbacks.TensorBoard("tensorboard_logs/alexnet/" + model_name)
              ])

    model.save("models/" + model_name)


def AlexNet_with_additional_data(input_shape: Tuple[int, int, int],
                                 additional_info_dim: int,
                                 n_class: int,
                                 epochs: int = 10,
                                 learning_rate: float = 0.001,
                                 validation_split_value: float = 0.2) -> None:
    file_name = "training_data.csv"

    model_name = f'AlexNet_model_with_additional_data_epochs_{epochs}_lr_{learning_rate}'

    final_data, max_nb_target = balance_data_v2(file_name)

    df_train, df_test = train_test_split(final_data, test_size=validation_split_value, random_state=42)

    train_images = load_images(df_train, "images")
    train_images = np.expand_dims(train_images, axis=-1)

    test_images = load_images(df_test, "images")
    test_images = np.expand_dims(test_images, axis=-1)

    train_speeds = df_train["speed"]
    test_speeds = df_test["speed"]
    train_throttles = df_train["throttle"]
    test_throttles = df_test["throttle"]
    train_brakes = df_train["brake"]
    test_brakes = df_test["brake"]

    train_y = df_train["inputs"].values
    train_y = np.array(train_y.tolist())
    train_y = tf.convert_to_tensor(train_y)

    test_y = df_test["inputs"].values
    test_y = np.array(test_y.tolist())
    test_y = tf.convert_to_tensor(test_y)

    # print(train_images.shape)
    # print(len(train_speeds))
    # print(len(train_throttles))
    # print(len(train_brakes))
    # print(len(train_y))

    model = AlexNet_model_with_additional_data(input_shape=input_shape,
                                               additional_info_dim=additional_info_dim,
                                               n_class=n_class,
                                               learning_rate=learning_rate)

    model.fit([train_images, train_speeds, train_throttles, train_brakes], train_y,
              epochs=epochs,
              validation_data=([test_images, test_speeds, test_throttles, test_brakes], test_y),
              callbacks=[
                  tf.keras.callbacks.TensorBoard("tensorboard_logs/alexnet/" + model_name)
              ])

    model.save("models/" + model_name)
