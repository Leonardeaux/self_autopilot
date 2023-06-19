import pandas as pd
import zipfile


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
