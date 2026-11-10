from datetime import datetime, timezone, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from config import settings

pw = PasswordHasher()
SECRET_KEY = settings.SECRET_KEY
ALGHORITHM = "HS256"

def hash_password(password: str):
    return pw.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pw.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(user_id: int) -> str:
    token_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": str(user_id), "exp": token_time}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGHORITHM)
   