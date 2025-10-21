from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core import settings as app_settings
from app.db import base as db_base


def create_db_engine(db_settings: app_settings.DBSettings) -> AsyncEngine:
    """
    Create async database engine from settings.

    Args:
        db_settings: Database configuration settings.

    Returns:
        AsyncEngine: Configured async database engine.
    """

    return create_async_engine(
        db_settings.url,
        echo=db_settings.ECHO,
        future=db_settings.FUTURE,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Create session maker from engine.

    Args:
        engine: Database engine.

    Returns:
        async_sessionmaker: Session factory for creating database sessions.
    """

    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def init_db_tables(engine: AsyncEngine) -> None:
    """
    Initialize database tables.

    Args:
        engine: Database engine.
    """

    async with engine.begin() as conn:
        await conn.run_sync(db_base.Base.metadata.create_all)
