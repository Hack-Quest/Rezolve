# Decision Intelligence Platform

**From raw security alert to one-page action plan — in seconds.**

Most AI security tools are just summarizers: feed them a noisy alert, get a shorter description of the same alert. They answer *"what happened?"* but never *"what do we do right now?"*

This platform is different. A four-agent pipeline runs locally on your machine, with each agent grounded in a real (mock) corporate database. The output isn't a summary — it's a **Decision Brief** containing the affected asset name, business risk, and three specific actions to take.

The wow: facts in the Decision Brief that **never appeared in the raw alert** — synthesized by the agents cross-referencing internal databases.

---

## How It Works

```
RAW ALERT  →  SCOUT        →  INVESTIGATOR  →  IMPACT       →  COMMANDER  →  DECISION BRIEF
              extracts        looks up         looks up        looks up
              the facts       the CVE          the asset       the playbook
                                ↓                ↓              ↓
                            cve_database    asset_inventory   playbooks
                              .json           .json            .json
```

| Agent | Model | Job | Database |
|-------|-------|-----|----------|
| **Scout** | gemma3:1b (local) | Extract target, attacker IP, and action from raw alert text | — |
| **Investigator** | gemma3:1b (local) | Diagnose the attack + cite the matching CVE | `cve_database.json` (15 entries) |
| **Impact** | llama3.2:3b (local) or llama-3.3-70b (Groq) | Map the event to a corporate asset + assess business risk | `asset_inventory.json` (15 assets) |
| **Commander** | llama3.2:3b (local) or llama-3.3-70b (Groq) | Generate executive headline + 3 grounded action items | `playbooks.json` (16 playbooks) |

Actual pipeline time depends on your hardware. The backend pre-loads `llama3.2:3b` into Ollama in the background the moment a run starts (in parallel with Scout + Investigator), so Impact and Commander usually find it already warm by the time they need it — see [Model Warm-Up](#model-warm-up) below. Falls back to Groq automatically if Ollama is slow or unavailable.

---

## The Three Differentiators

When you feed in a raw alert like *"Unauthorized database access attempt via Apache Struts on port 8080 from IP 198.51.100.42"*, the system produces a brief containing facts that **weren't in the original alert**:

1. **CVE number** — The Investigator looks up the software name in `cve_database.json` and returns the matching CVE, CVSS score, and attack type. That number came from your local database, not the LLM's memory. (If the model's own answer omits the CVE ID despite the prompt instructing it to cite one, the code appends it automatically from the matched record — see [Resilience Features](#resilience-features).)

2. **Affected asset + record count** — The Impact agent looks up the port in `asset_inventory.json` and returns the real asset name, network segment, and what's at risk. Neither appeared in the raw alert.

3. **Action items** — The Commander pulls 3 specific actions from `playbooks.json` based on severity. These aren't hallucinated — they're verbatim from your company's incident response handbook.

Every fact in the Decision Brief traces back to a source. That's what makes this a Decision Intelligence Platform, not an LLM wrapper.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for the frontend)
- [Ollama](https://ollama.com) running locally
- A free [Groq API key](https://console.groq.com) (fallback when local Ollama is slow or down)

### Install

```bash
git clone <your-repo-url>
cd Rezolve
python -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### Pull the LLMs

```bash
ollama pull gemma3:1b      # for Scout + Investigator (~800 MB)
ollama pull llama3.2:3b    # for Impact + Commander (~2 GB)
```

### Configure Environment

Copy `.env.example` to `.env` in the project root and fill in your Groq key:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=llama-3.3-70b-versatile
```

`OLLAMA_MODEL` is the fallback default for any agent not explicitly listed in `OLLAMA_MODEL_MAPPING` (see `backend/app/agents/router.py`) — Scout/Investigator/Impact/Commander each have an explicit entry there already, so you normally won't need to touch this.

---

## Running It

There are three ways to run the pipeline, from quickest-to-check to full-demo:

### 1. CLI — fastest way to sanity-check the agents

```bash
python test_pipeline.py                 # one random alert
python test_pipeline.py alert-001       # a specific alert
python test_pipeline.py --random 5      # 5 random alerts, no repeats
python test_pipeline.py --all           # full 50-alert regression
```

No server needed — this talks straight to Ollama/Groq and prints the Decision Brief to your terminal.

### 2. Live server — what the demo actually runs on

```bash
# from the project root
uvicorn backend.app.main:app --reload --port 8000
```

Then in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173/` for the landing page, or `http://localhost:5173/demo` to go straight to the live SOC dashboard. The frontend streams real agent output over Server-Sent Events — nothing in `/demo` is simulated or pre-timed.

### 3. Smoke test — verify the live server end-to-end

With the server from step 2 already running:

```bash
python smoke_test.py                    # alert-001, full test suite
python smoke_test.py alert-003          # different alert
python smoke_test.py --no-stream        # fast check, skip the slow SSE test
python smoke_test.py --verbose          # print full JSON of every response
```

This hits every endpoint, validates the full 10-event SSE sequence, checks all four agents' output schemas, and specifically verifies the three "wow moments" (CVE cited, real asset matched, three concrete actions) actually fired — not just that the pipeline didn't crash. Run this before every demo.

---

## Project Structure

```
Rezolve/
├── README.md                           # this file
├── .env.example                        # template for your .env (never commit the real one)
├── test_pipeline.py                    # CLI test runner
├── test_pipeline_mock.py               # same pipeline, mocked LLMs (no Ollama required)
├── smoke_test.py                       # end-to-end test of the LIVE server (see above)
│
├── shared/
│   └── data/
│       ├── cve_database.json           # 15 mock CVE entries
│       ├── asset_inventory.json        # 15 mock corporate assets
│       ├── playbooks.json              # 16 mock incident response playbooks
│       └── sample_alerts.json          # 50 demo alerts covering all severities
│
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py                     # FastAPI entrypoint — see API Reference below
│       ├── config.py                   # loads .env
│       ├── api/
│       │   └── sse.py                  # SSE streaming wrapper around the 4 agents
│       ├── agents/
│       │   ├── base.py                 # JSON cleaning + retry-with-fallback helper
│       │   ├── router.py               # LLM dispatcher (Ollama → Groq fallback)
│       │   ├── warmup.py               # background model pre-loading — see below
│       │   ├── prompts.py              # 4 agent system prompts
│       │   ├── scout.py                # Agent 1: entity extraction
│       │   ├── investigator.py         # Agent 2: CVE diagnosis
│       │   ├── impact.py               # Agent 3: asset + business impact (WOW)
│       │   └── commander.py            # Agent 4: executive action brief
│       ├── tools/
│       │   ├── cve_lookup.py           # lookup_cve(cve_id) → CVERecord
│       │   ├── asset_lookup.py         # lookup_asset(ip, port) → AssetRecord
│       │   └── playbook_lookup.py      # lookup_playbook(severity) → PlaybookResult
│       └── models/
│           ├── schemas.py              # Pydantic models for all data shapes
│           └── store.py                # in-memory alert store (no database)
│
└── frontend/                           # Vite + React + Tailwind
    ├── package.json
    └── src/
        ├── App.jsx                     # routes: "/" landing, "/demo" live dashboard
        ├── hooks/
        │   └── useSSEPipeline.js       # opens /api/stream, turns events into React state
        └── components/
            ├── LandingPage.jsx
            ├── page.jsx                 # the live demo screen
            ├── RawLogFeed.jsx           # column 1 — raw alert
            ├── AgentPipeline.jsx        # column 2 — 4 agents lighting up in real time
            ├── ExecutiveBrief.jsx       # column 3 — the Decision Brief
            ├── Header.jsx
            └── Footer.jsx
```

---

## API Reference

`backend/app/main.py` exposes:

| Endpoint | Description |
|----------|--------------|
| `GET /api/health` | `{"ok": true}` — liveness check |
| `GET /api/alerts` | List every alert currently in the in-memory store, with `pipeline_results` if it's been run |
| `GET /api/alerts/{alert_id}` | One alert by id. 404 if unknown |
| `GET /api/stream?alert_id=alert-001` | Replay a pre-seeded sample alert through the live SSE pipeline |
| `GET /api/stream?raw_alert=...` | Run free-text input through the same pipeline (not persisted — no stable id to key on) |

`/api/stream` is GET-only because the browser's native `EventSource` can't send a request body. Event sequence on the stream:

```
pipeline_start → agent_start(scout) → agent_complete(scout)
               → agent_start(investigator) → agent_complete(investigator)
               → agent_start(impact) → agent_complete(impact)
               → agent_start(commander) → agent_complete(commander)
               → pipeline_complete
```

(`pipeline_error` instead of `pipeline_complete` if something throws — the stream always closes cleanly either way, it never hangs.)

For direct Python integration without the HTTP layer:

```python
from backend.app.agents.scout import scout_alert
from backend.app.agents.investigator import investigate_scout_output
from backend.app.agents.impact import assess_impact
from backend.app.agents.commander import generate_command

scout = scout_alert(raw_alert)                                    # → ScoutOutput
investigator = investigate_scout_output(scout)                    # → InvestigatorOutput
impact = assess_impact(scout, investigator, raw_alert)             # → ImpactOutput
commander = generate_command(investigator, impact)                 # → CommanderOutput
```

---

## Model Warm-Up

Scout and Investigator run on a small model (`gemma3:1b`); Impact and Commander need a larger one (`llama3.2:3b`). Ollama only loads a model into memory once it's first requested, and on constrained hardware loading the larger model can evict the smaller one that was just used — which would otherwise mean Impact eats a cold-load delay on every single run.

`backend/app/agents/warmup.py` fixes this: the moment a pipeline run starts, it fires an empty-prompt request for `llama3.2:3b` in a background thread, in parallel with Scout and Investigator. By the time Impact actually needs the model, it's usually already warm. Even if Impact's own request still has to wait, the background load keeps running independently — so by the time Commander's turn comes, moments later, the model is reliably resident. `keep_alive` is set to 30 minutes on every big-model request so it doesn't get evicted between Impact and Commander, or between one demo alert and the next.

This also runs once at server startup (`main.py`'s `lifespan` handler), blocking until the model is warm — so the *first* alert of a live demo isn't the one that eats a cold-load penalty in front of judges.

If you're running on hardware with enough VRAM/RAM to hold both models at once, set `OLLAMA_MAX_LOADED_MODELS=2` when starting Ollama to remove the eviction risk entirely.

---

## Resilience Features

This pipeline is built to **never crash during a demo**.

| Feature | What it does |
|---------|--------------|
| **Ollama → Groq fallback** | If local Ollama is slow (10s) or errors, automatically retries on Groq cloud |
| **Model warm-up** | Big model pre-loads in the background so Impact/Commander rarely hit a cold start — see above |
| **JSON retry** | If an LLM returns malformed JSON, retry once with a stricter "return valid JSON" prompt |
| **Fallback responses** | If all retries fail, return a degraded-but-valid response so the pipeline continues |
| **Confidence cap** | Investigator confidence is capped at 95% in code (small models tend to ignore that prompt rule) |
| **CVE citation enforcement** | If the model's diagnosis omits the CVE ID despite the prompt rule, the matched CVE record is appended automatically — protects the #1 "wow moment" from silent model non-compliance |
| **Port extraction fallback** | If Scout drops the port number, recover it from the original raw alert text |
| **Stream-safe error handling** | A failed agent emits `pipeline_error` over SSE instead of crashing the connection — the frontend shows an error state, it never hangs |

---

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Pydantic v2, httpx
- **LLMs (local):** Ollama running Gemma 3 1B + Llama 3.2 3B
- **LLMs (cloud fallback):** Groq running Llama 3.3 70B
- **Frontend:** Vite + React 19 + Tailwind CSS v4 + Framer Motion + React Router
- **Realtime:** Server-Sent Events (`EventSource` in the browser, `StreamingResponse` in FastAPI) — no WebSocket, no polling

No external AI APIs are required for normal operation. The system runs end-to-end on a laptop, with Groq purely as a fallback for when local inference is too slow or unavailable.

---

## Sample Alerts

`shared/data/sample_alerts.json` contains 50 demo alerts covering:

- **CRITICAL:** Apache Struts RCE, ransomware, Kafka deserialization, PostgreSQL access, auth bypass
- **HIGH:** SQL injection, K8s privilege escalation, Redis exposure, OAuth misconfiguration, credential stuffing
- **MEDIUM:** XSS, path traversal, Nginx traversal
- **LOW:** Port scans, certificate expiry

Run any of them with `python test_pipeline.py alert-XXX`, or pick one from the dropdown on the live `/demo` dashboard.

---

## Team

Built by **Team HACKOPS**:

Anshika Khare · Animesh Mudit · Anshuman Awasthi · Anshika