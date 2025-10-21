from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from .base import BaseSchema


class SummaryKind(str, Enum):
    """Summary type enumeration."""

    RELEVANT = "relevant"
    ROLLING = "rolling"
    FINAL = "final"


class SummaryBase(BaseSchema):
    """Base summary schema."""

    kind: SummaryKind
    content: str = Field(..., min_length=1)


class SummaryCreate(SummaryBase):
    """Schema for creating a summary."""

    model_name: Optional[str] = Field(None, max_length=100)


class SummaryResponse(SummaryBase):
    """Schema for summary response."""

    id: int
    meeting_id: str
    generated_at: datetime
    model_name: Optional[str] = None


class SummaryList(BaseSchema):
    """Schema for summary list item."""

    id: int
    meeting_id: str
    kind: SummaryKind
    generated_at: datetime
    content_preview: str = Field(..., description="First 200 characters of content")
