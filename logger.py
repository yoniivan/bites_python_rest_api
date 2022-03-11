from enum import Enum
import json


class logger(Enum):
    ERROR = 0
    WARNING = 1
    DEBUG = 2
    SUCCESS = 3
    INFO = 4


def log(level, class_name, function_name, message):
    try:
        log = {
            "level": str(level),
            "class_name": str(class_name),
            "function_name": str(function_name),
            "message": str(message)
        }
        print(json.dumps(log))
    except Exception as e:
        print(e)

