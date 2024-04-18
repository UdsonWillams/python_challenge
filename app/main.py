import logging
from logging.config import dictConfig

from fastapi import FastAPI
from uvicorn import run

from app.api.v1.api_health import router as health_check_router
from app.api.v1.words.sort.views import router as sort_router
from app.api.v1.words.vowel_count.views import router as vowel_count_router
from app.utils.config import return_default_settings
from app.utils.logger import LogConfig
from app.utils.middlewares import ResponseTimeMiddleware

dictConfig(LogConfig().model_dump())

logger = logging.getLogger("app")
settings = return_default_settings()

app = FastAPI()
api_v1 = "/api/v1"
app.include_router(health_check_router)
app.include_router(sort_router, prefix=api_v1)
app.include_router(vowel_count_router, prefix=api_v1)
app.add_middleware(ResponseTimeMiddleware)


if __name__ == "__main__":
    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.IS_DEBUG,
        workers=settings.WORKERS,
    )
