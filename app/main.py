from fastapi import FastAPI
from app.routes.webhook_handler import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)
