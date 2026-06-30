import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.kafka.consumer import start_consumer
from app.api.v1.resume import router as resume_router
from app.api.v1.job_match import router as job_match_router
from app.api.v1.jd_analyzer import router as jd_analyzer_router
from app.api.v1.resume_optimizer import router as optimizer_router
from app.api.v1.ats_scorer import router as ats_router
from app.api.v1.cold_email import router as email_router
from app.api.v1.orchestration import router as pipeline_router

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s in %s mode", settings.SERVICE_NAME, settings.ENVIRONMENT)
    consumer_task = asyncio.create_task(start_consumer())
    logger.info("Kafka consumer task started")
    yield
    logger.info("Shutting down %s", settings.SERVICE_NAME)
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        logger.info("Kafka consumer stopped cleanly")


app = FastAPI(
    title="AI Job Copilot — AI Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(resume_router)
app.include_router(job_match_router)
app.include_router(jd_analyzer_router)
app.include_router(optimizer_router)
app.include_router(ats_router)
app.include_router(email_router)
app.include_router(pipeline_router)


@app.get("/health", tags=["ops"])
async def health():
    return {
        "status":      "healthy",
        "service":     settings.SERVICE_NAME,
        "environment": settings.ENVIRONMENT,
    }