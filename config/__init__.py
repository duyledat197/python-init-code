import os
from datetime import timedelta

from dotenv import load_dotenv, find_dotenv

from utils.enum_type import ApacEnum

load_dotenv(find_dotenv(), override=True)


class UserRole(ApacEnum):
    ADMIN = 'admin'
    USER = 'user'


class UserStatus(ApacEnum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN', 'admin@gmail.com')
DEFAULT_PASSWORD_ADMIN = os.environ.get('PASSWORD_ADMIN', 'Admin@123')

OTP_EXPIRY_TIME = 300  # 5 minutes
FORGOT_PASSWORD_CODE_EXPIRY_TIME = 600  # 10 minutes
FRONTEND_ENDPOINT = os.environ.get('FRONTEND_ENDPOINT', 'http://localhost:3000')
SECRET_KEY = os.environ.get('SECRET_KEY', 'test')

MAX_CONTENT_LENGTH = 5  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif', 'svg', 'pdf', 'docx', 'xls', 'xlsx', 'xlsm', 'doc'}
UPLOAD_FOLDER = 'uploads'

JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

SWAGGER_CONFIG = {
    "swagger": "2.0",
    "info": {
        "title": "API",
        "description": "API",
        "contact": {},
        "termsOfService": "http://rockship.co/#",
        "version": "0.1.0",
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

S3_REGION = os.environ.get('S3_REGION')
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
STORAGE_FOLDER = os.environ.get('STORAGE_FOLDER')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

ONE_DATE = 24 * 60 * 60
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
