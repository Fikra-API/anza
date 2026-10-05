import hashlib
import os
import secrets
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or SECRET_KEY == "default-insecure-secret-key":
    raise RuntimeError("SECRET_KEY is not set. Add it to .env — generate one with: python -c 'import secrets; print(secrets.token_hex(32))'")
COOKIE_NAME = "anza_session"


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000,
    ).hex()
    return pw_hash, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    pw_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(pw_hash, password_hash)


def create_session_token(user_id: int) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps({"user_id": user_id})


def read_session_token(token: str, max_age: int = 86400 * 14) -> int | None:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        data = serializer.loads(token, max_age=max_age)
        return data.get("user_id")
    except (BadSignature, SignatureExpired):
        return None
