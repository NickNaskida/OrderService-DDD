import uvicorn
from fastapi import FastAPI

from src.core.settings import settings
from src.features.allocation.api.api import api_router

app = FastAPI(
    title="Allocation API",
    description="API for the allocation service",
    version="0.1.0",
    docs_url="/",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, proxy_headers=True, log_level="debug")
