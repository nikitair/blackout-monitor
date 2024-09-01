import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s UTC - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')


logs_file_path = os.path.join("logs", "logs.log")
        

# handlers
terminal_handler = logging.StreamHandler()
file_handler = logging.FileHandler(logs_file_path)

# Terminal output
terminal_handler.setLevel(logging.INFO)
terminal_handler.setFormatter(formatter)
logger.addHandler(terminal_handler)

# File output
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
