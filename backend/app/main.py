from fastapi import FastAPI

from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.analyze import router as analyze_router


app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Code Intelligence API is running"}


app.include_router(health_router, prefix="/api/v1")
app.include_router(analyze_router, prefix="/api/v1")