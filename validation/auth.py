from voluptuous import Schema, Required, All, Any

from utils.exceptions import BadRequest
from utils.schema_validator import email_schema, password_schema, string_schema


def new_password_confirm_must_match(payload):
    if payload['new_password'] != payload['new_password_confirm']:
        raise BadRequest('new password confirm must match')
    return payload


def password_confirm_must_match(payload):
    if payload['password'] != payload['password_confirm']:
        raise BadRequest('password confirm must match')
    return payload


REGISTER_SCHEMA = Schema(All({
    Required('email'): email_schema,
    Required('name'): string_schema,
    Required('password'): password_schema,
    Required('password_confirm'): string_schema,
}, password_confirm_must_match))

LOGIN_SCHEMA = Schema(Any(
    {
        Required('email'): email_schema,
        Required('password'): string_schema
    },
    {
        Required('login_code'): string_schema
    }
))

CHANGE_PASSWORD_SCHEMA = Schema(All({
    Required('password'): string_schema,
    Required('new_password'): password_schema,
    Required('new_password_confirm'): string_schema
}, new_password_confirm_must_match))

FORGOT_PASSWORD_SCHEMA = Schema({
    Required('email'): email_schema
})

RESET_PASSWORD_SCHEMA = Schema(All({
    Required('password'): password_schema,
    Required('password_confirm'): string_schema,
    Required('set_password_code'): string_schema
}, password_confirm_must_match))
