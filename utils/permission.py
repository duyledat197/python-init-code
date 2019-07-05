from functools import wraps

from config import UserStatus

from flask import request
from flask_jwt_extended import get_jwt_identity

from model import User
from utils.exceptions import PermissionDenied


def authorized(roles: list = []):
    def real_jwt_required(fn):
        @wraps(fn)
        def internal(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.filter(User.id == user_id, User.status != UserStatus.BLOCKED.value).first()
            if user.role not in roles:
                raise PermissionDenied(f'Role {user.role} is not allowed to perform this action')
            request.user = user
            return fn(*args, **kwargs)

        return internal

    return real_jwt_required
