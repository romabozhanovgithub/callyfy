from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Meeting, SummaryRecord


class SummaryKind(str, Enum):
    RELEVANT = "relevant"
    ROLLING = "rolling"
    FINAL = "final"


class SummarizationBackend(Protocol):
    async def summarize(self, meeting: Meeting, kind: SummaryKind) -> str: ...


@dataclass
class SummarizationService:
    backend: SummarizationBackend

    async def generate_summary(
        self, meeting: Meeting, kind: SummaryKind, session: AsyncSession
    ) -> SummaryRecord:
        content = await self.backend.summarize(meeting, kind)
        record = SummaryRecord(meeting_id=meeting.id, kind=kind.value, content=content)
        session.add(record)
        await session.commit()
        return record
