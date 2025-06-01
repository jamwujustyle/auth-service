from fastapi import FastAPI, Path
from tortoise.contrib.fastapi import register_tortoise
from .api.routes.auth import router
from .configs.database import DB_URL

app = FastAPI()


@app.get("/")
def home():
    return "<h1>HELLO WORLD</h1>"


app.include_router(router, prefix="/auth")


register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
