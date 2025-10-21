from typing import AsyncGenerator

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core import settings


def get_settings(app: FastAPI) -> settings.Settings:
    """Get the settings."""
    return app.state.settings


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session from app state.

    This is a FastAPI dependency that retrieves the session maker from
    the application state and yields a database session for each request.

    Args:
        request: FastAPI request object.

    Yields:
        AsyncSession: Database session.
    """

    session_maker: async_sessionmaker[AsyncSession] = request.app.state.db_session_maker
    async with session_maker() as session:
        yield session
