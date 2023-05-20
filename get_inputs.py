import win32api as wapi

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
    keyList.append(char)


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def keys_to_one_hot(keys):
    """
    Convert keys to a ...multi-hot... array

    [(Q), (Z, Q), (Z), (Z, D), (D), (S, Q), (S), (S, D)] boolean values.
    """
    one_hot = [0, 0, 0, 0, 0, 0, 0, 0]

    if 'Z' in keys and 'Q' in keys:
        one_hot[1] = 1
    elif 'Z' in keys and 'D' in keys:
        one_hot[3] = 1
    elif 'S' in keys and 'Q' in keys:
        one_hot[5] = 1
    elif 'S' in keys and 'D' in keys:
        one_hot[7] = 1
    elif 'Q' in keys:
        one_hot[0] = 1
    elif 'D' in keys:
        one_hot[4] = 1
    elif 'S' in keys:
        one_hot[6] = 1
    else:
        one_hot[2] = 1

    return one_hot


def one_hot_to_keys(one_hot):
    if one_hot[1] == 1:
        keys = ['Z', 'Q']
    elif one_hot[3] == 1:
        keys = ['Z', 'D']
    elif one_hot[5] == 1:
        keys = ['S', 'Q']
    elif one_hot[7] == 1:
        keys = ['S', 'D']
    elif one_hot[0] == 1:
        keys = ['Q']
    elif one_hot[4] == 1:
        keys = ['D']
    elif one_hot[6] == 1:
        keys = ['S']
    else:
        keys = ['Z']

    return keys
