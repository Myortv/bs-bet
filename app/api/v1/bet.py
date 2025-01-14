from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends


from app.repository.bet import injectBetRepository, BetRepository

from app.schemas.bet import (
    BetInDB,
    BetCreate,
    BetUpdate,
)

api = APIRouter()


BetRepo = Annotated[BetRepository, Depends(injectBetRepository)]


@api.get('/bets', response_model=List[BetInDB])
async def get_bets(
    bet_repository: Annotated[BetRepository, Depends(injectBetRepository)],
    # bet_repository: BetRepo,
):
    import logging
    logging.warning(bet_repository)
    if result := await bet_repository.get_list():
        return result
    raise HTTPException(404)


@api.post('/bet', response_model=BetInDB)
async def create_bet(
    bet_data: BetCreate,
    bet_repository: BetRepo,
):
    import logging
    logging.warning(bet_repository)
    if result := await bet_repository.create(
        bet_data,
    ):
        return result
    raise HTTPException(500)
