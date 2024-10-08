from sqlalchemy.ext.asyncio import AsyncSession
from models import TradingResult


class TradingResultsRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def save_one(self, obj: TradingResult):
        print(f'Сохранение {obj.date}')
        self.session.add(obj)
        await self.session.commit()

    async def save_many(self, objs: list[TradingResult]):
        self.session.add_all(objs)
        await self.session.commit()
