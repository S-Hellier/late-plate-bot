# main.py
from fastapi import FastAPI
from scheduler import startScheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running bot")
    startScheduler()
    yield
    print("Bot shutting down")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "Bot is running"}
