import pandas as pd
import zipfile
import numpy as np
import os
import ast
from PIL import Image


def get_data_and_zip(data_file_name: str):
    train_data = pd.read_csv(data_file_name, sep=';')

    compression = zipfile.ZIP_DEFLATED

    zf = zipfile.ZipFile("data_archives/data_archive.zip", mode="w")
    try:
        zf.write(data_file_name, data_file_name, compress_type=compression)
        for file_name in train_data['image_name']:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            zf.write("images/" + file_name, file_name, compress_type=compression)
    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()


def load_images(df, img_dir):
    image_list = []
    for image_name in df['image_name']:
        image_path = os.path.join(img_dir, image_name)
        img = Image.open(image_path).convert('L')  # Convert to grayscale

        image_list.append(np.array(img))
    return np.array(image_list)


def convert_string_to_list(input_str):
    return ast.literal_eval(input_str)


def param_to_message(**kwargs: str):
    json_message = "{"
    for key, value in kwargs.items():
        json_message += f'"{key}": {value},'

    json_message = json_message[:-1]
    json_message += '}'
    return json_message
