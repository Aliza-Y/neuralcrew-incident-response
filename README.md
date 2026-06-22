# 🚨 NeuralCrew — Enterprise AI Incident Response System

> **Band of Agents Hackathon 2026 · Track 1: Internal Enterprise Workflows**

NeuralCrew deploys 4 AI agents on Band SDK to automate enterprise incident response. Triage classifies, Technical investigates, Comms drafts updates, Resolution closes with post-mortem. Reduces MTTR from 30+ minutes to under 2 minutes automatically.

---

## 👥 Team

| Name | Band Handle | Role |
|---|---|---|
| Laiba Idrees | @laiba.idrees2003 | Triage Agent · Technical Agent |
| Aliza Yousaf | @yousaffaliza | Comms Agent · Resolution Agent |

---

## 🎯 The Problem

When production goes down, chaos follows:

- ⏱ **30+ minutes** of phone calls and Slack messages before anyone knows what's wrong
- 👥 **4–6 people** woken up to do tasks that follow a predictable pattern every time
- 📄 **No audit trail** — decisions made in WhatsApp groups, post-mortems written from memory days later
- 💸 **Revenue loss** every single minute the system stays down

Every enterprise with a production system faces this. NeuralCrew solves it.

---

## 💡 Our Solution

NeuralCrew is a **multi-agent incident response pipeline** where four specialized AI agents collaborate through Band in real time. One human types the incident. The agents handle everything else.

```
Human reports incident
        ↓
  🔴 Triage Agent    →  Classifies severity (P0–P3), identifies impact
        ↓
  🔧 Technical Agent →  Root cause analysis, diagnostic steps, fix proposal
        ↓
  📢 Comms Agent     →  Internal engineering brief + External customer update
        ↓
  ✅ Resolution Agent →  Post-mortem report, prevention steps, INCIDENT CLOSED
```

---

## 🏗️ Architecture

### Tech Stack

| Technology | Role |
|---|---|
| **Band SDK** (band-sdk 1.0.0) | Multi-agent collaboration layer — WebSocket routing, @mention task delegation, audit trail |
| **LangGraph** | Agent framework — structured reasoning with tool-calling capability |
| **OpenAI GPT-4o-mini** | LLM powering all 4 agents via COMSATS University API |
| **Python 3.11 + AsyncIO** | Runtime — all 4 agents run concurrently via `asyncio.gather()` |
| **python-dotenv** | Secure API key and config management |

### Agent Details

| Agent | Owner | Framework | Responsibility |
|---|---|---|---|
| **Triage** | @laiba.idrees2003/triage | LangGraph + OpenAI | Classifies P0/P1/P2/P3, extracts incident details, routes to Technical |
| **Technical** | @laiba.idrees2003/technical | LangGraph + OpenAI | Root cause hypothesis, 5 diagnostic steps, recommended fix, risk level |
| **Comms** | @yousaffaliza/comms | LangGraph + OpenAI | Dual communication: internal ops briefing + external customer status update |
| **Resolution** | @yousaffaliza/resolution | LangGraph + OpenAI | Post-mortem report, timeline, prevention steps, closes incident with timestamp |

---

## 📁 Project Structure

```
Band_Of_Agents/
├── agents/
│   ├── triage_agent.py       # P0-P3 classification + @Technical handoff
│   ├── technical_agent.py    # Root cause analysis + @Comms handoff
│   ├── comms_agent.py        # Internal + External communications + @Resolution handoff
│   └── resolution_agent.py   # Post-mortem + INCIDENT CLOSED
├── run_all.py                # Launches all 4 agents concurrently
├── agent_config.yaml         # Band agent IDs and API keys (gitignored)
├── .env                      # Environment variables (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- A Band account at [app.band.ai](https://app.band.ai)
- OpenAI API key
- 4 agents registered in Band as "Connect Remote Agent" (External Agent)

### 1. Clone the repository

```bash
git clone https://github.com/Aliza-Y/neuralcrew-incident-response.git
cd neuralcrew-incident-response
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 5. Configure Band agent credentials

Create an `agent_config.yaml` file in the root directory:

```yaml
triage:
  agent_id: "your-triage-agent-uuid"
  api_key: "your-triage-api-key"

technical:
  agent_id: "your-technical-agent-uuid"
  api_key: "your-technical-api-key"

comms:
  agent_id: "your-comms-agent-uuid"
  api_key: "your-comms-api-key"

resolution:
  agent_id: "your-resolution-agent-uuid"
  api_key: "your-resolution-api-key"
```

> **Note:** Get these values from your Band dashboard → Agents → each agent's settings page.

### 6. Run all agents

```bash
python run_all.py
```

You should see all 4 agents connect and print their status:

```
Triage Agent is live!
Technical Agent is live!
Comms Agent is live!
Resolution Agent is live!
```

---

## 🚀 How to Trigger a Demo

Once all agents are running, go to your Band chat room and type:

```
@laiba.idrees2003/triage INCIDENT: Production API returning 503 errors. 
2000 users cannot access the application. Revenue loss $5000/minute. 
Started 10 minutes ago. No recent deployments.
```

### What happens next:

1. **Triage Agent** responds automatically with P0/P1 classification and hands off to @Technical
2. **Technical Agent** responds with full root cause analysis and hands off to @Comms
3. **Comms Agent** posts internal + external status updates and hands off to @Resolution
4. **Resolution Agent** writes the post-mortem and closes the incident with a timestamp

**Total time: under 2 minutes.**

---

## 📋 Requirements

```
band-sdk[langgraph]
langchain-openai
langchain
langchain-core
langgraph
python-dotenv
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🔄 Full Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    BAND CHAT ROOM                        │
│                                                          │
│  Human: @triage INCIDENT: [description]                  │
│                          │                               │
│              ┌───────────▼────────────┐                  │
│              │     TRIAGE AGENT        │                  │
│              │  • Severity: P0/P1/P2/P3│                  │
│              │  • Category             │                  │
│              │  • Impact               │                  │
│              │  • Immediate Action     │                  │
│              └───────────┬────────────┘                  │
│                          │ @Technical                    │
│              ┌───────────▼────────────┐                  │
│              │    TECHNICAL AGENT      │                  │
│              │  • Root Cause Analysis  │                  │
│              │  • 5 Diagnostic Steps   │                  │
│              │  • Recommended Fix      │                  │
│              │  • Risk Level           │                  │
│              └───────────┬────────────┘                  │
│                          │ @Comms                        │
│              ┌───────────▼────────────┐                  │
│              │      COMMS AGENT        │                  │
│              │  • Internal Update      │                  │
│              │  • External Status Page │                  │
│              └───────────┬────────────┘                  │
│                          │ @Resolution                   │
│              ┌───────────▼────────────┐                  │
│              │    RESOLUTION AGENT     │                  │
│              │  • Post-Mortem Report   │                  │
│              │  • Prevention Steps x3  │                  │
│              │  • INCIDENT CLOSED ✓    │                  │
│              └────────────────────────┘                  │
│                                                          │
│  Full audit trail permanently logged in this room ✓      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Target Audience

- **Mid-to-large enterprises** with 24/7 production systems and SLA obligations
- **Engineering & DevOps teams** tired of 3 AM incident calls
- **Compliance-heavy industries** (finance, healthcare, legal) needing documented audit trails
- **SaaS & e-commerce companies** where downtime directly equals revenue loss
- **CTOs and IT Managers** looking to reduce operational costs with AI automation

---

## 🔮 Future Scope

| Phase | What's Next |
|---|---|
| **Phase 1** | Connect to PagerDuty / Datadog for automatic incident triggers |
| **Phase 2** | Slack & Teams notifications, Jira ticket creation, Confluence post-mortem publishing |
| **Phase 3** | ML-based incident pattern recognition and predictive alerting |
| **Phase 4** | Cloud deployment on AWS Lambda / GCP Cloud Run for 24/7 always-on response |

---

## ⚠️ Known Limitations

During the hackathon build, we identified one architectural challenge worth noting:

**LangGraph thread state vs Band dynamic room routing:** LangGraph's `InMemorySaver` creates persistent thread state per room. When multiple messages arrive rapidly (e.g. retries), this can cause the Comms and Resolution agents to receive duplicate messages and respond multiple times.

**Root cause:** Race condition between LangGraph's stateful thread management and Band's dynamic room-scoped WebSocket routing.

**Production fix:** Implement room-aware thread IDs in the LangGraph checkpointer + message deduplication middleware using idempotency keys.

This does not affect the core workflow — all 4 agents process and respond correctly. Triage → Technical run in a fully automated chain, with Comms and Resolution completing the pipeline.

---

## 📄 License

MIT License — feel free to build on this.

---

## 🙏 Acknowledgements

- [Band](https://band.ai) for the multi-agent collaboration SDK and hackathon
- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent framework
- [OpenAI](https://openai.com) for GPT-4o-mini


---

