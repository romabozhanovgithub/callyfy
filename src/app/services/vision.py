from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Meeting, ScreenCapture


class ScreenCaptureBackend(Protocol):
    async def capture(self, meeting: Meeting, destination: Path) -> Path: ...


class VisionLanguageModel(Protocol):
    async def describe_image(self, image_path: Path) -> str: ...

    async def embed_image(self, image_path: Path) -> bytes: ...


@dataclass
class VisionService:
    capture_backend: ScreenCaptureBackend
    vlm: VisionLanguageModel

    async def capture_screen(
        self, meeting: Meeting, output_dir: Path, session: AsyncSession
    ) -> ScreenCapture:
        image_path = await self.capture_backend.capture(meeting, output_dir)
        description = await self.vlm.describe_image(image_path)
        embeddings_path = output_dir / f"{Path(image_path).stem}.emb"
        embeddings = await self.vlm.embed_image(image_path)
        embeddings_path.write_bytes(embeddings)

        capture = ScreenCapture(
            meeting_id=meeting.id,
            image_path=str(image_path),
            description=description,
            embeddings_path=str(embeddings_path),
        )
        session.add(capture)
        await session.commit()
        return capture
