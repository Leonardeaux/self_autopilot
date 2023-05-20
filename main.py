import time
import cv2
import numpy as np
import os
import datetime
import tensorflow as tf
from utils import N_CLASS, IMG_RESIZING
from supervised_training import AlexNet_training

if __name__ == '__main__':

    AlexNet_training(input_shape=IMG_RESIZING,
                     n_class=N_CLASS,
                     exp_name="AlexNet_model",
                     epochs=10,
                     learning_rate=0.001,
                     validation_split_value=0.2)
