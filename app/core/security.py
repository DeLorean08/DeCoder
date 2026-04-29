import bcrypt
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf=8")

    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def encode_jwt(
    payload: dict,
    key: str =  settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
    expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(ex=expire.timestamp(), 
                     iat=now.timestamp())
    encoded = jwt.encode(to_encode, key, algorithm)
    return encoded

def decode_jwt(
        token: str,
        key: str =  settings.SECRET_KEY,
        algorithms: str = settings.ALGORITHM,
):
    decode = jwt.decode(token, key, algorithms=[algorithms])
    return decode