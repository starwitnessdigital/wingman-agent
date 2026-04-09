# Wingman 🤝🏳️‍🌈

**Your gay best friend who gives it to you straight.**

An AI dating coach and safety companion built specifically for gay men. Wingman helps with openers that actually work, profile rewrites, red flag detection, sextortion warnings, meetup safety, and honest "is he into me or just bored?" assessments.

**Privacy-first. Zero data stored. No judgment.**

---

## What Wingman does

### 💬 Conversation Coach
- Generates openers that get responses (never "hey")
- "What do I say next?" with context-aware suggestions
- Natural escalation toward meetups
- Tone matching (casual hookup vs. dating vs. friendship)
- Conversation recovery when things go sideways

### ✏️ Profile Optimizer
- Bio rewrites tailored to each platform (Grindr ≠ Hinge ≠ Scruff)
- Photo selection and ordering advice
- Platform-specific strategy and unwritten rules

### 🛡️ Safety Companion
- Red flag analysis on conversations
- Catfish risk scoring
- **Sextortion warning detection** — early pressure for explicit content, no-video-verify patterns, blackmail setup identification
- Meetup safety checklists with check-in schedules
- Exit strategies for uncomfortable situations

### 🔍 Vibe Check
- Message decoder: "He said X, what does that mean?"
- Compatibility analysis
- Ghosting probability assessment
- Honest "is he interested or just bored?" read

---

## Tech stack

- **Python** with `anthropic` SDK (tool_use agent loop)
- **FastAPI** for the web server
- **Claude Opus 4.6** via Anthropic API
- Zero conversation storage — all processing ephemeral

---

## Privacy architecture

```
User message → RAM (session only) → Anthropic API → Response
                    ↓
              Cleared on:
              - Session TTL expiry (default 30 min)
              - Explicit /session/{id} DELETE
              - Server restart
              
              Never written to:
              - Database
              - Disk
              - Logs
              - Analytics
```

See [privacy_policy.md](privacy_policy.md) for the full policy.

---

## Setup

### Prerequisites
- Python 3.11+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Installation

```bash
git clone https://github.com/starwitnessdigital/wingman-agent
cd wingman-agent

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run CLI

```bash
python main.py
```

### Run Web Server

```bash
python server.py
# Open http://localhost:8000
```

### Run Demo

```bash
# Full demo (all features)
python demo.py

# Specific feature
python demo.py --feature opener
python demo.py --feature safety
python demo.py --feature sextortion
python demo.py --feature vibe
python demo.py --feature profile
python demo.py --feature escalate
python demo.py --feature decode
python demo.py --feature meetup
```

---

## Project structure

```
wingman-agent/
├── main.py                    # Agent loop (tool_use)
├── server.py                  # FastAPI server
├── demo.py                    # Feature demos
├── tools/
│   ├── __init__.py            # Tool registry
│   ├── conversation_coach.py  # Openers, responses, escalation
│   ├── profile_optimizer.py   # Bio rewrites, photo advice
│   ├── safety_companion.py    # Red flags, catfish, sextortion, safety
│   └── vibe_check.py          # Decoder, compatibility, ghosting
├── prompts/
│   └── system_prompt.txt      # Wingman's persona
├── web/
│   └── index.html             # Chat interface
├── privacy_policy.md          # Plain-English privacy policy
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Send a message, get a response |
| `GET` | `/session/{id}` | Get session info (no content) |
| `DELETE` | `/session/{id}` | Clear a session immediately |
| `GET` | `/health` | Health check |
| `GET` | `/privacy` | Privacy summary |

### Chat request

```json
POST /chat
{
  "message": "Write me an opener for this Grindr profile...",
  "session_id": "optional-existing-session-id"
}
```

### Chat response

```json
{
  "response": "Okay, here are three openers that'll actually get a reply...",
  "session_id": "uuid-for-this-session"
}
```

---

## Pricing

- **Free tier:** 5 queries/day, no account required
- **Full access:** $9.99/month, unlimited queries

---

## The philosophy

Built by a gay man who has used Grindr, Scruff, Hinge, and all the rest. Wingman understands that hookup culture is valid, that "discreet" has a specific meaning on these apps, that asking for face pics is just practical, and that sometimes you need help navigating a conversation at 11pm without being lectured about it.

Warm but honest. Never preachy. Understands the culture. Sex-positive. Uses community language naturally.

---

## Contributing

PRs welcome. Please keep contributions in the spirit of the project — useful, honest, community-aware, and privacy-respecting.

---

*If you're in danger, contact emergency services. If you're struggling, the Trevor Project is at 1-866-488-7386 or TheTrevorProject.org.*
