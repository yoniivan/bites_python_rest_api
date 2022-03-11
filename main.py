from flask import Flask, request, jsonify
from mongodb import insert_airplane, get_airplanes, find_one, update_one
from logger import log, logger
from marshmallow import Schema, fields, ValidationError
import os
from util_funcs import find_airplane


app = Flask(__name__)
class_name = "main.py"


class BaseSchema(Schema):
    id = fields.String(required=True)
    airplane_id = fields.String(required=True)
    serial_number = fields.String(required=True)
    description = fields.String(required=True)

@app.route('/api/devices/', methods=['GET'])
def get_request():
    try:
        get = get_airplanes()
        return jsonify(get)
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "get_request", message)
        return jsonify(message)


@app.route('/api/devices/', methods=['POST'])
def post_request():
    try:
        schema = BaseSchema()
        content = request.json
        result = schema.load(content)
        res = insert_airplane(result)
        return jsonify({"res": "item updated" if res else "item already exists or airplane does not exist"})

    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "add_device", message)
        return jsonify(message)

@app.route('/api/devices/<id>', methods=['GET'])
def get_request_id(id: str) -> object:
    try:
        get = find_one(id)
        res = get if get is not None else "No such item"
        return jsonify(res)
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "get_request_id", message)
        return jsonify(message)


@app.route('/api/devices/<id>', methods=['DELETE'])
def delete_request(id: str) -> object:
    try:
        update_one(id, {"deleted": False})
        return jsonify({"id": id})
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "delete_request", message)
        return jsonify(message)

@app.route('/api/devices/<id>', methods=['PATCH'])
def update_request(id: str) -> object:
    """
    Updates Only the Description param because the id is not all the rest are specified not to be update
    :param id:
    id param form user
    :return:
    """
    try:
        get = find_one(id)
        print("item_from_db:",get)
        if get is None:
            return jsonify({"message": "no such item"})

        if get["deleted"]:
            return jsonify({"message": "item was deleted"})

        content = request.json
        description = content.get("description", None)
        if description is None:
            return jsonify({"message": "you didn't send a description param"})
        else:
            update_one(id, {"description": description})
        return jsonify(content)
    except Exception as e:
        message = {
            "type": "exception_error",
            "message": str(e),
        }
        log(logger.ERROR, class_name, "update_request", message)
        return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')