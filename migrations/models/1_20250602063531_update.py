from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "verification_token_expires" TIMESTAMPTZ;
        ALTER TABLE "user" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" ADD "verification_token" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "verification_token_expires";
        ALTER TABLE "user" DROP COLUMN "created_at";
        ALTER TABLE "user" DROP COLUMN "verification_token";"""
