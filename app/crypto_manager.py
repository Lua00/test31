import base64
import os
from dataclasses import dataclass
from typing import Tuple

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken


DEFAULT_ITERATIONS = 200_000
DEFAULT_SALT_BYTES = 16
TEXT_PREFIX = "ENCV1"  # marker for text payloads
FILE_PREFIX = b"ENCV1\x00"  # marker for file payloads (binary)


@dataclass
class DerivedKey:
    key: bytes
    salt: bytes


def generate_salt(length: int = DEFAULT_SALT_BYTES) -> bytes:
    if length < 16:
        # enforce minimum salt length for safety
        length = 16
    return os.urandom(length)


def derive_key(password: str, salt: bytes, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    if not isinstance(password, str) or password == "":
        raise ValueError("Parola boş olamaz")
    if not isinstance(salt, (bytes, bytearray)) or len(salt) < 16:
        raise ValueError("Salt en az 16 bayt olmalı")
    if iterations < 50_000:
        # basic floor for PBKDF2 iterations
        iterations = 50_000

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    raw_key = kdf.derive(password.encode("utf-8"))
    # Fernet expects a 32-byte key urlsafe-base64 encoded
    return base64.urlsafe_b64encode(raw_key)


def build_fernet(password: str, salt: bytes, iterations: int) -> Fernet:
    key = derive_key(password=password, salt=salt, iterations=iterations)
    return Fernet(key)


# ---- Text helpers (salt embedded) ----

def encrypt_text(plaintext: str, password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    salt = generate_salt()
    fernet = build_fernet(password=password, salt=salt, iterations=iterations)
    token = fernet.encrypt(plaintext.encode("utf-8"))
    # embed as: ENCV1$<salt_b64>$<token_b64>
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii")
    token_b64 = token.decode("ascii")
    return f"{TEXT_PREFIX}${salt_b64}${token_b64}"


def decrypt_text(payload: str, password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    try:
        if not payload.startswith(TEXT_PREFIX + "$"):
            raise ValueError("Geçersiz metin şeması")
        _, salt_b64, token_b64 = payload.split("$", 2)
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        token = token_b64.encode("ascii")
        fernet = build_fernet(password=password, salt=salt, iterations=iterations)
        plaintext_bytes = fernet.decrypt(token)
        return plaintext_bytes.decode("utf-8")
    except (InvalidToken, ValueError, base64.binascii.Error) as exc:
        raise ValueError("Çözme başarısız. Parola yanlış veya veri bozuk.") from exc


# ---- File helpers (binary, header: FILE_PREFIX + salt(16) + token) ----

def encrypt_bytes(data: bytes, password: str, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    salt = generate_salt()
    fernet = build_fernet(password=password, salt=salt, iterations=iterations)
    token = fernet.encrypt(data)
    return FILE_PREFIX + salt + token


def decrypt_bytes(blob: bytes, password: str, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    try:
        if not blob.startswith(FILE_PREFIX):
            raise ValueError("Geçersiz dosya şeması")
        salt = blob[len(FILE_PREFIX):len(FILE_PREFIX) + DEFAULT_SALT_BYTES]
        token = blob[len(FILE_PREFIX) + DEFAULT_SALT_BYTES:]
        fernet = build_fernet(password=password, salt=salt, iterations=iterations)
        return fernet.decrypt(token)
    except (InvalidToken, ValueError) as exc:
        raise ValueError("Çözme başarısız. Parola yanlış veya dosya bozuk.") from exc