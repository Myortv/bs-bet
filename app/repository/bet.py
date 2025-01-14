from typing import List

from app.schemas.bet import BetInDB, BetCreate, BetUpdate


from app.tools.db import (
    postgres_manager,
    PostgresManager,
    DatabaseConnection,
)
from app.tools.db_t import test_postgres_manager


class BetRepository():
    def __init__(
        self,
        manager: PostgresManager = postgres_manager,
    ):
        self.manager = manager

    async def get_list(self) -> List[BetInDB]:
        async with DatabaseConnection(self.manager) as conn:
            result = await conn.fetch(
                """select * from bet""",
            )
            if result:
                return [BetInDB(**row) for row in result]

    async def create(self, bet_data: BetCreate) -> BetInDB:
        async with DatabaseConnection(self.manager) as conn:
            result = await conn.fetchrow(
                """
                insert into bet (event_id, bet_amount)
                values ($1, $2)
                returning *
                """,
                bet_data.event_id,
                bet_data.bet_amount
            )
            if result:
                return BetInDB(**result)

    async def update_bets_statuses_on_event_change(
        self,
        event_id: int,
        bet_data: BetUpdate,
    ) -> BetInDB:
        async with DatabaseConnection(self.manager) as conn:
            result = await conn.fetchrow(
                """
                update bet set status = $1
                where event_id = $2
                """,
                bet_data.status.value,
                event_id,
            )
            if result:
                return BetInDB(**result)


def injectBetRepository():
    return BetRepository()


def injectTestBetRepository() -> BetRepository:
    return BetRepository(manager=test_postgres_manager)
