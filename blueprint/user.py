from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import UserRole, UserStatus
from model import User
from model.db import db
from services.user import get_user_profile_or_404, create_user

from utils.exceptions import BadRequest
from utils.permission import authorized
from utils.requester import get_pagination_params, get_sort
from utils.responser import generate_success_response
from utils.schema_validator import validated, UUID_schema
from validation.user import UPDATE_USER_PROFILE, CREATE_USER_SCHEMA, check_is_new_email

user_route = Blueprint('user', __name__, url_prefix='/users')

MAP_SORT = {
    'name': User.name
}


@user_route.route('', methods=['POST'])
@jwt_required
@validated(CREATE_USER_SCHEMA)
@swag_from('../apidocs/user/create.yml')
def create():
    body = request.data
    check_is_new_email(body['email'])
    data_user = body.copy()
    user_created = create_user(data=data_user)
    user_created.set_password(body['password'])
    user_created.save(session=db.session)
    return generate_success_response(user_created.to_json())


@user_route.route('', methods=['GET'])
@jwt_required
@swag_from('../apidocs/user/get_list.yml')
def get_list():
    offset, limit = get_pagination_params(request)
    sort_by, sort_type = get_sort(request=request,
                                  map_sort=MAP_SORT,
                                  default_sort_by='user_created_at')
    role = request.args.get('role', None)
    query = User.query
    if role is not None:
        query = query.filter(User.role == role)
    status = request.args.get('status', None)
    if status is not None:
        query = query.filter(User.status == status)

    count = query.count()
    users = query.order_by(sort_type(sort_by)).offset(offset).limit(limit).all()
    data = [u.to_json() for u in users]
    return generate_success_response(data=data, offset=offset, limit=limit, total=count)


@user_route.route('/<user_id>', methods=['GET'])
@jwt_required
@swag_from('../apidocs/user/get_profile.yml')
def get_profile(user_id):
    user_id = UUID_schema(user_id)
    user = get_user_profile_or_404(user_id)
    data = user.to_json()
    return generate_success_response(data)


@user_route.route('/<uuid:user_id>', methods=['PUT'])
@jwt_required
@validated(UPDATE_USER_PROFILE)
@swag_from('../apidocs/user/update_user.yml')
def update_user_profile(user_id):
    user = get_user_profile_or_404(user_id)
    body = request.data
    user_info_update = body.copy()
    if 'email' in user_info_update:
        check_is_new_email(body['email'])
    if 'password' in user_info_update:
        user.set_password(user_info_update['password'])

    user.update(data_update=user_info_update, session=db.session)
    user_data = user.to_json()
    user_data['new_password'] = body['password']
    return generate_success_response(user_data)


@user_route.route('/me', methods=['GET'])
@jwt_required
@swag_from('../apidocs/user/get_me.yml')
def get_me():
    user_id = get_jwt_identity()
    user = get_user_profile_or_404(user_id)
    data = user.to_json()
    return generate_success_response(data)


@user_route.route('/me', methods=['PUT'])
@jwt_required
@validated(UPDATE_USER_PROFILE)
@swag_from('../apidocs/user/get_me.yml')
def update_me():
    user_id = get_jwt_identity()
    user = get_user_profile_or_404(user_id)
    body = request.data
    user_info_update = body.copy()
    user.update(data_update=user_info_update, session=db.session)
    return generate_success_response(user.to_json())


@user_route.route('/<uuid:user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    user = get_user_profile_or_404(user_id)
    user.status = UserStatus.BLOCKED.value
    db.session.commit()
    return generate_success_response()
