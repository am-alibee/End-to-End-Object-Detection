import sys
from signLanguage.logger import logging
from signLanguage.exception import SignException

logging.info("Hello world")

try:
    a = 4 / "dlsdjfd"
except Exception as e:
    raise SignException(e, sys) from e