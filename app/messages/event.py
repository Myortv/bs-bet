from typing import Optional

import json


from aio_pika import Message


from app.schemas.event import (
    Event,
    EventState,
)

from app.schemas.bet import BetUpdate, BetStatus


from app.tools.rabbit import RabbitMQ, rabbit_manager
from app.repository.bet import BetRepository, injectBetRepository


class EventMessages():
    def __init__(
        self,
        manager: Optional[RabbitMQ] = rabbit_manager,
        exchange_name: Optional[str] = "event",
        queue_name: Optional[str] = "event",
        bet_manager: Optional[BetRepository] = injectBetRepository(),
    ):
        self.bet_manager = bet_manager
        # self.manager = manager
        # self.exchange_name = exchange_name

    async def consume_event_update(
        self,
        payload: dict
    ) -> None:
        old_event = Event(**payload.get('old_event'))
        updated_event = Event(**payload.get('updated_event'))
        if (
            old_event.state == EventState.NEW
            and old_event.state != updated_event.state
        ):
            match updated_event.state:
                case EventState.FINISHED_LOSE:
                    bet_data = BetUpdate(
                        status=BetStatus.lose,
                    )
                case EventState.FINISHED_WIN:
                    bet_data = BetUpdate(
                        status=BetStatus.win,
                    )

            await self.bet_manager.update_bets_statuses_on_event_change(
                updated_event.event_id,
                bet_data,
            )

    def return_subscribers(self):
        return [
            ('event', 'update', self.consume_event_update)
        ]


async def injectEventMessages():
    return EventMessages()


event_messages = EventMessages()
