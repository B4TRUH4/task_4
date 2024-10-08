import os
import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

DOWNLOAD_DIR = 'bulletins'


START_DATE = datetime.date(2023, 1, 1)

COLUMNS = [
    'код инструмента',
    'наименование инструмента',
    'базис поставки',
    'объем договоров в единицах измерения',
    'обьем договоров, руб.',
    'количество договоров, шт.',
]

BASE_LINK = 'https://spimex.com/upload/reports/oil_xls/oil_xls_{}162000.xls'

RETRIES = 3
SEMAPHORE_COUNT = 10
TIMEOUT = 2
