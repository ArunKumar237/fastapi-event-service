from fastapi import FastAPI

from app.core.logging import logger

app = FastAPI(title="Async Event Service")


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
