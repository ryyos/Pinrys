import logging
from datetime import datetime as time
from icecream import ic



logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', encoding="utf-8", level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG) 
console.setFormatter(formatter)

file_log = logging.FileHandler(filename="logs/logging.log", encoding="utf-8")
file_log.setLevel(level=logging.DEBUG)
file_log.setFormatter(formatter)

logger = logging.getLogger()
for existing_handler in logger.handlers[:]:
       logger.removeHandler(existing_handler)

logger.addHandler(console)
logger.addHandler(file_log)

