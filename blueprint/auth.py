import uuid
from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import (jwt_required,
                                jwt_refresh_token_required,
                                get_raw_jwt, get_jwt_identity,
                                create_access_token,
                                create_refresh_token)

from config import FRONTEND_ENDPOINT, UserStatus
from model import User, RevokedToken
from model.db import db
from services.user import find_user_by_email
from tasks.mail import send_mail_reset_password
from utils.exceptions import BadRequest
from utils.responser import generate_success_response
from utils.schema_validator import validated
from validation.auth import LOGIN_SCHEMA, CHANGE_PASSWORD_SCHEMA, FORGOT_PASSWORD_SCHEMA, \
    RESET_PASSWORD_SCHEMA

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
@validated(LOGIN_SCHEMA)
@swag_from('../apidocs/auth/login.yml')
def login():
    body = request.data
    account = body.copy()
    user = User.query.filter(
        User.email == account['email'].lower(),
        User.status != UserStatus.BLOCKED.value
    ).first()
    if not user:
        raise BadRequest('Login failed. Please enter a valid login name and password.')
    if not user.check_password(account['password']):
        raise BadRequest('Login failed. Please enter a valid login name and password.')
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'role': user.role
    }
    return generate_success_response(data)


@auth.route('/logout-access', methods=['POST'])
@jwt_required
@swag_from('../apidocs/auth/logout_access.yml')
def logout_access():
    jti = get_raw_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return generate_success_response()


@auth.route('/logout-refresh', methods=['POST'])
@jwt_refresh_token_required
@swag_from('../apidocs/auth/logout_refresh.yml')
def logout_refresh():
    jti = get_raw_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return generate_success_response()


@auth.route('/token-refresh', methods=['POST'])
@jwt_refresh_token_required
@swag_from('../apidocs/auth/token_refresh.yml')
def token_refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    data = {'access_token': access_token}
    return generate_success_response(data)


@auth.route('/change-password', methods=['POST'])
@jwt_required
@validated(CHANGE_PASSWORD_SCHEMA)
@swag_from('../apidocs/auth/change_password.yml')
def change_password():
    user_id = get_jwt_identity()
    body = request.data
    user = User.query.get_or_404(user_id)
    if not user.check_password(body['password']):
        raise BadRequest('Password is incorrect')
    user.set_password(body['new_password'])
    db.session.commit()
    return generate_success_response()


@auth.route('/forgot-password', methods=['POST'])
@validated(FORGOT_PASSWORD_SCHEMA)
@swag_from('../apidocs/auth/forgot_password.yml')
def forgot_password():
    body = request.data
    user = find_user_by_email(body['email'])
    if not user:
        raise BadRequest('email is not found')
    user.request_forgot_password_at = datetime.utcnow()
    user.set_password_code = str(uuid.uuid4())
    db.session.commit()
    reset_link = f'{FRONTEND_ENDPOINT}/reset-password?token={user.set_password_code}'
    send_mail_reset_password(user, reset_link)
    return generate_success_response()


@auth.route('/reset-password', methods=['POST'])
@validated(RESET_PASSWORD_SCHEMA)
@swag_from('../apidocs/auth/reset_password.yml')
def reset_password():
    body = request.data
    user = db.session.query(User).filter_by(set_password_code=body['set_password_code']).first()
    if not bool(user):
        raise BadRequest('set password code is not found')
    user.request_forgot_password_at = None
    user.set_password_code = None
    user.set_password(body['password'])
    db.session.commit()
    return generate_success_response()
