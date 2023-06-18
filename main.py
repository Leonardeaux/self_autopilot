import time
import cv2
import numpy as np
import os
import datetime
import tensorflow as tf
from utils import N_CLASS, IMG_RESIZING
from dataset_management import launch_dataset_feeding, launch_dataset_feeding_v2, view_dataset_v2,test
from supervised_training import AlexNet_training

if __name__ == '__main__':

    # AlexNet_training(input_shape=IMG_RESIZING,
    #                  n_class=N_CLASS,
    #                  exp_name="AlexNet_model",
    #                  epochs=15,
    #                  learning_rate=0.001,
    #                  validation_split_value=0.2)
    test()
    # view_dataset_v2("training_data.csv")
