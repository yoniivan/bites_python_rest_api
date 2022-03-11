import os
from logger import log, logger
import pymongo
import json
from util_funcs import find_airplane


class_name = "postgres.py"
cols = {"_id": 0, "id": 1, "airplane_id": 1, "serial_number": 1, "description": 1, "deleted": 1}


def insert_airplane(item):
    try:
        conn = open_connection()
        id = item.get("id")
        serial_number = item.get("serial_number")
        airplane_id = item.get("airplane_id")
        description = item.get("description")
        is_in_list = find_airplane(airplane_id)

        if is_in_list is False:
            return False

        db_id = conn.airplanes.find_one({"$or": [{"id": id}, {"serial_number": serial_number}]})
        print("db_id" ,db_id)
        if db_id is None:
          obj = {
              "id": id,
              "airplane_id": airplane_id,
              "serial_number": serial_number,
              "description": description,
              "deleted": False
          }
          conn.airplanes.insert_one(obj)
          return True
        else:
            return False

    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "insert_airplane", message)


def get_airplanes():
    try:
        conn = open_connection()
        get = conn.airplanes.find({}, cols)
        items = list(get)
        print(items)
        arr = []
        # deleted no included in the query because it is supposed to be visible for the server
        for item in items:
            if item["deleted"] is False:
                arr.append(item)

        return arr
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "get_airplanes", message)

def find_one(id):
    try:
        conn = open_connection()
        # deleted no included in the query because it is supposed to be visible for the server
        get = conn.airplanes.find_one({"id": str(id)},cols)
        print("vvvvvvvvvv", get)
        return get if get["deleted"] is False else None
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
            "params": id
        }
        log(logger.ERROR, class_name, "find_one", message)


def update_one(id, set):
    try:
        conn = open_connection()
        get = conn.airplanes.update_one({"id": id}, {"$set": set})
        print("get",get)
        return get
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "find_one", message)




def open_connection():
    try:
        client = pymongo.MongoClient(os.environ["DB_1_PORT_27017_TCP_ADDR"] ,27017)
        db = client.airplanes
        return db
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "open_connection", message)



