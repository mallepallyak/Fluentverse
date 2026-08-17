from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_demo import router as demo_router
from app.database import init_db


init_db()

app = FastAPI(
    title="FluentVerse API",
    description="AI-native personalized language learning from media content.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(demo_router)