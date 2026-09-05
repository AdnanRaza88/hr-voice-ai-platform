# HR Voice AI Platform

Local-first multi-agent HR platform: screening, knowledge RAG, meeting minutes, employee panels, and voice.

**Repo:** https://github.com/AdnanRaza88/hr-voice-ai-platform

---

## Can it run right now?

**Yes — foundation is runnable** if you have Python 3.11+ and at least one LLM API key.

**Works today**
- FastAPI app + light UI
- Multi-provider LLM (Groq / OpenAI / OpenCode Zen / Ollama)
- Basic RAG (ingest + ask)
- Screening Q&A flow
- MOM from transcript text

**Not ready yet**
- Full Graphify agent memory layer
- Multi-agent chunking (5 agents)
- JWT + department join-code auth
- Admin / Employee panels
- Live multi-agent MOM
- Full voice / TTS call layer

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/AdnanRaza88/hr-voice-ai-platform.git
cd hr-voice-ai-platform

# 2. Virtual env
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install
pip install -r requirements.txt

# 4. Env
cp .env.example .env
```

Edit `.env` and set **one** provider key:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
```

Or OpenCode Zen:

```env
LLM_PROVIDER=opencode_zen
OPENCODE_API_KEY=your_key_here
OPENCODE_MODEL=big-pickle
OPENCODE_BASE_URL=https://opencode.ai/zen/v1
```

```bash
# 5. Run
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

| | |
|--|--|
| App | http://127.0.0.1:8000 |
| API docs | http://127.0.0.1:8000/docs |

---

## Architecture (locked)

| Layer | Role | Tech |
|--------|------|------|
| **Graphify** | Full agentic knowledge graph + agent memory | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache 2.0) |
| **RAG** | Separate document Q&A | Multi-agent chunking → **FAISS** + HF embeddings |
| **App DB** | Users, departments, tasks, sessions | **SQLite** (local) |
| **Orchestration** | Stateful agents | LangGraph + LangChain |
| **LLM** | User picks provider | Groq, OpenAI, OpenCode Zen, Ollama |
| **Voice** | STT / TTS | gTTS + stronger modules later |
| **UI** | Light liquid-glass | Vanilla HTML / CSS / JS |

**Rule:** Graphify is **not** RAG.  
Graphify = structured graph memory for the agentic system (full power).  
RAG = vector retrieval over policies/docs (FAISS + SQLite metadata).

---

## Provider API

```http
GET  /api/providers
POST /api/providers
POST /api/providers/test
```

```json
{
  "llm_provider": "opencode_zen",
  "opencode_api_key": "your-key",
  "opencode_model": "big-pickle"
}
```

---

## Phases

Full checklist: **[docs/PHASES.md](docs/PHASES.md)**

| Phase | Focus | Status |
|-------|--------|--------|
| **P0** | Foundation: providers, basic RAG, screening, MOM, UI shell | In progress |
| **P1** | JWT + department codes, SQLite, Admin/Employee | Next |
| **P2** | Agentic RAG (5 chunk agents) + FAISS + **Graphify full** | Planned |
| **P3** | Multi-agent MOM | Planned |
| **P4** | Voice layer | Planned |
| **P5** | Employee tasks / departments polish | Planned |

---

## Notes

- Local-first, open-source friendly stack
- Graphify Apache 2.0 — **full use** in this project
- No Google OAuth for local path (department join codes)
