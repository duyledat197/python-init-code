import os

import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from flask import current_app

from config import STORAGE_FOLDER, S3_BUCKET_NAME
from utils.exceptions import ApplicationError, BadRequest


class Storage:
    client = None
    resource = None

    def __init__(self, client, resource):
        self.client = client
        self.resource = resource

    def get_bucket(self):
        return self.resource.Bucket(S3_BUCKET_NAME)

    def generate_url_upload(self, key, mime_type):
        if not isinstance(key, str):
            raise ApplicationError('Key must be a string')
        if not isinstance(mime_type, str):
            raise ApplicationError('Mime type must be a string')
        return self.client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': key,
                'ContentType': mime_type,
                'ACL': 'private'
            },
            ExpiresIn=600
        )

    def generate_url_read(self, key):
        if not isinstance(key, str):
            raise ApplicationError('Key must be a string')
        return self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': key,
            },
        )

    def get_object(self, key):
        if not isinstance(key, str):
            raise ApplicationError('Key must be a string')
        key = self.custom_key(key)
        return self.resource.Object(S3_BUCKET_NAME, key)

    def check_if_object_exists(self, key: str):
        key = self.custom_key(key)
        response = self.client.list_objects(
            Bucket=S3_BUCKET_NAME,
            Prefix=key
        )
        return 'Contents' in response

    def validate_filename_exist(self, filename):
        if not self.check_if_object_exists(filename):
            raise BadRequest('filename not exist')
        return filename

    def delete_object(self, key: str):
        self.get_object(key).delete()
        return

    def get_size_object(self, key):
        try:
            return self.get_object(key).content_length
        except ClientError as e:
            current_app.logger.debug(e)
            return None

    def upload_file_obj(self, data, key, content_type='image/jpg'):
        if key[0] == '/':
            key = key[1:]
        try:
            key = self.custom_key(key)
            return self.client.upload_fileobj(
                data, S3_BUCKET_NAME, key,
                ExtraArgs={
                    'ContentType': content_type
                }
            )
        except S3UploadFailedError as e:
            current_app.logger.debug(e)
            raise ApplicationError('Can not upload to server')

    @staticmethod
    def custom_key(key: str) -> str:
        return f'{STORAGE_FOLDER}/{key}'


def make_storage(client=None, resource=None):
    if client is None:
        client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
            region_name=os.getenv('S3_REGION')
        )
    if resource is None:
        resource = boto3.resource(
            's3',
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
            region_name=os.getenv('S3_REGION')
        )
    return Storage(client, resource)


storage = make_storage()
