from datetime import datetime
from functools import reduce

from sqlalchemy import func, distinct, or_, and_

from model import User
from utils.exceptions import BadRequest
from config import UserStatus


def create_user(data):
    user = User(
        role=data['role'],
        email=data['email'].lower(),
        name=data['name'],
        extension=data.get('extension', None)
    )
    return user


def find_user_by_email(email):
    user = User.query.find_by_filter(model=User, filter={'email': email.lower()})
    return user


def get_blocked_user_or_404(user_id):
    user = User.query.filter(User.id == str(user_id), User.status == UserStatus.BLOCKED.value).first()
    if not bool(user):
        raise BadRequest('User not found or is active')
    return user


def get_user_profile_or_404(user_id):
    user = User.query.filter(User.id == str(user_id), User.status != UserStatus.BLOCKED.value).first()
    if not bool(user):
        raise BadRequest('User not found or is blocked')
    return user
