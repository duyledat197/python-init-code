from voluptuous import Optional, Schema, Required

from services.user import find_user_by_email
from utils.exceptions import BadRequest
from utils.schema_validator import string_schema, password_schema, email_schema


def check_is_new_email(email):
    user = find_user_by_email(email)
    if bool(user):
        raise BadRequest('email already exists')
    return


UPDATE_USER_PROFILE = Schema({
    Optional('name'): string_schema
})

CREATE_USER_SCHEMA = Schema({
    Required('email'): email_schema,
    Required('name'): string_schema,
    Required('password'): password_schema
})
