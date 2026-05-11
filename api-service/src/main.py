import logging
from contextlib import asynccontextmanager
from typing import Final

from api_v1.api import api_router as api_v1_router
from core.app_orchestrator import AppOrchestrator
from core.config import settings as local_settings
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from shared.common_config import settings as common_settings
from shared.queue.broker import broker

log_level = logging.DEBUG if common_settings.debug else logging.ERROR
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    app_orchestrator = AppOrchestrator()
    await app_orchestrator.setup()
    await broker.startup()
    yield
    await app_orchestrator.shutdown()
    await broker.shutdown()


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)


async def validate_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != local_settings.x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
    return api_key


app: Final[FastAPI] = FastAPI(
    title="Fresh Harvest API",
    lifespan=lifespan,
    dependencies=[Depends(validate_api_key)],
)
app.include_router(
    router=api_v1_router,
    tags=[api_v1_router.prefix],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(str(exc))
    return JSONResponse(
        status_code=500, content={"status": "failed", "details": str(exc)}
    )
