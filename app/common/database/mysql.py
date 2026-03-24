from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession
)
from ..config.settings import settings
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = (
    f"mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# --- FIXED ENGINE CONFIG ---
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,      # IMPORTANT: validates connection before using it
    pool_recycle=180,        # IMPORTANT: prevents stale connections
)

# --- FIXED SESSION CONFIG ---
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# --- DB INIT ---
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda x: None)
        logger.info("MySQL Database connected successfully")
    except Exception as e:
        logger.error(f"MySQL Database connection failed: {e}")

# --- PROVIDE SESSION ---
async def get_async_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
