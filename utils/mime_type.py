import enum

MIME_TYPE = {'image/jpg', 'image/jpeg', 'image/png'}


class MimeSupport(enum.Enum):
    jpg = 'image/jpg'
    jpeg = 'image/jpeg'
    png = 'image/png'


def is_image_type(mime):
    if mime in MIME_TYPE:
        return True
    return False
