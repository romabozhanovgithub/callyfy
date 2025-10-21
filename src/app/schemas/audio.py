from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema


class RawAudioArtifactBase(BaseSchema):
    """Base audio artifact schema."""

    file_path: str = Field(..., max_length=512)
    sample_rate: Optional[int] = Field(None, gt=0)
    duration_seconds: Optional[float] = Field(None, gt=0)


class RawAudioArtifactCreate(BaseSchema):
    """Schema for creating an audio artifact record."""

    meeting_id: str
    file_path: str = Field(..., max_length=512)
    sample_rate: Optional[int] = Field(None, gt=0)
    duration_seconds: Optional[float] = Field(None, gt=0)


class RawAudioArtifactResponse(RawAudioArtifactBase):
    """Schema for audio artifact response."""

    id: int
    meeting_id: str
    recorded_at: datetime
