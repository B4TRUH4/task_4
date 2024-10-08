import asyncio
import functools
import os
import time
from datetime import datetime
from typing import Callable

import aiohttp
from aiohttp import ClientSession

from config import DOWNLOAD_DIR, SEMAPHORE_COUNT, TIMEOUT
from download import fetch_and_save, generate_links
from database import prepare_db, Session
from repository import TradingResultsRepository
from models import TradingResult
from processing import read_table


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"Функция {func.__name__} выполнялась {end - start:.4f} секунд")
        return result

    return wrapper


async def process(
    session: ClientSession,
    link: str,
    trade_date: datetime.date,
    semaphore: asyncio.Semaphore,
) -> None:
    filename = os.path.join(DOWNLOAD_DIR, f'bulletin_{trade_date}.xls')
    await fetch_and_save(session, link, filename, semaphore)
    if not os.path.exists(filename):
        return
    df = read_table(filename)
    repository = TradingResultsRepository(Session())
    results = []
    for index, row in df.iterrows():
        trading_result = TradingResult(
            exchange_product_id=row['код инструмента'],
            exchange_product_name=row['наименование инструмента'],
            oil_id=row['код инструмента'][:4],
            delivery_basis_id=row['код инструмента'][4:7],
            delivery_basis_name=row['базис поставки'],
            delivery_type_id=row['код инструмента'][-1],
            volume=int(row['объем договоров в единицах измерения']),
            total=int(row['обьем договоров, руб.']),
            count=int(row['количество договоров, шт.']),
            date=trade_date,
        )
        results.append(trading_result)
    await repository.save_many(results)


@timer
async def main() -> None:
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    links = generate_links()
    await prepare_db()
    semaphore = asyncio.Semaphore(SEMAPHORE_COUNT)
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=TIMEOUT)
    ) as session:
        tasks = []
        for link, trade_date in links:
            tasks.append(process(session, link, trade_date, semaphore))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
