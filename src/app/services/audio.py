from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Meeting, RawAudioArtifact, TranscriptSegment


class AudioCaptureBackend(Protocol):
    async def start_stream(self, meeting: Meeting) -> None: ...

    async def stop_stream(self, meeting: Meeting) -> None: ...

    async def iter_chunks(self, meeting: Meeting) -> Iterable[bytes]: ...

    async def record_raw_audio(self, meeting: Meeting, destination: Path) -> None: ...


class ASRBackend(Protocol):
    async def transcribe_chunk(self, audio: bytes) -> TranscriptSegment: ...

    async def transcribe_file(self, audio_path: Path) -> Iterable[TranscriptSegment]: ...


@dataclass
class AudioService:
    capture_backend: AudioCaptureBackend
    asr_backend: ASRBackend

    async def start_capture(self, meeting: Meeting) -> None:
        await self.capture_backend.start_stream(meeting)

    async def stop_capture(self, meeting: Meeting) -> None:
        await self.capture_backend.stop_stream(meeting)

    async def process_live_chunk(
        self, meeting: Meeting, chunk: bytes, session: AsyncSession
    ) -> TranscriptSegment:
        transcript = await self.asr_backend.transcribe_chunk(chunk)
        transcript.meeting_id = meeting.id  # type: ignore[attr-defined]
        session.add(transcript)
        await session.commit()
        return transcript

    async def record_full_audio(
        self, meeting: Meeting, destination: Path, session: AsyncSession
    ) -> RawAudioArtifact:
        await self.capture_backend.record_raw_audio(meeting, destination)
        artifact = RawAudioArtifact(meeting_id=meeting.id, file_path=str(destination))
        session.add(artifact)
        await session.commit()
        return artifact

    async def post_process_audio(
        self, artifact: RawAudioArtifact, session: AsyncSession
    ) -> list[TranscriptSegment]:
        segments: list[TranscriptSegment] = []
        for segment in await self.asr_backend.transcribe_file(Path(artifact.file_path)):
            segment.meeting_id = artifact.meeting_id  # type: ignore[attr-defined]
            segments.append(segment)
            session.add(segment)
        await session.commit()
        return segments
