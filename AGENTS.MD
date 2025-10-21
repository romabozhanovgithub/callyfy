# Project Briefing

## Mission
Callyfy is a privacy-first, real-time meeting summarizer that runs entirely on the user's machine. It captures streaming audio from team calls, produces accurate transcripts, and distills the conversation into concise action items, decisions, and sentiment insights using lightweight local language models.

## Core Capabilities
- Streaming speech-to-text pipeline with sub-second latency using on-device ASR models.
- Automatic diarization to attribute statements to speakers without leaving the local environment.
- Decision and action-item extraction powered by compact local LLMs.
- Sentiment and engagement analysis across the conversation timeline while keeping data on-device.
- Optional linkage of summaries to local documentation, tickets, or CRM exports.

## System Overview
- `FastAPI` service orchestrates REST and WebSocket endpoints as well as background jobs.
- Asynchronous `SQLAlchemy` layer stores meetings, participants, transcripts, and summaries in a local database (SQLite by default).
- Local inference pipeline hosts small-footprint LLMs (e.g., GGUF/GGML variants via llama.cpp, Ollama, or similar runtimes) for summarization, classification, and task extraction.
- Audio preprocessing leverages FFmpeg-compatible tooling for normalization, chunking, and optional noise reduction.
- Background workers handle diarization, summarization retries, and notification dispatch using local queues or schedulers.

## Tech Stack
- Language: Python 3.12
- Framework: FastAPI (async)
- ASGI Server: Uvicorn
- ORM: SQLAlchemy with asyncio support
- Configuration: pydantic-settings (env-based)
- Packaging: Poetry
- Testing: Pytest, pytest-async
- Tooling: Black, Flake8, Isort, Mypy
- Local inference: llama.cpp/Ollama-compatible runtimes for quantized LLMs and ASR engines like Whisper.cpp or Vosk

## Integrations & Services
- Local speech-to-text engine (Whisper.cpp, Vosk, or equivalent) configured per environment.
- Local summarization provider using quantized models (e.g., Mistral-7B-Instruct GGUF) through llama.cpp/Ollama bindings.
- Optional offline connectors: export summaries to Markdown, JSON, or local ticketing systems; provide hooks for manual syncing with Notion, Slack, Jira.

## Operational Notes
- Environment variables stored in `.env`; see `src/app/core/settings.py` for defaults.
- Database defaults to SQLite via `sqlite+aiosqlite`, but Postgres can be used if available locally.
- Ensure FFmpeg is installed on hosts handling audio ingestion.
- Provision adequate CPU/GPU resources for local inference; document model paths and runtime flags.
- Schedule background workers locally (e.g., APScheduler, cron) for post-call summary polishing and notifications.
