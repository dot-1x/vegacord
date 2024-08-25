from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.core.config import settings

if settings.ENVIRONMENT == "PRD":
    DBURI = settings.MAIN_DB_URI
else:
    DBURI = settings.TEST_DB_URI

async_engine = create_async_engine(DBURI, pool_pre_ping=True)
session_maker = async_sessionmaker(async_engine, expire_on_commit=True)
