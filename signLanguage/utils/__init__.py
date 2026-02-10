import os.path
import sys
import yaml
import base64

from signLanguage.exception import SignException
from signLanguage.logger import logging

def read_yaml(filepath: str) -> dict:
    try:
        with open(filepath, "rb") as yaml_file:
            logging.info("Read yaml file successful")
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SignException(e, sys)
    

def write_yaml_file(filepath: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml file")

    except Exception as e:
        raise SignException(e, sys)
    
def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open("./data/"+filename, "wb") as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagedPath):
    with open(croppedImagePaht, "rb") as f:
        return base64.b64encode(f.read())