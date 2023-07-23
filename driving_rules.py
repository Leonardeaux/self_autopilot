import tensorflow as tf
import numpy as np
import cv2
from typing import Dict
from game_events import *
from variables import N_CLASS, IMG_RESIZING, BOX
from mss import mss
from get_inputs import key_check
from acc_mmap import read_physics

sct = mss()


def not_really_an_ai(lane_slope_1: float, lane_slope_2: float) -> None:
    if lane_slope_1 < 0 and lane_slope_2 < 0:
        right_event()
    elif lane_slope_1 > 0 and lane_slope_2 > 0:
        left_event()
    else:
        forward_event()


def supervised_trained_driving(model_name: str, box: Dict[str, int]):
    model = tf.keras.models.load_model(f"models/{model_name}")

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False

    while True:
        if not paused:
            stream = sct.grab(box)
            frame = np.array(stream)
            cv2.imshow("game", frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (IMG_RESIZING[1], IMG_RESIZING[0]))

            # moves = list(np.around(model.predict([frame])[0]))
            moves = list(
                np.around(
                    model.predict(
                        frame.reshape(
                            -1, IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]
                        )
                    )[0]
                )
            )
            # moves = model.predict(frame.reshape(-1, IMG_RESIZING[0], IMG_RESIZING[1], IMG_RESIZING[2]))
            print(moves)

            # [(Q), (Z, Q), (Z), (Z, D), (D), (S, Q), (S), (S, D)] boolean values.
            if moves == [1, 0, 0, 0, 0, 0, 0, 0]:
                left_event()
            elif moves == [0, 1, 0, 0, 0, 0, 0, 0]:
                forward_left_event()
            elif moves == [0, 0, 1, 0, 0, 0, 0, 0]:
                forward_event()
            elif moves == [0, 0, 0, 1, 0, 0, 0, 0]:
                forward_right_event()
            elif moves == [0, 0, 0, 0, 1, 0, 0, 0]:
                right_event()
            elif moves == [0, 0, 0, 0, 0, 1, 0, 0]:
                backward_left_event()
            elif moves == [0, 0, 0, 0, 0, 0, 1, 0]:
                backward_event()
            elif moves == [0, 0, 0, 0, 0, 0, 0, 1]:
                backward_right_event()

        if cv2.waitKey(25) & 0xFF == ord("w"):
            cv2.destroyAllWindows()
            break

        keys = key_check()

        if "T" in keys:
            if paused:
                paused = False
            else:
                paused = True
                release_all_movements_keys()


def supervised_trained_driving_with_speed(model_name: str, box: Dict[str, int]):
    model = tf.keras.models.load_model(f"models/{model_name}")

    for i in list(range(5))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False

    while True:
        if not paused:
            stream = sct.grab(box)
            frame = np.array(stream)
            cv2.imshow(
                "game", cv2.resize(frame, (IMG_RESIZING[1] * 4, IMG_RESIZING[0] * 4))
            )
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (IMG_RESIZING[1], IMG_RESIZING[0]))

            # moves = list(np.around(model.predict([frame])[0]))
            car_infos = read_physics()
            moves = np.argmax(
                model.predict(
                    [
                        frame.reshape(
                            -1, IMG_RESIZING[1], IMG_RESIZING[0], IMG_RESIZING[2]
                        ),
                        np.array([car_infos[0]]),
                        np.array([car_infos[1]]),
                        np.array([car_infos[2]]),
                    ]
                )[0]
            )
            print(moves)

            # [(Q), (Z, Q), (Z), (Z, D), (D), (S, Q), (S), (S, D)] boolean values.
            if moves == 0:
                left_event()
            elif moves == 1:
                forward_left_event()
            elif moves == 2:
                forward_event()
            elif moves == 3:
                forward_right_event()
            elif moves == 4:
                right_event()
            elif moves == 5:
                backward_left_event()
            elif moves == 6:
                backward_event()
            elif moves == 7:
                backward_right_event()

        if cv2.waitKey(25) & 0xFF == ord("w"):
            cv2.destroyAllWindows()
            break

        keys = key_check()

        if "T" in keys:
            if paused:
                paused = False
            else:
                paused = True
                release_all_movements_keys()
