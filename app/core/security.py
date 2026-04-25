import bcrypt
import jwt

from app.core.config import settings

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf=8")

    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def encode_jwt(
    payload: dict,
    key: str =  settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM
):
    encoded = jwt.encode(payload, key, algorithm=algorithm)
    return encoded

def decode_jwt(
        token: str,
        key: str =  settings.SECRET_KEY,
        algorithms: str = settings.ALGORITHM,
):
    decode = jwt.decode(token, key, algorithms=[algorithms])
    return decode