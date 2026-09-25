from fastapi import FastAPI
import logging

from app.database import Base, engine
from app.models import db_models  
from app.routers import jobs, resumes, candidates, matching

from fastapi import Request
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(
    title="AI Recruitment & Candidate Matching Platform",
    description="AI-powered platform for matching candidates against job descriptions",
    version="0.1.0",
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal error occurred. Please try again later."},
    )

app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(candidates.router)
app.include_router(matching.router)


@app.get("/")
def root():
    return {"message": "AI Recruitment Platform API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}