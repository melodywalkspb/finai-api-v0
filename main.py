from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized.")
    yield


app = FastAPI(title="FinAI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/transactions/{tg_id}")
async def get_user(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_transactions_by_user(user.id)


@app.post("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    transaction_count = await rq.get_transaction_count(user.id)
    return {"transaction_count": transaction_count}