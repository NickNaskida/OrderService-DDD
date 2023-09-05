import uvicorn
from fastapi import FastAPI

from src.features.allocation.infrastructure import adapter
from src.core.settings import settings
from src.features.allocation.api.api import api_router

app = FastAPI(
    title="Allocation API",
    description="API for the allocation service",
    version="0.1.0",
    docs_url="/",
)


# add routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# start db mappers
adapter.start_mappers()


if __name__ == "__main__":
    uvicorn.run(app, port=8000, proxy_headers=True, log_level="debug")
