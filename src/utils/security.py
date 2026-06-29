from jwt import ExpiredSignatureError, InvalidTokenError, InvalidSignatureError, encode, decode
from src.core.config import Settings
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from datetime import datetime, timedelta, timezone

settings = Settings()

argon = PasswordHasher()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
TOKEN_EXPIRE = settings.TOKEN_EXPIRE

def hash_password (password: str):
    return argon.hash(password)

def verify_password (hashed_password: str, password: str):
    try:
        return argon.verify(hashed_password, password)
    except VerificationError:
        return False
    
def create_token_jwt (user_id: int, name: str, email: str, token_duration = timedelta(seconds = TOKEN_EXPIRE)):
    expire = datetime.now(timezone.utc) + token_duration

    payload = {
        "sub": str(user_id),
        "nome": name,
        "email": email,
        "exp": expire,
        "type": "access"
    }

    encoded_jwt = encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_token_jwt (token_jwt: str, expected_type: str | None = None):

    try:
        payload = decode(token_jwt, SECRET_KEY, algorithms = [ALGORITHM])

        if expected_type and payload.get("type") != expected_type:
            return None

        return payload

    except InvalidTokenError:
        return None
    except ExpiredSignatureError:
        return None
    except InvalidSignatureError:
        return None
    except Exception:
        return None