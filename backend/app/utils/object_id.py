from typing import Any

from bson import ObjectId


def validate_object_id(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value

    if isinstance(value, str) and ObjectId.is_valid(value):
        return ObjectId(value)

    raise ValueError("Invalid MongoDB ObjectId")


def object_id_to_str(value: ObjectId) -> str:
    return str(value)
