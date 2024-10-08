from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from models import Base
from dotenv import load_dotenv
from config import DATABASE_URL

load_dotenv()
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(bind=engine)


async def prepare_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
