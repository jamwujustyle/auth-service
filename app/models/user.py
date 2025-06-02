from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt
from uuid import uuid4
import os
import hmac
import hashlib
from datetime import datetime, timedelta


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=12)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)
    is_verified = fields.BooleanField(default=False)
    verification_token = fields.CharField(max_length=255, null=True)
    verification_token_expires = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def generate_verification_token(self):
        """Generate a secure verification token"""

        token = str(uuid4())

        secret = os.environ.get("EMAIL_VERIFICATION_SECRET", None)

        signature = hmac.new(
            secret.encode(), f"{self.id}:{token}".encode(), hashlib.sha256
        ).hexdigest()

        self.verification_token = f"{token}:{signature}"
        self.verification_token_expires = datetime.utcnow() + timedelta(hours=24)

    def verify_token(self, token: str) -> bool:
        """Verify the email verification token"""
        if not self.verification_token or not self.verification_token_expires:
            return False
        if datetime.utcnow() > self.verification_token_expires:
            return False

        try:
            stored_token, stored_signature = self.verification_token.split(":")
            provided_token, provided_signature = token.split(":")

            if stored_token != provided_token:
                return False

            secret = os.environ.get("EMAIL_VERIFICATION_SECRET", None)
            expected_signature = hmac.new(
                secret.encode(), f"{self.id}:{provided_token}".encode(), hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_signature, provided_signature)
        except ValueError:
            return False
