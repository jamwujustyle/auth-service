from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .api.routes import auth, internal
from .configs.database import DB_URL
from contextlib import asynccontextmanager
from .kafka_producer import kafka_producer
from .configs.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.start()
    yield
    await kafka_producer.stop()


app = FastAPI(title="Auth service", lifespan=lifespan)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(internal.router, tags=["internal"])


@app.get("/health")
def health_check():
    logger.critical("bitch ass nigga")
    return {"status": "healthy"}


register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
