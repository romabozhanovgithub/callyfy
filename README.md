# Callyfy

Callyfy is a privacy-first, real-time meeting assistant designed to run entirely on your local machine. It captures streaming audio, screen content, and generates rolling summaries using lightweight, quantized language models—no external cloud services required.

## Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Scheduling Cadence](#scheduling-cadence)
- [Integrations](#integrations)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Model & Runtime Setup](#model--runtime-setup)
- [Frontend Recommendations](#frontend-recommendations)
- [Post-Meeting Pipeline](#post-meeting-pipeline)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features

- Live speech-to-text capture every 2 seconds using on-device ASR models
- Full-session raw audio recording for high-fidelity post-processing
- Periodic screen capture (every 5 seconds) with vision-language analysis
- Rolling “relevant” summaries every 10 seconds and conversation summaries every 30 seconds
- Local SQLite storage for transcripts, screen captures, summaries, and audio artifacts
- Full-text transcript search plus extensible multimodal (visual/audio) search

## Architecture Overview

```
Client (Web / Desktop)
    ↕ REST / WebSocket
FastAPI Backend
    ├─ Audio Service (capture, ASR, raw audio)
    ├─ Vision Service (screen capture, VLM analysis)
    ├─ Summarization Service (local LLM)
    ├─ Storage Service (SQLite + file system)
    ├─ Search Service (text + vector)
    └─ Scheduler Service (AnyIO-based periodic tasks)

Local Runtimes
    ├─ ASR Engine (Whisper.cpp, Vosk, Parakeet)
    ├─ VLM (Qwen2.5-VL 7B or similar)
    └─ LLM (Phi-3.5 Mini, Qwen 2.5 7B, etc.)
```

All data remains on-device. Background workers orchestrate capture, transcription, and summarization loops. Clients subscribe to updates via WebSocket for near-real-time insights.

## Project Structure

```
src/app/
    core/              # Settings, dependencies, error handlers
    db/                # SQLAlchemy async engine setup
    models/            # Meetings, transcripts, screen captures, summaries, audio
    routers/           # Versioned API modules
    services/          # Audio, vision, summarization, storage, search, scheduler
    main.py            # FastAPI application factory
```

Key routers to implement:
- `audio`: WebSocket endpoint for live chunks, REST endpoint for raw audio upload
- `vision`: REST endpoint to trigger screen capture or describe stored images
- `summaries`: REST/WebSocket to fetch latest summaries
- `search`: Full-text and multimodal query endpoints
- `meetings`: CRUD operations for meeting lifecycle

## Scheduling Cadence

| Task | Interval | Service |
|------|----------|---------|
| Live transcription | 2 s | AudioService + SchedulerService |
| Screen capture + VLM | 5 s | VisionService + SchedulerService |
| Relevant summary | 10 s | SummarizationService (kind="relevant") |
| Conversation summary | 30 s | SummarizationService (kind="rolling") |

Use `SchedulerService` with AnyIO task group to orchestrate these cycles per active meeting.

## Integrations

### ASR (Audio)
- **NVIDIA Parakeet TDT 0.6B V2** (ONNX, TensorRT) for streaming
- **Whisper.cpp** (C++ backend with Python bindings) for CPU-friendly transcription
- **Vosk** (Kaldi-based) for lightweight offline support

### Summarization (LLM)
- **Phi-3.5 Mini**, **Qwen-2.5 7B** via llama.cpp or Ollama
- Ensure models are quantized to fit (e.g., 4-bit GGUF for CPU-bound devices)

### Vision (Screen Capture + VLM)
- **Qwen2.5-VL 7B** via vLLM/llama.cpp integration
- For screen capture: `mss` (cross-platform), `pyautogui`, or platform-specific APIs wrapped in backends

### Vector & Search
- **FAISS**, **LanceDB**, or **Milvus Lite** for local vector similarity on screen embeddings
- SQLite FTS5 for transcript full-text search

## Installation

```bash
poetry install
```

Optional: install dev tools `poetry install --with dev`.

## Running Locally

```bash
poetry run uvicorn app.main:create_app --factory --reload
```

Use `.env` to configure model paths, device selection (CPU/GPU), and storage directories.

## Model & Runtime Setup

- Download GGUF/GGML quantized models into a local `models/` directory
- Configure llama.cpp/Ollama runtimes for LLM + VLM models
- Install ASR runtimes (Whisper.cpp binaries, CUDA/TensorRT if using Parakeet)
- Provide screen capture backend configuration per OS (Windows: `mss`, Mac: `pyobjc` with `Quartz`)

## Frontend Recommendations

- **Web App**: React/Vite + Tailwind talking to REST/WebSocket; easiest cross-platform
- **Desktop**: Tauri (Rust/WebView) or Electron, reusing web frontend; ensures Windows & macOS distribution
- Provide local WebSocket stream visualizing live transcripts and summaries; audio capture handled by native layer feeding backend endpoints

## Post-Meeting Pipeline

1. Stop live capture and finalize meeting session
2. Trigger `AudioService.post_process_audio` with the full raw recording for higher-accuracy transcription
3. Re-run summarization with full transcript for final summary artifacts
4. Persist refined summaries and transcripts for future search queries

## Roadmap

- Implement multimodal search index (FAISS/LanceDB integration)
- Build plugin architecture for additional capture modalities (e.g., whiteboard OCR)
- Add automated diarization and speaker labeling
- Develop local dashboard UI with session timeline visualization
- Provide export templates (Markdown, CSV, Notion, Jira)

## Contributing

1. Create a feature branch
2. Install dev dependencies (`poetry install --with dev`)
3. Run `flake8`, `black`, `isort`, and `pytest`
4. Open a pull request with context and testing notes

## License

MIT License