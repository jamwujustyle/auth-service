from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" RENAME TO "users";
        ALTER TABLE "users" ADD "last_login" TIMESTAMPTZ;
        ALTER TABLE "users" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME TO "user";
        ALTER TABLE "users" DROP COLUMN "last_login";
        ALTER TABLE "users" DROP COLUMN "updated_at";"""
