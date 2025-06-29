# main.py
from fastapi import FastAPI
from scheduler import startScheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    startScheduler()

@app.get("/")
async def root():
    return {"status": "Bot is running"}
