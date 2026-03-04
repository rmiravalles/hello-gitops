from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

ENV_TO_INDEX = {
    "dev": BASE_DIR / "index.dev.html",
    "prod": BASE_DIR / "index.prod.html",
}

@app.get("/")
def read_root():
    app_env = os.getenv("APP_ENV", "dev").strip().lower()
    index_file = ENV_TO_INDEX.get(app_env, BASE_DIR / "index.html")
    return FileResponse(index_file)