from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.orm import create_db_and_tables
from app.routes.webhook_handler import router as webhook_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(webhook_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
