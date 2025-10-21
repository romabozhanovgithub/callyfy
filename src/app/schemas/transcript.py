from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema


class TranscriptSegmentBase(BaseSchema):
    """Base transcript segment schema."""

    text: str = Field(..., min_length=1)
    started_at: datetime
    ended_at: datetime
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class TranscriptSegmentCreate(TranscriptSegmentBase):
    """Schema for creating a transcript segment."""

    speaker_id: Optional[int] = None


class TranscriptSegmentResponse(TranscriptSegmentBase):
    """Schema for transcript segment response."""

    id: int
    meeting_id: str
    speaker_id: Optional[int] = None


class TranscriptSegmentWithSpeaker(TranscriptSegmentResponse):
    """Schema for transcript segment with speaker name."""

    speaker_name: Optional[str] = None
