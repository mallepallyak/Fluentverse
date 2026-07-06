from fastapi import FastAPI
from app.api.routes_demo import router as demo_router


app = FastAPI(
    title="FluentVerse API",
    description="AI-native personalized language learning from media content.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(demo_router)