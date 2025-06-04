from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_user_email_1b4f1c";
        ALTER TABLE "user" DROP CONSTRAINT IF EXISTS "user_email_key";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_user_email_1b4f1c" ON "user" ("email");
        ALTER TABLE "user" ADD CONSTRAINT "user_email_key" UNIQUE ("email");"""
