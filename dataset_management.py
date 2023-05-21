import os
import numpy as np
import datetime
import cv2
import time
import pandas as pd
import shutil
from typing import List
from random import shuffle
from collections import Counter
from grab_screen import grab_screen
from get_inputs import keys_to_one_hot, key_check, one_hot_to_keys
from utils import TOP_BIG, LEFT_BIG, WIDTH_BIG, HEIGHT_BIG, IMG_RESIZING


def charge_train_dataset(file_name) -> List[np.array]:
    if os.path.isfile(file_name):
        print('File exists, loading previous data')
        training_data = list(np.load(file_name, allow_pickle=True))
    else:
        print('File does not exist ')
        training_data = []

    return training_data


def save_data(file_name, data):
    np.save(file_name, data)


def launch_dataset_feeding() -> None:
    file_name = 'training_data.npy'

    shutil.copyfile(file_name, f'data_archive/training_data_{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.npy')

    file_name_tmp = 'training_data_tmp.npy'

    training_data_tmp = []

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    while True:

        screen = grab_screen(LEFT_BIG, TOP_BIG, WIDTH_BIG, HEIGHT_BIG)

        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        screen = cv2.resize(screen, IMG_RESIZING[:-1])
        keys = key_check()
        inputs = keys_to_one_hot(keys)
        training_data_tmp.append(np.array([screen, inputs], dtype=object))
        cv2.imshow("video", screen)
        # print("outputs = {} - keys = {}".format(output, one_hot_to_keys(output)))
        if cv2.waitKey(25) & 0xFF == ord('w'):
            cv2.destroyAllWindows()
            break

        if len(training_data_tmp) % 500 == 0:
            np.save(f'data_tmp/{file_name_tmp}', training_data_tmp)
            print("{}".format(len(training_data_tmp)))

    training_data = charge_train_dataset(file_name)
    training_data_tmp = np.load(f'data_tmp/{file_name_tmp}', allow_pickle=True)

    final_data = np.vstack((training_data, training_data_tmp))

    print(f'training_data = {len(training_data)} - training_data_tmp = {len(training_data_tmp)} - final_data = {len(final_data)}')

    np.save(file_name, final_data)


def balance_data(file_name):
    train_data = charge_train_dataset(file_name)

    df = pd.DataFrame(train_data)

    nb_targets = Counter(df[1].apply(str))

    min_target = np.min(list(nb_targets.values()))

    lefts = []
    lefts_forwards = []
    forwards = []
    rights_forwards = []
    rights = []
    backwards_lefts = []
    backwards = []
    backwards_rights = []

    shuffle(train_data)

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == [1, 0, 0, 0, 0, 0, 0, 0]:
            lefts.append([img, choice])
        elif choice == [0, 1, 0, 0, 0, 0, 0, 0]:
            lefts_forwards.append([img, choice])
        elif choice == [0, 0, 1, 0, 0, 0, 0, 0]:
            forwards.append([img, choice])
        elif choice == [0, 0, 0, 1, 0, 0, 0, 0]:
            rights_forwards.append([img, choice])
        elif choice == [0, 0, 0, 0, 1, 0, 0, 0]:
            rights.append([img, choice])
        elif choice == [0, 0, 0, 0, 0, 1, 0, 0]:
            backwards_lefts.append([img, choice])
        elif choice == [0, 0, 0, 0, 0, 0, 1, 0]:
            backwards.append([img, choice])
        elif choice == [0, 0, 0, 0, 0, 0, 0, 1]:
            backwards_rights.append([img, choice])
        else:
            print('no matches')

    lefts = lefts[:min_target]
    lefts_forwards = lefts_forwards[:min_target]
    forwards = forwards[:min_target]
    rights_forwards = rights_forwards[:min_target]
    rights = rights[:min_target]
    backwards_lefts = backwards_lefts[:min_target]
    backwards = backwards[:min_target]
    backwards_rights = backwards_rights[:min_target]

    final_data = lefts + lefts_forwards + forwards + rights_forwards + rights + backwards_lefts + backwards + backwards_rights
    shuffle(final_data)
    return final_data, min_target


def view_dataset(file_name: str):
    train_data = charge_train_dataset(file_name)[-1000:]
    i = 0
    while True:
        cv2.imshow("image", train_data[i][0])
        print(train_data[i][1])
        i += 1

        if cv2.waitKey(25) & 0xFF == ord('w'):
            cv2.destroyAllWindows()
            break
