import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analyze

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))

app = FastAPI(
    title="Parse Mind",
    description="LLM Text analysis",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)


@app.get("/health")
async def health_check():
    return {"status": "Disparse and move, blud!"}
