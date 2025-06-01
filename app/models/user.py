from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=12)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)
    is_verified = fields.BooleanField(default=False)

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)
