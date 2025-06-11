from tortoise.models import Model
from tortoise import fields
from uuid import uuid4
import os
import hmac
import hashlib
from datetime import datetime, timedelta, timezone
import argon2
from argon2 import PasswordHasher
from ..configs.logging_config import logger

ph = PasswordHasher()


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=12)
    email = fields.CharField(max_length=255, unique=False)
    password = fields.CharField(max_length=128)

    is_verified = fields.BooleanField(default=False)
    verification_token = fields.CharField(max_length=255, null=True)
    verification_token_expires = fields.DatetimeField(null=True)
    last_login = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def set_password(self, password: str):
        self.password = ph.hash(password)

    def check_password(self, password: str) -> bool:

        try:
            ph.verify(self.password, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    def generate_verification_token(self):
        """Generate a secure verification token"""

        token = str(uuid4())

        secret = os.environ.get("EMAIL_VERIFICATION_SECRET", None)
        if not secret:
            logger.error("EMAIL_VERIFICATION_SECRET not found during token generation")
            raise ValueError("invalid email secret")
        signature = hmac.new(
            secret.encode(), f"{self.id}:{token}".encode(), hashlib.sha256
        ).hexdigest()

        self.verification_token = f"{token}:{signature}"

        self.verification_token_expires = datetime.now(timezone.utc) + timedelta(
            hours=24
        )

    def verify_token(self, token: str) -> bool:
        """Verify the email verification token"""
        if not self.verification_token or not self.verification_token_expires:
            logger.critical("missing verification token or expiry")
            return False
        if datetime.now(timezone.utc) > self.verification_token_expires:
            logger.critical(f"verification token expired")
            return False

        try:
            stored_token, stored_signature = self.verification_token.split(":")
            provided_token, provided_signature = token.split(":")

            if stored_token != provided_token:
                logger.critical(f"token mismatch")
                return False

            secret = os.environ.get("EMAIL_VERIFICATION_SECRET", None)
            if not secret:
                logger.critical(
                    "EMAIL_VERIFICATION_SECRET not set during token verification"
                )
                return False
            expected_signature = hmac.new(
                secret.encode(), f"{self.id}:{provided_token}".encode(), hashlib.sha256
            ).hexdigest()
            if expected_signature == stored_signature:
                logger.critical("signatures match")

            is_valid = hmac.compare_digest(expected_signature, provided_signature)
            return is_valid
        except ValueError:
            return False

    class Meta:
        table = "users"
