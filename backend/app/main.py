import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging_config import setup_logging
from api import http_router, websocket_router

try:
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    print(f"INFO [main.py]: Ensured logs directory exists at: {settings.LOGS_DIR}")
except OSError as e:
    print(f"CRITICAL ERROR [main.py]: Could not create logs directory at {settings.LOGS_DIR}: {e}")
except Exception as e:
    print(f"CRITICAL ERROR [main.py]: Unexpected error creating logs directory: {e}")
    

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Starting FastAPI application...")
logger.info(f"App Name: {settings.APP_NAME}")
logger.info(f"Logs Directory: {settings.LOGS_DIR}")

app = FastAPI(
    title=settings.APP_NAME,
    description="An academic assistant system using Google ADK and FastAPI.",
    version="1.0.0"
    )

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS middleware configured for origins: {origins}")

app.include_router(
    http_router.router,
    prefix="/api/http",
    tags=["HTTP Endpoints"]
    )

app.include_router(
    websocket_router.router,
    prefix="/api/ws",
    tags=["WebSocket Endpoints"]
    )

logger.info("API routers included.")

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint providing basic application info."""
    logger.debug("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.APP_NAME}"}

logger.info("FastAPI application initialization complete. Ready to accept connections.")