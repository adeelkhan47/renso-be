import base64
import hashlib
import hmac
import os
from typing import Tuple


def create_hash(string: str) -> Tuple[str, str]:
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", string.encode(), salt, 100000)
    salt = base64.urlsafe_b64encode(salt).decode("utf-8")
    pw_hash = base64.urlsafe_b64encode(pw_hash).decode("utf-8")
    return salt, pw_hash


def is_correct(salt: str, pw_hash: str, string: str) -> bool:
    salt = base64.urlsafe_b64decode(salt.encode("utf-8"))
    pw_hash = base64.urlsafe_b64decode(pw_hash.encode("utf-8"))
    return hmac.compare_digest(
        pw_hash, hashlib.pbkdf2_hmac("sha256", string.encode(), salt, 100000)
    )
