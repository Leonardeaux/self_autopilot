import numpy as np
import tensorflow as tf
from dataset_management import balance_data
from typing import Tuple
from AlexNet import AlexNet_model


def AlexNet_training(input_shape: Tuple[int, int, int],
                     exp_name: str,
                     n_class: int, epochs: int = 10,
                     learning_rate: float = 0.001,
                     validation_split_value: float = 0.2) -> None:

    model_name = f'{exp_name}_epochs_{epochs}_lr_{learning_rate}'

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

    model.save(model_name)
