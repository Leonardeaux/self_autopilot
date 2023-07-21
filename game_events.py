import time
from generic_inputs import INPUTS_DICT, PressKey, ReleaseKey


def restart_event():
    PressKey(INPUTS_DICT["ESCAPE"])
    time.sleep(0.5)
    PressKey(INPUTS_DICT["ENTER"])


def release_all_movements_keys():
    ReleaseKey(INPUTS_DICT["UP"])
    ReleaseKey(INPUTS_DICT["DOWN"])
    ReleaseKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["RIGHT"])


def forward_event():
    PressKey(INPUTS_DICT["UP"])
    ReleaseKey(INPUTS_DICT["DOWN"])
    ReleaseKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["LEFT"])


def backward_event():
    PressKey(INPUTS_DICT["DOWN"])
    ReleaseKey(INPUTS_DICT["UP"])
    ReleaseKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["LEFT"])


def right_event():
    PressKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["UP"])
    ReleaseKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["DOWN"])


def left_event():
    PressKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["UP"])
    ReleaseKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["DOWN"])


def forward_left_event():
    PressKey(INPUTS_DICT["UP"])
    PressKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["DOWN"])


def forward_right_event():
    PressKey(INPUTS_DICT["UP"])
    PressKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["DOWN"])


def backward_left_event():
    PressKey(INPUTS_DICT["DOWN"])
    PressKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["UP"])


def backward_right_event():
    PressKey(INPUTS_DICT["DOWN"])
    PressKey(INPUTS_DICT["RIGHT"])
    ReleaseKey(INPUTS_DICT["LEFT"])
    ReleaseKey(INPUTS_DICT["UP"])
