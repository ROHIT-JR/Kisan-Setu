from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, diagnose, advisory, districts, trace

app = FastAPI(title="Kisan Setu API", version=settings.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(diagnose.router)
app.include_router(advisory.router)
app.include_router(districts.router)
app.include_router(trace.router)
