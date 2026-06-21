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
| **Scout** | qwen2.5:0.5b (local) | Extract target, attacker IP, and action from raw alert text | — |
| **Investigator** | qwen2.5:0.5b (local) | Diagnose the attack + cite the matching CVE | `cve_database.json` (15 entries) |
| **Impact** | llama3:8b (local) or llama-3.3-70b (Groq) | Map the event to a corporate asset + assess business risk | `asset_inventory.json` (15 assets) |
| **Commander** | llama3:8b (local) or llama-3.3-70b (Groq) | Generate executive headline + 3 grounded action items | `playbooks.json` (16 playbooks) |

The pipeline runs end-to-end in **~25 seconds** with local LLMs, or **~5 seconds** when the Groq cloud fallback kicks in.

---

## The Three Differentiators

When you feed in a raw alert like *"Unauthorized database access attempt via Apache Struts on port 8080 from IP 198.51.100.42"*, the system produces a brief containing facts that **weren't in the original alert**:

1. **CVE number** — The Investigator looks up the software name in `cve_database.json` and returns `CVE-2026-0001, CVSS 9.8, OGNL injection`. That CVE number came from your local database, not the LLM's memory.

2. **Affected asset + record count** — The Impact agent looks up port 8080 in `asset_inventory.json` and returns *"Production Struts Gateway, Payments Gateway segment, 5M records at risk"*. Neither the asset name nor the record count appeared in the raw alert.

3. **Action items** — The Commander pulls 3 specific actions from `playbooks.json` based on the severity. These aren't hallucinated — they're verbatim from your company's incident response handbook.

Every fact in the Decision Brief traces back to a source. That's what makes this a Decision Intelligence Platform, not an LLM wrapper.

---

## Quick Start

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) running locally
- A free [Groq API key](https://console.groq.com) (fallback when local Ollama times out)

### Install

```bash
git clone <your-repo-url>
cd decision_platform
python -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### Pull the LLMs

```bash
ollama pull qwen2.5:0.5b    # for Scout + Investigator (~400 MB)
ollama pull llama3:8b        # for Impact + Commander (~4.7 GB)
```

### Configure Environment

Create a `.env` file in the project root:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=llama-3.3-70b-versatile
```

### Run the Pipeline

```bash
# Run a random alert from the 50-alert sample
python test_pipeline.py

# Run a specific alert
python test_pipeline.py alert-001

# Run 5 random alerts
python test_pipeline.py --random 5

# Run all 50 alerts (full regression — takes ~20 min)
python test_pipeline.py --all
```

---

## Project Structure

```
decision_platform/
├── README.md                           # this file
├── test_pipeline.py                    # CLI test runner + run_pipeline() integration point
├── test_pipeline_mocked.py             # same pipeline, mocked LLMs (no Ollama required)
├── .env                                # your API keys (NEVER commit this)
│
├── shared/
│   └── data/
│       ├── cve_database.json           # 15 mock CVE entries
│       ├── asset_inventory.json        # 15 mock corporate assets
│       ├── playbooks.json              # 16 mock incident response playbooks
│       └── sample_alerts.json          # 50 demo alerts covering all severities
│
└── backend/
    ├── requirements.txt                # pydantic, httpx, python-dotenv, pytest
    └── app/
        ├── config.py                   # loads .env
        ├── agents/
        │   ├── base.py                 # JSON cleaning + retry-with-fallback helper
        │   ├── router.py               # LLM dispatcher (Ollama → Groq fallback)
        │   ├── prompts.py              # 4 agent system prompts
        │   ├── scout.py                # Agent 1: entity extraction
        │   ├── investigator.py         # Agent 2: CVE diagnosis
        │   ├── impact.py               # Agent 3: asset + business impact (WOW)
        │   └── commander.py            # Agent 4: executive action brief
        ├── tools/
        │   ├── cve_lookup.py           # lookup_cve(cve_id) → CVERecord
        │   ├── asset_lookup.py         # lookup_asset(ip, port) → AssetRecord
        │   └── playbook_lookup.py      # lookup_playbook(severity) → PlaybookResult
        └── models/
            └── schemas.py              # Pydantic models for all data shapes
```

---

## API Reference (for P3 — FastAPI integration)

The pipeline exposes one clean function. Import it, wrap it in FastAPI, done.

```python
from test_pipeline import run_pipeline
from backend.app.models.schemas import PipelineResults

# Run the full 4-agent pipeline on a raw alert string
results: PipelineResults = run_pipeline(raw_alert)
```

### `PipelineResults` Schema

```json
{
  "scout": {
    "target": "Apache Struts on 10.0.0.150:8080",
    "attacker_ip": "198.51.100.42",
    "action": "Apache Struts exploit"
  },
  "investigator": {
    "diagnosis": "RCE via CVE-2026-0001 due to improper HTTP Content-Type header validation in Apache Struts v4.2",
    "confidence_score": 92
  },
  "impact": {
    "severity": "CRITICAL",
    "affected_asset": "Production Struts Gateway",
    "potential_damage": "5M payment records at risk via OGNL injection."
  },
  "commander": {
    "summary_headline": "CRITICAL: RCE on Production Struts Gateway",
    "recommended_actions": [
      "Isolate affected servers immediately from the main VPC subnet.",
      "Engage Incident Command Team and initiate P0 communication channel.",
      "Patch or rotate service credentials for affected machines."
    ]
  }
}
```

### Individual Agent Functions (for SSE streaming between agents)

```python
from backend.app.agents.scout import scout_alert
from backend.app.agents.investigator import investigate_scout_output
from backend.app.agents.impact import assess_impact
from backend.app.agents.commander import generate_command

scout = scout_alert(raw_alert)                                    # → ScoutOutput
investigator = investigate_scout_output(scout)                    # → InvestigatorOutput
impact = assess_impact(scout, investigator, raw_alert)            # → ImpactOutput
commander = generate_command(investigator, impact)                # → CommanderOutput
```

Emit an SSE event between each call so the frontend can show real-time progress.

---

## Resilience Features

This pipeline is built to **never crash during a demo**.

| Feature | What it does |
|---------|--------------|
| **Ollama → Groq fallback** | If local Ollama times out (8s) or errors, automatically retries on Groq cloud |
| **JSON retry** | If an LLM returns malformed JSON, retry once with a stricter "return valid JSON" prompt |
| **Fallback responses** | If all retries fail, return a degraded-but-valid response so the pipeline continues |
| **Confidence cap** | Investigator confidence is capped at 95% in code (Qwen 0.5B ignores prompt rules) |
| **Port extraction fallback** | If Scout drops the port number, recover it from the original raw alert text |

---

## Tech Stack

- **Backend:** Python 3.11+, Pydantic v2, httpx
- **LLMs (local):** Ollama running Qwen 2.5 0.5B + Llama 3 8B
- **LLMs (cloud fallback):** Groq running Llama 3.3 70B
- **Frontend:** Next.js + Tailwind + Recharts (separate — see `frontend/`)
- **API:** FastAPI + Server-Sent Events (separate — see `backend/app/api/`)

No external AI APIs required for normal operation. The system runs end-to-end on a laptop.

---

## Demo Script (90 Seconds)

> *"Here's a raw alert — just chaotic text: port number, IP, no context. Watch what happens.*
>
> *Scout extracts the entities in 2 seconds. Investigator cross-references our local CVE database — this is CVE-2026-0001, Apache Struts RCE, CVSS 9.8, 92% confidence. That CVE number wasn't in the alert — the system looked it up.*
>
> *Impact maps the port to our corporate asset inventory — this is the Production Struts Gateway, 5 million records at risk in the Payments Gateway segment. The alert never said which server was under attack — the system figured it out.*
>
> *Commander issues three specific actions from our incident response playbook. These aren't generic — they came from our approved playbook database.*
>
> *Total time: 25 seconds. From noise to decision."*

---

## Sample Alerts

`shared/data/sample_alerts.json` contains 50 demo alerts covering:

- **CRITICAL:** Apache Struts RCE, ransomware, Kafka deserialization, PostgreSQL access, auth bypass
- **HIGH:** SQL injection, K8s privilege escalation, Redis exposure, OAuth misconfiguration, credential stuffing
- **MEDIUM:** XSS, path traversal, Nginx traversal
- **LOW:** Port scans, certificate expiry

Run any of them with `python test_pipeline.py alert-XXX`.

---

## Team

Built at a 24-hour hackathon by a 4-person squad:

- **Person 1** — AI Engineer (agents, prompts, LLM routing)
- **Person 2** — Integration Engineer (mock databases, lookup tools)
- **Person 3** — Bridge/Pipeline (FastAPI, SSE, orchestration)
- **Person 4** — Frontend (Next.js dashboard, real-time UI)
