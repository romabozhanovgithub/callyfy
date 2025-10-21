from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Meeting, RawAudioArtifact, ScreenCapture, SummaryRecord, TranscriptSegment


@dataclass
class StorageService:
    base_dir: Path

    async def create_meeting(self, title: str, session: AsyncSession) -> Meeting:
        meeting = Meeting(title=title)
        session.add(meeting)
        await session.commit()
        await session.refresh(meeting)
        (self.base_dir / meeting.id).mkdir(parents=True, exist_ok=True)
        return meeting

    async def list_meetings(self, session: AsyncSession) -> list[Meeting]:
        result = await session.execute(select(Meeting))
        return list(result.scalars())

    async def get_meeting_assets(
        self, meeting: Meeting, session: AsyncSession
    ) -> tuple[
        list[TranscriptSegment], list[ScreenCapture], list[SummaryRecord], list[RawAudioArtifact]
    ]:
        transcripts = await session.execute(
            select(TranscriptSegment).where(TranscriptSegment.meeting_id == meeting.id)
        )
        captures = await session.execute(
            select(ScreenCapture).where(ScreenCapture.meeting_id == meeting.id)
        )
        summaries = await session.execute(
            select(SummaryRecord).where(SummaryRecord.meeting_id == meeting.id)
        )
        audio = await session.execute(
            select(RawAudioArtifact).where(RawAudioArtifact.meeting_id == meeting.id)
        )
        return (
            list(transcripts.scalars()),
            list(captures.scalars()),
            list(summaries.scalars()),
            list(audio.scalars()),
        )

    def resolve_meeting_dir(self, meeting: Meeting) -> Path:
        return self.base_dir / meeting.id

    def resolve_audio_path(self, meeting: Meeting, filename: str) -> Path:
        return self.resolve_meeting_dir(meeting) / filename

    def resolve_screen_dir(self, meeting: Meeting) -> Path:
        path = self.resolve_meeting_dir(meeting) / "screens"
        path.mkdir(parents=True, exist_ok=True)
        return path
