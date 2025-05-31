from fastapi import FastAPI, Path
from api.routes import auth_router

app = FastAPI()


@app.get("/")
def home():
    return "<h1>HELLO WORLD</h1>"


app.include_router(auth_router, prefix="/auth")
