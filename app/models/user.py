from tortoise.models import Model
from tortoise import fields
from uuid import uuid4


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=12)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    @property
    def hashed_password(self):
        return self.password
