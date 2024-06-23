import uvicorn as uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.healthcheck import root_router
from api.rates import rates_router
from config import settings
from db import persistent_engine
from models.db_models.base_engine import Model

docs_conf = {"docs_url": None, "redoc_url": None, "openapi_url": None}
if settings.ENABLE_DOCS:
    docs_conf["docs_url"] = "/docs"
    docs_conf["redoc_url"] = "/redoc"
    docs_conf["openapi_url"] = "/openapi.json"


app = FastAPI(
    version="0.0.1",
    title=settings.PROJECT_NAME,
    description="NBRB microservices family",
    **docs_conf,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

middlewares = [
    # AuthMiddleware(),
]

app.include_router(root_router)
app.include_router(rates_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
        log_config=None,
    )
