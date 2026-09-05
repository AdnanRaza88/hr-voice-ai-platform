# Build phases and tech stack

## Tech stack tags

| Tag | Choice | Notes |
|-----|--------|--------|
| `backend` | FastAPI | REST + later websockets |
| `agents` | LangGraph + LangChain | Stateful graphs |
| `llm` | Groq / OpenAI / OpenCode Zen / Ollama | User-selectable |
| `graph` | **Graphify full** | Agent memory + structured KG (not RAG) |
| `rag` | Multi-agent chunking + **FAISS** | Separate from Graphify |
| `db` | **SQLite** | Users, depts, tasks; metadata for FAISS |
| `vector` | FAISS (primary) | Optional pgvector later if Postgres |
| `auth` | JWT + department join codes | No Google OAuth for local first |
| `ui` | Light liquid-glass | Vanilla / minimal JS |
| `voice` | gTTS + stronger STT/TTS | Phase 4 |
| `embeddings` | HuggingFace sentence-transformers | Offline-capable |

---

## Phase 0 — Foundation (current)

- [x] FastAPI app skeleton
- [x] Multi-provider LLM factory (`src/core/llm.py`)
- [x] Provider status / save / test API
- [x] Basic RAG path (loader → chunk → vector → answer)
- [x] Screening flow (single agent style)
- [x] MOM text generation
- [x] Light UI shell
- [ ] Push remaining routes + UI to GitHub
- [ ] README / run path verified end-to-end

**Stack:** `backend` `llm` `rag` `ui`

---

## Phase 1 — Auth + data

- [ ] SQLite schema: users, departments, join_codes, sessions
- [ ] JWT issue / verify middleware
- [ ] Department join-code signup (classroom-style)
- [ ] Admin/HR vs Employee permission split
- [ ] Settings UI: provider select + API key save + test

**Stack:** `auth` `db` `ui` `backend`

---

## Phase 2 — Agentic RAG + Graphify (full)

### RAG (vector path)
- [ ] 5 chunking agents (planner, splitter, critic, embedder, indexer)
- [ ] Switch store to **FAISS** (+ SQLite for file/chunk metadata)
- [ ] High retrieval quality
- [ ] Employee privacy chat widget only

### Graphify (graph path — full power)
- [ ] Install/integrate graphifyy as project tool
- [ ] Build graph over policies, agent contracts, org docs
- [ ] Agents query graph for structured memory
- [ ] Persist graph.json / reports under project data

**Rule:** Graphify is not a light add-on. Agentic system uses it as primary structured memory. RAG remains the separate FAISS path for fuzzy doc Q&A.

**Stack:** `graph` `rag` `vector` `agents` `embeddings`

---

## Phase 3 — Multi-agent MOM

- [ ] Transcript ingest
- [ ] Speaker identification
- [ ] Transcript enhance / correct
- [ ] Key points + action items + owners
- [ ] End-of-meeting summary distribution

**Stack:** `agents` `backend` `ui`

---

## Phase 4 — Voice

- [ ] STT pipeline
- [ ] TTS (gTTS baseline → stronger module)
- [ ] Screening over voice session

**Stack:** `voice` `agents` `backend`

---

## Phase 5 — Employees / tasks

- [ ] Levels, departments, deadlines
- [ ] Task assignment from HR
- [ ] Per-department sessions

**Stack:** `db` `ui` `agents`
