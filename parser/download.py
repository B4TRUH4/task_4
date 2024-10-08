import asyncio
import os
import pandas as pd
import aiohttp
import datetime

from aiohttp import ClientSession

from config import START_DATE, BASE_LINK, RETRIES


def generate_date_range() -> list[datetime.date]:
    dates = pd.date_range(start=START_DATE, end=datetime.date.today())
    return [date.date() for date in dates]


def generate_links() -> list[tuple[str, datetime.date]]:
    links = [
        (BASE_LINK.format(date.strftime('%Y%m%d')), date)
        for date in generate_date_range()
    ]
    return links


async def file_exists(filename: str) -> bool:
    if os.path.exists(filename):
        print(f'Файл {filename} существует. Пропуск...')
        return True
    return False


async def download_content(session: ClientSession, url: str) -> bytes:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.read()


def save_to_file(filename: str, content: bytes) -> None:
    with open(filename, 'wb') as file:
        file.write(content)
    print(f'Файл {filename} сохранен.')


async def fetch_with_retries(
    session: ClientSession, url: str, retries: int = RETRIES
) -> bytes | None:
    for attempt in range(retries):
        try:
            content = await download_content(session, url)
            return content
        except asyncio.TimeoutError:
            print(
                f'Таймаут при попытке {attempt + 1} загрузить {url}. Повтор...'
            )
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                print(f'Файла {url} не существует. Пропуск...')
                return
            else:
                print(
                    f'Ошибка {e} при попытке {attempt + 1} '
                    f'загрузить {url}. Повтор...'
                )
        await asyncio.sleep(1)

    print(f'Не удалось загрузить файл {url} после {retries} попыток.')
    return


async def fetch_and_save(
    session: ClientSession,
    url: str,
    filename: str,
    semaphore: asyncio.Semaphore,
) -> None:
    if await file_exists(filename):
        return
    async with semaphore:
        content = await fetch_with_retries(session, url)
        if content:
            save_to_file(filename, content)
