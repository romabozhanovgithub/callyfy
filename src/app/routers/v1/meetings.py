from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.models import Meeting
from app.schemas import MeetingCreate, MeetingList, MeetingResponse
from app.services import StorageService

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("/", response_model=list[MeetingList])
async def list_meetings(
    session: AsyncSession = Depends(deps.get_session),
    storage: StorageService = Depends(),
) -> list[Meeting]:
    """List all meetings."""
    meetings = await storage.list_meetings(session)
    return meetings


@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    meeting_data: MeetingCreate,
    session: AsyncSession = Depends(deps.get_session),
    storage: StorageService = Depends(),
) -> Meeting:
    """Create a new meeting."""
    meeting = await storage.create_meeting(title=meeting_data.title, session=session)
    return meeting


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: str,
    session: AsyncSession = Depends(deps.get_session),
) -> Meeting:
    """Get a specific meeting by ID."""
    meeting = await session.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return meeting


@router.post("/{meeting_id}/start", response_model=MeetingResponse)
async def start_meeting(
    meeting_id: str,
    session: AsyncSession = Depends(deps.get_session),
) -> Meeting:
    """Mark a meeting as started."""
    meeting = await session.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    if not meeting.started_at:
        meeting.started_at = datetime.utcnow()
    await session.commit()
    await session.refresh(meeting)
    return meeting


@router.post("/{meeting_id}/stop", response_model=MeetingResponse)
async def stop_meeting(
    meeting_id: str,
    session: AsyncSession = Depends(deps.get_session),
) -> Meeting:
    """Mark a meeting as ended."""
    meeting = await session.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    if not meeting.ended_at:
        meeting.ended_at = datetime.utcnow()
    await session.commit()
    await session.refresh(meeting)
    return meeting
