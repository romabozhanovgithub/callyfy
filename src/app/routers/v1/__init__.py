from fastapi import APIRouter

from . import meetings

router = APIRouter(prefix="/v1")
router.include_router(meetings.router)
