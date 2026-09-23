from fastapi import FastAPI

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