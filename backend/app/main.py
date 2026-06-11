from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import groups, health, matches, predictions
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="WorldCupIQ API",
    version="0.1.0",
    description="MVP API for World Cup 2026 fixtures.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(groups.router)
app.include_router(matches.router)
app.include_router(predictions.router)
