import os
from datetime import datetime
from io import BytesIO

from docxtpl import DocxTemplate

from config import ALLOWED_EXTENSIONS
from services.storage import storage
from utils.exceptions import ApplicationError

DOCX_MINE_TYPE = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_folder_upload(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_filename(filename, prefix='upload'):
    extension = os.path.splitext(filename)[1]
    timestamp = datetime.utcnow().timestamp()
    return f'{prefix}-{timestamp}{extension}'


def create_file_docx_from_template(template_path, data):
    file_name = get_filename(template_path, prefix='doc')
    document = DocxTemplate(template_path)
    document.render(data)
    file = document.get_docx()
    stream = BytesIO()
    file.save(stream)
    stream.seek(0)
    try:
        storage.upload_file_obj(stream, file_name, DOCX_MINE_TYPE)
        stream.close()
    except Exception as e:
        raise ApplicationError(str(e))
    return file_name
