import enum


from pydantic import BaseModel

from app.tools.types import Positive2DecimalPlaces


class EventState(enum.Enum):
    NEW = 'new'
    FINISHED_WIN = 'finished_win'
    FINISHED_LOSE = 'finished_lose'


class Event(BaseModel):
    event_id: int
    coefficient: Positive2DecimalPlaces
    deadline: int
    state: EventState
