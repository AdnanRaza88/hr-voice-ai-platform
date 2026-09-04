# HR Voice AI Platform

Local-first multi-agent platform for HR screening, knowledge retrieval, and meeting minutes.

## Current foundation

- Flexible LLM providers: **Groq**, **OpenAI**, **OpenCode Zen**, **Ollama**
- Provider select + API key save via API (`/api/providers`)
- Agentic RAG (Chroma + HuggingFace embeddings)
- Screening conversation flow
- Minutes of Meeting generation
- Light frosty web UI
- FastAPI backend

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set at least one provider key.

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000`

## Provider API

- `GET /api/providers` — status
- `POST /api/providers` — save provider + keys
- `POST /api/providers/test` — live test

OpenCode Zen example:

```json
{"llm_provider":"opencode_zen","opencode_api_key":"your-key","opencode_model":"big-pickle"}
```

## Roadmap

1. Auth (JWT + department join codes)
2. Agentic RAG multi-agent chunking + Graphify-style knowledge graph
3. Employee / Admin panels + tasks
4. Multi-agent MOM
5. Voice / TTS

Repo: https://github.com/AdnanRaza88/hr-voice-ai-platform
