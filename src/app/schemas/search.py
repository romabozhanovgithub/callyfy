from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import BaseSchema
from .capture import ScreenCaptureList
from .summary import SummaryList
from .transcript import TranscriptSegmentResponse


class SearchQuery(BaseSchema):
    """Schema for search query parameters."""

    query: str = Field(..., min_length=1, max_length=500)
    meeting_id: Optional[str] = Field(None, description="Filter by specific meeting")
    limit: int = Field(20, ge=1, le=100)


class SearchResults(BaseSchema):
    """Schema for search results."""

    transcripts: list[TranscriptSegmentResponse] = []
    summaries: list[SummaryList] = []
    screen_captures: list[ScreenCaptureList] = []
    total_results: int = Field(..., description="Total number of results across all categories")


class VisualSearchQuery(BaseSchema):
    """Schema for visual search query."""

    embedding: bytes = Field(..., description="Query embedding for similarity search")
    meeting_id: Optional[str] = Field(None, description="Filter by specific meeting")
    limit: int = Field(10, ge=1, le=50)


class VisualSearchResults(BaseSchema):
    """Schema for visual search results."""

    captures: list[ScreenCaptureList] = []
    total_results: int
