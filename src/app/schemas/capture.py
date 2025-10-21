from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema


class ScreenCaptureBase(BaseSchema):
    """Base screen capture schema."""

    image_path: str = Field(..., max_length=512)
    description: Optional[str] = None
    embeddings_path: Optional[str] = Field(None, max_length=512)


class ScreenCaptureCreate(BaseSchema):
    """Schema for creating a screen capture record."""

    meeting_id: str
    image_path: str = Field(..., max_length=512)
    description: Optional[str] = None


class ScreenCaptureResponse(ScreenCaptureBase):
    """Schema for screen capture response."""

    id: int
    meeting_id: str
    captured_at: datetime


class ScreenCaptureList(BaseSchema):
    """Schema for screen capture list item."""

    id: int
    meeting_id: str
    captured_at: datetime
    image_path: str
    description: Optional[str] = None
