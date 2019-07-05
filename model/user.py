import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from model.db import db
from utils.hash_util import hash_password, check_password
from config import UserStatus


class User(db.Model):
    __tablename__ = 'user'
    __json_hidden__ = [
        'password_hash',
        'set_password_code',
        'request_forgot_password_at'
    ]
    __update_field__ = [
        'email',
        'name',
        'role'
    ]
    # Columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False, default=UserStatus.ACTIVE.value)
    name = Column(String, nullable=False)

    request_forgot_password_at = Column(DateTime)
    set_password_code = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        super(User, self).__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)
