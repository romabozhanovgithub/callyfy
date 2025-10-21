from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema


class ParticipantBase(BaseSchema):
    """Base participant schema."""

    name: str = Field(..., max_length=255)
    role: Optional[str] = Field(None, max_length=100)


class ParticipantCreate(ParticipantBase):
    """Schema for creating a participant."""

    pass


class ParticipantResponse(ParticipantBase):
    """Schema for participant response."""

    id: int
    meeting_id: str


class MeetingBase(BaseSchema):
    """Base meeting schema."""

    title: str = Field(..., max_length=255)


class MeetingCreate(MeetingBase):
    """Schema for creating a meeting."""

    pass


class MeetingResponse(MeetingBase):
    """Schema for meeting response with full details."""

    id: str
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class MeetingWithParticipants(MeetingResponse):
    """Schema for meeting response with participants."""

    participants: list[ParticipantResponse] = []


class MeetingList(BaseSchema):
    """Schema for meeting list item."""

    id: str
    title: str
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class MeetingUpdate(BaseSchema):
    """Schema for updating meeting fields."""

    title: Optional[str] = Field(None, max_length=255)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
