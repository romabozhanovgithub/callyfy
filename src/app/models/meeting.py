from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    participants: Mapped[List[Participant]] = relationship("Participant", back_populates="meeting")
    transcripts: Mapped[List[TranscriptSegment]] = relationship(
        "TranscriptSegment", back_populates="meeting", cascade="all, delete-orphan"
    )
    screen_captures: Mapped[List[ScreenCapture]] = relationship(
        "ScreenCapture", back_populates="meeting", cascade="all, delete-orphan"
    )
    summaries: Mapped[List[SummaryRecord]] = relationship(
        "SummaryRecord", back_populates="meeting", cascade="all, delete-orphan"
    )
    audio_artifacts: Mapped[List[RawAudioArtifact]] = relationship(
        "RawAudioArtifact", back_populates="meeting", cascade="all, delete-orphan"
    )


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="participants")


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE")
    )
    speaker_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("participants.id"), nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="transcripts")
    speaker: Mapped[Optional[Participant]] = relationship("Participant")


class ScreenCapture(Base):
    __tablename__ = "screen_captures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE")
    )
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    image_path: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    embeddings_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="screen_captures")


class SummaryRecord(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE")
    )
    kind: Mapped[str] = mapped_column(String(50), nullable=False)  # relevant, rolling, final
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="summaries")


class RawAudioArtifact(Base):
    __tablename__ = "raw_audio_artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE")
    )
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    sample_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(nullable=True)

    meeting: Mapped[Meeting] = relationship("Meeting", back_populates="audio_artifacts")
