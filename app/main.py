from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.ingestion.router import router as ingestion_router
from app.core.exceptions import AppException
from app.core.logging import logger
from app.utils.ids import generate_event_id

app = FastAPI(title="Async Event Service")

app.include_router(ingestion_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(generate_event_id()))
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(
        "Application error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "status_code": exc.status_code,
            "error": exc.message,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception",
        extra={"request_id": getattr(request.state, "request_id", None)},
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": getattr(request.state, "request_id", None),
        },
    )
