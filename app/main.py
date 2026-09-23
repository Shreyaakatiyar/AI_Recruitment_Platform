from fastapi import FastAPI

from app.database import Base, engine
from app.models import db_models  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Recruitment & Candidate Matching Platform",
    description="AI-powered platform for matching candidates against job descriptions",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "AI Recruitment Platform API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}