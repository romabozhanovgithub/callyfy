"""Pydantic schemas for API request/response validation."""

from .audio import RawAudioArtifactBase, RawAudioArtifactCreate, RawAudioArtifactResponse
from .base import BaseSchema
from .capture import (
    ScreenCaptureBase,
    ScreenCaptureCreate,
    ScreenCaptureList,
    ScreenCaptureResponse,
)
from .meeting import (
    MeetingBase,
    MeetingCreate,
    MeetingList,
    MeetingResponse,
    MeetingUpdate,
    MeetingWithParticipants,
    ParticipantBase,
    ParticipantCreate,
    ParticipantResponse,
)
from .search import SearchQuery, SearchResults, VisualSearchQuery, VisualSearchResults
from .summary import SummaryBase, SummaryCreate, SummaryKind, SummaryList, SummaryResponse
from .transcript import (
    TranscriptSegmentBase,
    TranscriptSegmentCreate,
    TranscriptSegmentResponse,
    TranscriptSegmentWithSpeaker,
)

__all__ = [
    # Base
    "BaseSchema",
    # Meeting
    "MeetingBase",
    "MeetingCreate",
    "MeetingResponse",
    "MeetingList",
    "MeetingUpdate",
    "MeetingWithParticipants",
    "ParticipantBase",
    "ParticipantCreate",
    "ParticipantResponse",
    # Transcript
    "TranscriptSegmentBase",
    "TranscriptSegmentCreate",
    "TranscriptSegmentResponse",
    "TranscriptSegmentWithSpeaker",
    # Screen Capture
    "ScreenCaptureBase",
    "ScreenCaptureCreate",
    "ScreenCaptureResponse",
    "ScreenCaptureList",
    # Summary
    "SummaryBase",
    "SummaryCreate",
    "SummaryResponse",
    "SummaryList",
    "SummaryKind",
    # Audio
    "RawAudioArtifactBase",
    "RawAudioArtifactCreate",
    "RawAudioArtifactResponse",
    # Search
    "SearchQuery",
    "SearchResults",
    "VisualSearchQuery",
    "VisualSearchResults",
]
