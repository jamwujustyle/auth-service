from tortoise.models import Model
from tortoise import fields
from uuid import uuid4
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey
import os


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=12)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    def set_password(self, password: str):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend,
        )
        hashed_password = kdf.derive(password.encode())
        self.password = salt + hashed_password

    def check_password(self, password: str) -> bool:
        salt = self.password[:16]
        stored_hash = self.password[16:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        try:
            kdf.verify(password.encode(), stored_hash)
            return True
        except InvalidKey:
            return False
