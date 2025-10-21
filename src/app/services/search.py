from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ScreenCapture, SummaryRecord, TranscriptSegment


@dataclass
class SearchService:
    text_index_path: Path
    vector_index_path: Path

    async def full_text_search(self, query: str, session: AsyncSession) -> list[TranscriptSegment]:
        like_query = f"%{query}%"
        result = await session.execute(
            select(TranscriptSegment).where(TranscriptSegment.text.ilike(like_query))
        )
        return list(result.scalars())

    async def semantic_summary_search(
        self, query: str, session: AsyncSession
    ) -> list[SummaryRecord]:
        like_query = f"%{query}%"
        result = await session.execute(
            select(SummaryRecord).where(SummaryRecord.content.ilike(like_query))
        )
        return list(result.scalars())

    async def visual_search(
        self, query_embedding: bytes, session: AsyncSession
    ) -> list[ScreenCapture]:
        # TODO: integrate with local vector index (FAISS, Milvus Lite, LanceDB) using embeddings
        return []
