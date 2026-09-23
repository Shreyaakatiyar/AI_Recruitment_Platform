from fastapi import FastAPI

from app.database import Base, engine
from app.models import db_models  
from app.routers import jobs, resumes, candidates, matching

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Recruitment & Candidate Matching Platform",
    description="AI-powered platform for matching candidates against job descriptions",
    version="0.1.0",
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