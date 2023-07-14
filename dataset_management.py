import os
import numpy as np
import datetime
import cv2
import time
import pandas as pd
import shutil
from sklearn.utils import resample
from PIL import Image
from typing import List
from random import shuffle
from collections import Counter
from grab_screen import grab_screen
from get_inputs import keys_to_one_hot, key_check, one_hot_to_keys
from variables import TOP_2K, LEFT_2K, WIDTH_2K, HEIGHT_2K, IMG_RESIZING, TOP_ACC, LEFT_ACC, WIDTH_ACC, HEIGHT_ACC
from acc_mmap import read_physics
from utils import get_data_and_zip, convert_string_to_list


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

    shutil.copyfile(file_name,
                    f'data_archive/training_data_{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.npy')

    file_name_tmp = 'training_data_tmp.npy'

    training_data_tmp = []

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    while True:

        screen = grab_screen(LEFT_2K, TOP_2K, WIDTH_2K, HEIGHT_2K)

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

    print(
        f'training_data = {len(training_data)} - training_data_tmp = {len(training_data_tmp)} - final_data = {len(final_data)}')

    np.save(file_name, final_data)


def launch_dataset_feeding_v2() -> None:
    file_name = 'training_data.csv'

    get_data_and_zip(file_name)

    training_file = open(file_name, 'a')

    counter = 0
    wait_c = 0

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    while True:

        screen = grab_screen(LEFT_ACC, TOP_ACC, WIDTH_ACC, HEIGHT_ACC)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, IMG_RESIZING[:-1])
        cv2.imshow("video", screen)

        keys = key_check()
        inputs = keys_to_one_hot(keys)

        car_infos = read_physics()

        timestamp = time.time()
        image_filename = f"image_{counter}_{timestamp}.png"

        line = f"{timestamp};{image_filename};{inputs};{car_infos[0]};{car_infos[1]};{car_infos[2]}\n"

        # print("outputs = {} - keys = {}".format(output, one_hot_to_keys(output))) # Print inputs with equivalent keys

        if counter == 0 or counter % 500 != 0 or wait_c == 50:
            counter += 1
            cv2.imwrite(f'images/{image_filename}', screen)
            training_file.write(line)
            wait_c = 0
        else:
            print('wait...' + str(wait_c))
            wait_c += 1

        if cv2.waitKey(25) & 0xFF == ord('w'):
            cv2.destroyAllWindows()
            break

    training_file.close()


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


def balance_data_v2(file_name):
    train_data = pd.read_csv(file_name, sep=';')

    class_counts = train_data['inputs'].value_counts()

    print(f'Unbalanced dataset : \n{class_counts}')

    min_class_size = class_counts.min()

    balanced_df = pd.DataFrame()

    for class_tuple, count in class_counts.items():
        class_subset = train_data[train_data['inputs'] == class_tuple]
        class_subset_downsampled = resample(class_subset,
                                            replace=False,
                                            n_samples=min_class_size,
                                            random_state=42)
        balanced_df = pd.concat([balanced_df, class_subset_downsampled])

    balanced_class_counts = balanced_df['inputs'].value_counts()

    print(f'Balanced dataset : \n{balanced_class_counts}')

    balanced_df['inputs'] = balanced_df['inputs'].apply(convert_string_to_list)

    return balanced_df, min_class_size


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


def view_dataset_v2(file_name: str):
    train_data = pd.read_csv(file_name, sep=';')

    for image_name in train_data['image_name']:
        img = cv2.imread(f'images/{image_name}')

        cv2.imshow('screen', img)

        if cv2.waitKey(25) & 0xFF == ord('w'):
            cv2.destroyAllWindows()
            break
