from datetime import datetime, timezone
from typing import Callable

from bson import ObjectId
from pydantic import BaseConfig, BaseModel


def datetime_2_isoformat(date_time: datetime) -> str:
    return date_time.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def snake_2_camel(var: str) -> str:
    return "".join(word if idx == 0 else word.capitalize() for idx, word in enumerate(var.split(sep="_")))


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        validate_assignment: bool = True
        arbitrary_types_allowed: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime: datetime_2_isoformat, ObjectId: str}
        alias_generator: Callable = snake_2_camel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(oid=value):
            raise ValueError("Invalid Object ID!")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(type="string")
