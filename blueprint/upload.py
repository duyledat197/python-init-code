from flasgger import swag_from
from flask import Blueprint, request, Response

from services.storage import storage
from utils.exceptions import BadRequest, ApplicationError
from utils.file_upload import allowed_file, get_filename
from utils.responser import generate_success_response

upload_route = Blueprint('upload', __name__, url_prefix='/uploads')


@upload_route.route('', methods=['POST'])
@swag_from('../apidocs/upload/upload_file.yml')
def upload_file_to_s3():
    file = request.files['file'] if 'file' in request.files else None
    if file is None:
        raise BadRequest('Form data invalid')
    if file.filename == '':
        raise BadRequest('Logo no selected file')
    if not allowed_file(file.filename):
        raise BadRequest('Extension is not allow')
    filename = get_filename(file.filename)
    try:
        storage.upload_file_obj(file, filename, file.mimetype)
    except Exception as e:
        raise ApplicationError(e)
    return generate_success_response(data={'filename': filename})


@upload_route.route('/<filename>', methods=['GET'])
@swag_from('../apidocs/upload/get_file.yml')
def get_file_from_s3(filename):
    if not storage.check_if_object_exists(filename):
        raise BadRequest('File not found')
    try:
        file = storage.get_object(filename).get()
    except Exception as e:
        raise ApplicationError(str(e))
    return Response(file['Body'].read(), mimetype=file['ContentType'])


@upload_route.route('/<filename>', methods=['PUT'])
def update(filename):
    if not storage.check_if_object_exists(filename):
        raise BadRequest('File not found')
    file = request.files['file'] if 'file' in request.files else None
    if file is None:
        raise BadRequest('Form data invalid')
    try:
        s3_object = storage.get_object(filename)
        s3_object.upload_fileobj(Fileobj=file, ExtraArgs={'ContentType': file.mimetype})
    except Exception as e:
        raise ApplicationError(str(e))
    return Response(file['Body'].read(), mimetype=file['ContentType'])
