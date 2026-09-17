from fastapi import FastAPI

app = FastAPI(
    title="HelioSL API",
    description="Agentic AI Renewable Energy Intelligence Platform for Sri Lanka",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "name": "HelioSL",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }