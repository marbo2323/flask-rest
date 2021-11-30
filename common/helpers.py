import json

from flask import make_response


def error_response(error_code: int, error_message: str):
    return make_response({"error":error_message},error_code)
