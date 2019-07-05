import hashlib
import hmac
import uuid


def string_to_binary(string):
    binary_array = bytearray()
    binary_array.extend(map(ord, string))
    return binary_array


def hash_hmac_sha256(secret, message):
    m = hmac.new(
        string_to_binary(secret),
        message.encode(),
        hashlib.sha256
    )
    return m.hexdigest()


def hash_sha256(message):
    return hashlib.sha256(message.encode()).hexdigest()


def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt
    return hashed_password


def check_password(hashed_password, password):
    if (not hashed_password) or (not password):
        return False
    user_password, salt = hashed_password.split(':')
    return user_password == hashlib.sha512(salt.encode() + password.encode()).hexdigest()
