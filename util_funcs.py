import json
import re

def read_file():
    try:
        with open("airplanes.json", "r", newline=None) as text_file:
            return json.load(text_file)
    except Exception as e:
        print(e)


def find_airplane(plane):
    airplanes = read_file()
    if plane in airplanes:
        return True
    return False

