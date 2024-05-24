from datetime import datetime
import secrets
import hashlib
import base64
import enum
from .algorithms import serialize_to_json
import config
from main_app.exceptions import InvalidTokenError


class TypeToken(enum.StrEnum):
    REFRESH = 'refresh'
    ACCESS = 'access'


def calculate_password_hash(row_password: str, salt: str = None):
    if salt is None:
        salt = secrets.token_bytes(16)
    else:
        salt = bytes.fromhex(salt)
    password_hash = hashlib.scrypt(row_password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    return password_hash.hex(), salt.hex()


def compare_digest(hash_a, hash_b):
    return secrets.compare_digest(hash_a, hash_b)


def verify_passwords(password_hash: str, salt: str, row_password: str):
    new_hash, _ = calculate_password_hash(row_password, salt)
    return compare_digest(password_hash, new_hash)


def create_confirm_code():
    code = [str(secrets.randbelow(10)) for _ in range(config.LENGTH_CONFIRM_CODE)]
    return ''.join(code)


def create_token(binary_date):
    data = base64.urlsafe_b64encode(binary_date)
    sign = hashlib.blake2b(key=config.SECRET_KEY)
    sign.update(data)
    return '.'.join((data.hex(), sign.hexdigest()))


def verify_token(binary_data, tfa_sign):
    new_tfa_token = create_token(binary_data)
    _, new_tfa_sign = new_tfa_token.split('.')
    return compare_digest(tfa_sign, new_tfa_sign)


def create_jwt_tokens(token_id: str, expiration_datetime: datetime):
    payload = {"alg": "BLAKE_2B", "uuid": token_id}
    refresh_salt = secrets.token_hex(16)
    binary_refresh_data = serialize_to_json(payload | {"type": TypeToken.REFRESH, "salt": refresh_salt})

    access_salt = secrets.token_hex(16)
    binary_access_data = serialize_to_json(payload | {"type": TypeToken.ACCESS, "salt": access_salt,
                                                      "expiration_datetime": expiration_datetime.isoformat()})

    access_token = create_token(binary_access_data)
    refresh_token = create_token(binary_refresh_data)

    return access_token, refresh_token


def verify_jwt_token(binary_data, jwt_sign):
    return verify_token(binary_data, jwt_sign)


def parse_token(token: str):
    try:
        if isinstance(token, str):
            auth = token.split('.')
            if len(auth) == 2:
                data, sign = auth
                binary_data = base64.urlsafe_b64decode(bytes.fromhex(data))
                return binary_data, sign

        raise InvalidTokenError()

    except Exception as ex:
        raise InvalidTokenError(ex)


def parse_jwt_token(jwt_token):
    binary_data, sign = parse_token(jwt_token)

    if not verify_jwt_token(binary_data, sign):
        raise InvalidTokenError()

    return binary_data, sign
