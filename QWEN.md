# Personal AI Employee Agent - Project Context

## Project Overview

This is a **hackathon project** for building a "Digital FTE" (Full-Time Equivalent) - an autonomous AI employee powered by **Qwen Code** and **Obsidian**. The system proactively manages personal and business affairs 24/7 using a local-first, agent-driven architecture.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

**Current Status:** ✅ **Bronze Tier Complete** - Foundation implemented and working

---

## Core Architecture

| Layer | Component | Purpose | Status |
|-------|-----------|---------|--------|
| **Brain** | Qwen Code / Claude Code | Reasoning engine with Ralph Wiggum persistence loop | ✅ Implemented |
| **Memory/GUI** | Obsidian (Markdown) | Dashboard, knowledge base, long-term memory | ✅ Implemented |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems to trigger AI | ✅ File System Watcher |
| **Hands** | MCP Servers | Model Context Protocol for external actions | 🔄 Playwright MCP installed |

---

## Repository Structure

```
Personal-AI-Employee-Agent/
├── PRD.md                      # Product Requirements Document (1201 lines - full blueprint)
├── QWEN.md                     # This file - project context for AI assistant
├── skills-lock.json            # Installed skill dependencies
├── .gitattributes              # Git text normalization config
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/   # Browser automation skill
│           ├── SKILL.md                # Skill documentation
│           ├── references/
│           │   └── playwright-tools.md # Complete MCP tool reference
│           └── scripts/
│               ├── mcp-client.py       # Universal MCP client (HTTP + stdio)
│               ├── start-server.sh     # Start Playwright MCP server
│               ├── stop-server.sh      # Stop Playwright MCP server
│               └── verify.py           # Server health check
├── AI_Employee_Vault/          # Obsidian vault (core workspace)
│   ├── Dashboard.md            # Real-time status summary
│   ├── Company_Handbook.md     # Rules of engagement
│   ├── Business_Goals.md       # Q1 2026 objectives
│   ├── README.md               # Quick start guide
│   ├── USER_GUIDE.md           # Complete user documentation
│   ├── Inbox/                  # Drop zone for new files
│   ├── Needs_Action/           # Pending action items (queue)
│   ├── Done/                   # Completed tasks (organized by date)
│   ├── Plans/                  # Multi-step task plans
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions ready to execute
│   ├── Accounting/             # Bank transactions, invoices
│   ├── Briefings/              # CEO briefing reports
│   └── scripts/                # Automation scripts
│       ├── base_watcher.py     # Abstract base class for all watchers
│       ├── filesystem_watcher.py # File system watcher (Bronze Tier)
│       ├── orchestrator.py     # Processes Needs_Action folder
│       ├── verify_bronze_tier.py # Verification script
│       ├── SKILL.md            # Qwen Code agent skill documentation
│       └── requirements.txt    # Python dependencies
└── docs/
    └── bronze-tier/
        ├── BRONZE_TIER_PRD.md  # Bronze tier specification
        ├── USER_GUIDE.md       # User documentation
        └── QA_Reports/         # Quality assurance reports
```

---

## Key Concepts

### Watcher Pattern

Lightweight Python scripts run continuously, monitoring inputs and creating actionable `.md` files in `/Needs_Action`:

```python
class BaseWatcher(ABC):
    """Abstract base class for all watchers"""
    
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass
    
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass
    
    def run(self):
        """Main loop - runs until interrupted"""
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(check_interval)
```

### Ralph Wiggum Loop

A Stop hook pattern that keeps Qwen Code iterating until multi-step tasks are complete:

1. Orchestrator creates state file with prompt
2. Qwen Code works on task
3. Qwen Code tries to exit
4. Stop hook checks: Is task file in `/Done`?
5. YES → Allow exit (complete)
6. NO → Block exit, re-inject prompt (loop continues)

### Human-in-the-Loop (HITL)

For sensitive actions (payments, sending messages):
1. AI creates approval request in `/Pending_Approval`
2. User moves file to `/Approved` or `/Rejected`
3. Orchestrator triggers MCP action for approved items

### Business Handover

Autonomous weekly audits generating "Monday Morning CEO Briefing":
- Revenue summary vs. targets
- Bottleneck identification
- Proactive cost optimization suggestions

---

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Qwen Code / Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers & automation |
| GitHub Desktop | Latest | Version control |

### Hardware Requirements

- **Minimum:** 8GB RAM, 4-core CPU, 20GB free disk
- **Recommended:** 16GB RAM, 8-core CPU, SSD storage
- **For always-on:** Dedicated mini-PC or cloud VM

### Installation

```bash
# Install Python dependencies
pip install -r AI_Employee_Vault/scripts/requirements.txt
```

### Running the System

```bash
# Terminal 1: Start the File System Watcher (runs continuously)
cd AI_Employee_Vault/scripts
python filesystem_watcher.py

# Terminal 2: Process pending items (run once)
python orchestrator.py

# Or run orchestrator continuously (checks every 5 minutes)
python orchestrator.py --continuous
```

### Usage Pattern

1. **Drop a file** into `AI_Employee_Vault/Inbox/`
2. **Watcher detects** it within 30 seconds and creates an action file in `Needs_Action/`
3. **Orchestrator processes** it via Qwen Code
4. **Results logged** in `Dashboard.md`, file moved to `Done/`

---

## Development Conventions

### File Naming

- Action files: `<TYPE>_<ID>_<DATE>.md` (e.g., `FILE_DROP_report_20260317_120000.md`)
- Approval requests: `APPROVAL_REQUIRED_<Description>.md`
- Briefings: `<YYYY-MM-DD>_<Day>_Briefing.md`

### Markdown Frontmatter

All action files use YAML frontmatter:
```yaml
---
type: file_drop
source: filesystem
created: 2026-03-17T12:00:00
priority: high
status: pending
original_name: report.pdf
---
```

### Priority Levels

| Priority | Keywords | Response Target |
|----------|----------|-----------------|
| **urgent** | urgent, asap, emergency, immediate | Process immediately |
| **high** | invoice, payment, contract, legal, tax | Within 4 hours |
| **normal** | (default) | Within 24 hours |
| **low** | archive, reference, FYI | When time permits |

### Human-in-the-Loop Pattern

For sensitive actions:
1. AI creates approval request in `/Pending_Approval`
2. User moves file to `/Approved` or `/Rejected`
3. Orchestrator executes approved actions
4. AI logs action in `Dashboard.md`

---

## Installed Skills

### browsing-with-playwright

Browser automation using Playwright MCP server.

**Purpose:** Navigate websites, fill forms, click elements, take screenshots, extract data.

**Server Management:**
```bash
# Start server (port 8808, shared browser context)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Stop server (closes browser gracefully)
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh

# Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

**Key Tools Available:**
- `browser_navigate` - Navigate to URL
- `browser_snapshot` - Capture accessibility snapshot (better than screenshot)
- `browser_click` - Click element by ref
- `browser_type` - Type text into editable element
- `browser_fill_form` - Fill multiple form fields
- `browser_take_screenshot` - Take viewport or full-page screenshot
- `browser_evaluate` - Execute JavaScript
- `browser_run_code` - Run multi-step Playwright code
- `browser_wait_for` - Wait for text or time
- `browser_close` - Close browser

**Important:** The `--shared-browser-context` flag is required to maintain browser state across multiple calls.

---

## Hackathon Tiers

| Tier | Time | Deliverables | Status |
|------|------|--------------|--------|
| **Bronze** | 8-12h | ✅ Obsidian dashboard, 1 watcher, basic Qwen integration | **Complete** |
| **Silver** | 20-30h | Multiple watchers, MCP server, HITL workflow, scheduling | 🔄 Next Target |
| **Gold** | 40+h | Full cross-domain, Odoo integration, Ralph Wiggum loop, audit logging | ⏳ Planned |
| **Platinum** | 60+h | Cloud deployment, work-zone specialization, A2A upgrade | ⏳ Future |

### Bronze Tier Deliverables (✅ Complete)

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] File System Watcher script (`filesystem_watcher.py`)
- [x] Qwen Code integration (`orchestrator.py`)
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] Agent skill documentation (`SKILL.md`)

### Silver Tier Deliverables (Next Steps)

- [ ] Add Gmail Watcher for email monitoring
- [ ] Add WhatsApp Watcher for message monitoring
- [ ] Implement MCP server for sending emails
- [ ] Add human-in-the-loop approval workflow
- [ ] Set up scheduled processing via cron/Task Scheduler
- [ ] Auto-post to LinkedIn/social media

### Gold Tier Deliverables (Future)

- [ ] Full cross-domain integration (Personal + Business)
- [ ] Odoo Community accounting integration via MCP
- [ ] Facebook/Instagram/Twitter integration
- [ ] Multiple MCP servers for different action types
- [ ] Weekly Business and Accounting Audit with CEO Briefing
- [ ] Error recovery and graceful degradation
- [ ] Comprehensive audit logging
- [ ] Ralph Wiggum loop for autonomous multi-step completion

---

## MCP Server Configuration

Configure in `~/.config/claude-code/mcp.json`:
```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

### Recommended MCP Servers

| Server | Capabilities | Use Case |
|--------|--------------|----------|
| filesystem | Read, write, list files | Built-in vault operations |
| email-mcp | Send, draft, search emails | Gmail integration |
| browser-mcp | Navigate, click, fill forms | Payment portals, web automation |
| calendar-mcp | Create, update events | Scheduling |
| slack-mcp | Send messages, read channels | Team communication |

---

## Security & Privacy

### Credential Management

- **NEVER** store credentials in vault or commit to git
- Use environment variables: `export GMAIL_API_KEY="your-key"`
- Use `.env` file (add to `.gitignore`) for local development
- Rotate credentials monthly

### Permission Boundaries

| Action Category | Auto-Approve | Require Approval |
|-----------------|--------------|------------------|
| Email replies | To known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

### Audit Logging

Every action logged to `/Vault/Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "2026-03-17T10:30:00Z",
  "action_type": "email_send",
  "actor": "qwen_code",
  "target": "client@example.com",
  "approval_status": "approved",
  "result": "success"
}
```

---

## Error Handling & Recovery

### Retry Logic

```python
def with_retry(max_attempts=3, base_delay=1, max_delay=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    time.sleep(delay)
        return wrapper
    return decorator
```

### Graceful Degradation

- **Gmail API down:** Queue outgoing emails locally
- **Banking API timeout:** Never retry payments automatically
- **Qwen Code unavailable:** Watchers continue collecting
- **Obsidian vault locked:** Write to temporary folder

---

## Key Reference Documents

| Document | Purpose |
|----------|---------|
| [PRD.md](PRD.md) | Full architecture blueprint (1201 lines) |
| [AI_Employee_Vault/Company_Handbook.md](AI_Employee_Vault/Company_Handbook.md) | Operating rules and escalation policies |
| [AI_Employee_Vault/Business_Goals.md](AI_Employee_Vault/Business_Goals.md) | Q1 2026 objectives and metrics |
| [AI_Employee_Vault/scripts/SKILL.md](AI_Employee_Vault/scripts/SKILL.md) | Qwen Code agent skill documentation |
| [docs/bronze-tier/BRONZE_TIER_PRD.md](docs/bronze-tier/BRONZE_TIER_PRD.md) | Bronze tier specification |
| [docs/bronze-tier/USER_GUIDE.md](docs/bronze-tier/USER_GUIDE.md) | Complete user guide |

---

## Wednesday Research Meetings

- **When:** Wednesdays 10:00 PM PKT
- **Zoom:** [Join Meeting](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube:** [Panaversity Channel](https://www.youtube.com/@panaversity)

---

## Learning Resources

### Prerequisites

| Topic | Resource |
|-------|----------|
| Claude Code Fundamentals | [Agent Factory Textbook](https://agentfactory.panerasity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows) |
| Obsidian Fundamentals | [Obsidian Help](https://help.obsidian.md) |
| MCP Introduction | [Model Context Protocol](https://modelcontextprotocol.io/introduction) |
| Agent Skills | [Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |

### Core Learning

| Topic | Resource |
|-------|----------|
| Claude + Obsidian Integration | [YouTube](https://www.youtube.com/watch?v=sCIS05Qt79Y) |
| Building MCP Servers | [MCP Quickstart](https://modelcontextprotocol.io/quickstart) |
| Playwright Automation | [Playwright Docs](https://playwright.dev/python) |

---

## Example Workflow: Processing a File Drop

```
1. User drops file: echo "Summarize this" > Inbox/report.txt

2. Watcher detects (within 30s):
   - Calculates file hash
   - Creates: Needs_Action/FILE_DROP_report_20260317_120000.md
   - Auto-detects priority based on filename

3. Orchestrator processes:
   - Reads action file frontmatter
   - Invokes Qwen Code with structured prompt
   - Qwen analyzes content, performs actions

4. Completion:
   - Qwen updates Dashboard.md
   - Moves file to Done/YYYY-MM-DD/
   - Logs action in audit log
```

---

*Last Updated: 2026-03-18*
*Project Status: Bronze Tier ✅ Complete - Ready for Silver Tier Enhancement*
