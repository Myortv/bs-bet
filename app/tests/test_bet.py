import pytest

from httpx import AsyncClient, ASGITransport


from app.main import app

from app.tests.fixtures import (
    base_setup,
    postgres_cleanup,
    event_loop,
    anyio_backend,
    async_setup_lifespan,
)


@pytest.mark.anyio
async def test_list_bets(
    postgres_cleanup,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            'bet/api/v1/bet/bets',
        )
        assert response.status_code == 404
        await base_setup()
        response = await ac.get(
            'bet/api/v1/bet/bets',
        )
        assert response.status_code == 200


@pytest.mark.anyio
async def test_create_bad_input(
    postgres_cleanup,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            'bet/api/v1/bet/bet',
            json={
                  "event_id": 1,
                  "bet_amount": -10
            }
        )
        assert response.status_code != 200

        response = await ac.post(
            'bet/api/v1/bet/bet',
            json={
                  "event_id": 1,
                  "bet_amount": 1.11111
            }
        )
        assert response.status_code != 200


@pytest.mark.anyio
async def test_create(
    postgres_cleanup,
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            'bet/api/v1/bet/bet',
            json={
                  "event_id": 1,
                  "bet_amount": 10
            }
        )
        assert response.status_code == 200
