import aiohttp

from asyncache import cached
from cachetools import TTLCache

from fastapi import APIRouter, HTTPException


from app.core.config import configs


api = APIRouter()


cache_ttl = 60


@api.get('/events')
async def get_events():
    return await get_events_req()


@cached(TTLCache(1024, ttl=cache_ttl))
async def get_events_req():
    async with aiohttp.ClientSession() as client:
        async with client.get(
            f'http://{configs.LINE_HOST}/line/api/v1/event/list'
        ) as response:
            if response.ok:
                return await response.json()
            raise HTTPException(response.status)
