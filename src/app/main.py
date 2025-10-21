from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError

from app.core import errors, exception_handlers
from app.core import settings as app_settings
from app.db import database
from app.routers import v1 as v1_router


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = app_settings.Settings()
    app.state.settings = settings

    # Initialize database
    engine = database.create_db_engine(settings.db)
    db_session_maker = database.create_session_factory(engine)
    app.state.db_engine = engine
    app.state.db_session_maker = db_session_maker
    await database.init_db_tables(engine)

    yield

    # Database shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    settings = app_settings.Settings()

    app = FastAPI(
        title=settings.app.NAME,
        version=settings.app.VERSION,
        description="Local meeting assistant",
        lifespan=lifespan,
    )

    # Exception handlers
    app.add_exception_handler(errors.AppError, exception_handlers.app_error_handler)
    app.add_exception_handler(
        RequestValidationError,
        exception_handlers.validation_exception_handler,
    )

    # Routers
    api_router = APIRouter(prefix="/api")
    api_router.include_router(v1_router.router)
    app.include_router(api_router)

    return app
