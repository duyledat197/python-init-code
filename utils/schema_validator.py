import re
import uuid
from datetime import datetime
from functools import wraps

from services.storage import storage
from utils.datetime_util import get_now
from utils.exceptions import UserInputInvalid, ApplicationError, BadRequest

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
PASSWORD_PATTERN = r"(^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,}))"
URL_PATTERN = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)?"
FILENAME_PATTERN = r"(^[a-zA-Z0-9._ -]+$)"
USER_EXTENSION_PATTERN = r"[0-9]{3}"


def user_extension_validator(ext: str):
    pattern = re.compile(USER_EXTENSION_PATTERN)
    if pattern.match(ext):
        return True
    return False


def user_extension_schema(value):
    if not user_extension_validator(value):
        raise UserInputInvalid(f"{value} is wrong extension format")
    return value


def email_validator(email: str):
    pattern = re.compile(EMAIL_PATTERN)
    if pattern.match(email):
        return True
    return False


def password_validator(password: str):
    pattern = re.compile(PASSWORD_PATTERN)
    if pattern.match(password):
        return True
    return False


def url_validator(url: str):
    pattern = re.compile(URL_PATTERN)
    if pattern.match(url):
        return True
    return False


def filename_validator(filename: str):
    pattern = re.compile(FILENAME_PATTERN)
    if pattern.match(filename):
        return True
    return False


def boolean_value(value):
    if value is not None:
        value = value == 'true'
    return value


def enum_value(enum_class):
    def validate_type(value):
        enum_list = enum_class.list()
        if value not in enum_list:
            raise UserInputInvalid(f"Invalid type '{value}', must be in {enum_list}")
        return value

    return validate_type


def UUID_schema(value):
    try:
        uuid.UUID(value)
        return value
    except ValueError:
        raise UserInputInvalid(f'id {value} invalid')


def date_schema(value):
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except TypeError:
        raise UserInputInvalid(f"'{value}' must respect datetime format '{DATE_FORMAT}'")


def datetime_schema(value):
    try:
        if type(value) == datetime:
            return value
        return datetime.strptime(value, DATETIME_FORMAT)
    except TypeError:
        raise UserInputInvalid(f"'{value}' must respect datetime format '{DATETIME_FORMAT}'")


def end_date_schema(value):
    try:
        if type(value) == datetime:
            return value
        value = datetime.strptime(value, DATETIME_FORMAT)
        if value < get_now():
            raise UserInputInvalid("end_date update must uper than now")
        return value
    except TypeError:
        raise UserInputInvalid(f"'{value}' must respect datetime format '{DATETIME_FORMAT}'")


def edit_date_schema(value):
    try:
        if type(value) == datetime:
            return value
        value = datetime.strptime(value, DATETIME_FORMAT)
        if value < get_now():
            raise UserInputInvalid("Date update must uper than now")
        return value
    except TypeError:
        raise UserInputInvalid(f"'{value}' must respect datetime format '{DATETIME_FORMAT}'")


def email_schema(value):
    if not email_validator(value):
        raise UserInputInvalid(f"{value} is wrong email format")
    return value


def number_schema(value):
    try:
        int(value)
        return value
    except Exception:
        raise UserInputInvalid(f'{value} must be a number')


def password_schema(value):
    if not password_validator(value):
        raise UserInputInvalid(f"password is wrong format")
    return value


def url_schema(value):
    if not url_validator(value):
        raise UserInputInvalid(f"url is wrong format")
    return value


def filename_schema(value):
    if not filename_validator(value):
        raise UserInputInvalid(f"filename is wrong format")
    return value


def string_schema(value):
    if not isinstance(value, str):
        raise UserInputInvalid(f'value must be a string')
    if not bool(value.strip()):
        raise UserInputInvalid(f"string not empty")
    return value


def dict_schema(value):
    if not isinstance(value, dict):
        raise UserInputInvalid(f'value must be a string')
    return value


def filename_exist(filename):
    if not storage.check_if_object_exists(filename):
        raise BadRequest('filename not exist')
    return filename


def validated(schema_validator):
    """
    Using to validate schema of request.data. Raise Voluptuous.Invalid if failed.
    """

    def internal(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            from flask import request
            if not request.is_json:
                raise ApplicationError("Bad Request", detail="Expect json type body")
            data = schema_validator(request.get_json())
            request.data = data
            return func(*args, **kwargs)

        return decorated

    return internal
