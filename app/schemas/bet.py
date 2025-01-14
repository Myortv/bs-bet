import enum

from typing import Optional


from pydantic import BaseModel

from app.tools.types import Positive2DecimalPlaces


class BetStatus(enum.Enum):
    pending = 'pending'
    win = 'win'
    lose = 'lose'


class BetInDB(BaseModel):
    id: int
    event_id: int
    bet_amount: Positive2DecimalPlaces
    status: BetStatus


class BetCreate(BaseModel):
    event_id: int
    bet_amount: Positive2DecimalPlaces


class BetUpdate(BaseModel):
    status: BetStatus
