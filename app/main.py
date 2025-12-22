from fastapi import FastAPI

from app.core.logging import logger
from app.ingestion.router import router as ingestion_router

app = FastAPI(title="Async Event Service")

app.include_router(ingestion_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
