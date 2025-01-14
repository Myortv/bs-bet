from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI


from app.core.config import configs, tags_metadata

from app.tools.rabbit import rabbit_manager
from app.tools.db import init_asyncpg

from app.messages.event import event_messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to rabbit
    await rabbit_manager.initialize(
        "amqp://guest:guest@rabbitmq:",
        10,
    )
    for items in [
        *event_messages.return_subscribers()
    ]:
        rabbit_manager.subscribe(*items)
    await rabbit_manager.start_consuming()
    await init_asyncpg(
        configs.POSTGRES_DB,
        configs.POSTGRES_HOST,
        configs.POSTGRES_USER,
        configs.POSTGRES_PASSWORD,
    )

    yield
    await rabbit_manager.stop()

app = FastAPI(
    title=configs.PROJECT_NAME,
    version='0.0.1',
    docs_url=configs.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{configs.API_V1_STR}/openapi.json',
    lifespan=lifespan,
    # exception_handlers=handled_exceptions,
)

if configs.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from app.api.v1 import (
    bet,
    event,
)

app.include_router(
    bet.api,
    prefix=configs.API_V1_STR + "/bet",
    tags=["bet"]
)
app.include_router(
    event.api,
    prefix=configs.API_V1_STR + "/event",
    tags=["event"]
)
