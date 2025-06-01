from fastapi import FastAPI, Path

from .api.routes.auth import router

app = FastAPI()


@app.get("/")
def home():
    return "<h1>HELLO WORLD</h1>"


app.include_router(router, prefix="/auth")
