import jwt

from config import SECRET_KEY

ALGORITHM = 'HS256'


def get_encode(json):
    code = jwt.encode(json, SECRET_KEY, algorithm=ALGORITHM).decode()
    return code


def get_decode(code):
    json = jwt.decode(code, SECRET_KEY, algorithms=[ALGORITHM])
    return json
