import asyncio

from functools import partial
from typing import Generator


import pytest


from app.tools.db_t import (
    init_tets_postgres,
    stop_test_asyncpg,
    test_postgres_manager
)
from app.repository.bet import (
    injectBetRepository,
    injectTestBetRepository,
)
from app.core.config import configs


from app.main import app


app.dependency_overrides[injectBetRepository] = injectTestBetRepository


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()



@pytest.fixture(scope="session", autouse=True)
async def async_setup_lifespan(anyio_backend):
    await init_tets_postgres(
        configs.TEST_POSTGRES_DB,
        configs.TEST_POSTGRES_HOST,
        configs.POSTGRES_USER,
        configs.POSTGRES_PASSWORD,
    )
    await test_postgres_manager.reset()
    yield
    await stop_test_asyncpg()


@pytest.fixture(scope="function")
async def postgres_cleanup():
    await test_postgres_manager.cleanup()
    yield
    # await test_postgres_manager.cleanup()


async def base_setup():
    from app.schemas.bet import BetCreate

    bet_repo = injectTestBetRepository()

    items = [
        BetCreate(
           event_id=1,
           bet_amount=1.1,
        ),
        BetCreate(
           event_id=2,
           bet_amount=2.2,
        ),
        BetCreate(
           event_id=3,
           bet_amount=3.3,
        ),
        BetCreate(
           event_id=4,
           bet_amount=4.4,
        ),
        BetCreate(
           event_id=1,
           bet_amount=5,
        ),
    ]
    for item in items:
        await bet_repo.create(item)
