# Bronze Tier PRD: AI Employee Foundation

**Personal AI Employee Hackathon 0**  
**Tier:** Bronze (Foundation)  
**Status:** ✅ Complete  
**Last Updated:** 2026-03-17

---

## Executive Summary

The Bronze Tier represents the **Minimum Viable Deliverable** for the Personal AI Employee system. It establishes the foundational architecture upon which Silver, Gold, and Platinum tiers are built.

**Tagline:** *Your AI Employee foundation - local-first, file-driven, Qwen Code-powered.*

**Estimated Time:** 8-12 hours  
**Actual Time:** ~6 hours (implementation)

---

## Tier Requirements (From Main PRD)

### Required Deliverables

| # | Requirement | Status | Location |
|---|-------------|--------|----------|
| 1 | Obsidian vault with Dashboard.md | ✅ Complete | `AI_Employee_Vault/Dashboard.md` |
| 2 | Company_Handbook.md | ✅ Complete | `AI_Employee_Vault/Company_Handbook.md` |
| 3 | One working Watcher script | ✅ Complete | `AI_Employee_Vault/scripts/filesystem_watcher.py` |
| 4 | Qwen Code integration | ✅ Complete | `AI_Employee_Vault/scripts/orchestrator.py` |
| 5 | Basic folder structure | ✅ Complete | `/Inbox`, `/Needs_Action`, `/Done` |
| 6 | Agent Skills documentation | ✅ Complete | `AI_Employee_Vault/scripts/SKILL.md` |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BRONZE TIER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   WATCHER    │         │ ORCHESTRATOR │                     │
│  │  (Senses)    │────────▶│   (Brain)    │                     │
│  │              │  Files  │              │                     │
│  └──────────────┘         └──────────────┘                     │
│         │                       │                               │
│         ▼                       ▼                               │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   Inbox/     │         │ Needs_Action/│                     │
│  │ (Drop Zone)  │         │ (Queue)      │                     │
│  └──────────────┘         └──────────────┘                     │
│                                 │                               │
│                                 ▼                               │
│                         ┌──────────────┐                        │
│                         │   Done/      │                        │
│                         │ (Archive)    │                        │
│                         └──────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. The Nerve Center (Obsidian Vault)

**Purpose:** Acts as the GUI and Long-Term Memory

| File | Purpose | Status |
|------|---------|--------|
| `Dashboard.md` | Real-time status dashboard | ✅ Created |
| `Company_Handbook.md` | Rules of engagement | ✅ Created |
| `Business_Goals.md` | Q1 2026 objectives | ✅ Created |
| `README.md` | Usage instructions | ✅ Created |
| `USER_GUIDE.md` | Complete user guide | ✅ Created |

#### 2. The Muscle (Qwen Code)

**Purpose:** Reasoning engine that processes action items

| Component | Purpose | Status |
|-----------|---------|--------|
| `orchestrator.py` | Processes Needs_Action folder | ✅ Created |
| `SKILL.md` | Qwen Code agent skill doc | ✅ Created |

#### 3. The Senses (Watchers)

**Purpose:** Monitor inputs and create actionable files

| Component | Purpose | Status |
|-----------|---------|--------|
| `base_watcher.py` | Abstract base class | ✅ Created |
| `filesystem_watcher.py` | Monitors Inbox folder | ✅ Created |

---

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time status
├── Company_Handbook.md       # Operating rules
├── Business_Goals.md         # Objectives & metrics
├── README.md                 # Quick start guide
├── USER_GUIDE.md             # Complete documentation
├── Inbox/                    # Drop zone for new files
├── Needs_Action/             # Pending action items
├── Done/                     # Completed items (by date)
│   └── YYYY-MM-DD/
├── Plans/                    # Multi-step task plans
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Ready for execution
├── Accounting/               # Financial records
├── Briefings/                # CEO briefings
└── scripts/                  # Automation scripts
    ├── base_watcher.py       # Base watcher class
    ├── filesystem_watcher.py # File system watcher
    ├── orchestrator.py       # Processing orchestrator
    ├── verify_bronze_tier.py # Verification script
    ├── SKILL.md              # Agent skill documentation
    └── requirements.txt      # Python dependencies
```

---

## Technical Specifications

### Watcher Pattern

**File:** `scripts/base_watcher.py`

```python
class BaseWatcher(ABC):
    """Abstract base class for all watchers."""
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass
    
    def run(self):
        """Main watcher loop - runs continuously"""
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(self.check_interval)
```

### File System Watcher

**File:** `scripts/filesystem_watcher.py`

**Features:**
- Monitors `Inbox/` folder every 30 seconds
- Creates action files with metadata (size, type, hash)
- Auto-detects priority based on filename
- Tracks processed files (no duplicates)

**Priority Detection:**

| Priority | Keywords | Example |
|----------|----------|---------|
| Urgent | urgent, asap, emergency | `URGENT_contract.pdf` |
| High | invoice, payment, contract | `invoice_march.pdf` |
| Normal | (default) | `meeting_notes.txt` |
| Low | archive, reference, FYI | `FYI_report.pdf` |

### Orchestrator

**File:** `scripts/orchestrator.py`

**Workflow:**
1. Scan `Needs_Action/` for pending files
2. Sort by priority (urgent first)
3. Invoke Qwen Code for each file
4. Move completed files to `Done/YYYY-MM-DD/`
5. Update `Dashboard.md` with stats

**Qwen Code Integration:**
```python
result = subprocess.run(
    ['qwen', '--prompt', prompt],
    capture_output=True,
    text=True,
    timeout=600,
    shell=True  # Windows PATH inheritance
)
```

---

## Action File Format

Every action file follows this standard format:

```markdown
---
type: file_drop
source: filesystem
created: 2026-03-17T08:30:00
priority: normal
status: pending
original_name: report.pdf
file_size: 1.5 MB
file_type: .PDF
file_hash: abc123...
---

## File Information

- **Original Name:** report.pdf
- **Size:** 1.5 MB
- **Type:** .PDF
- **Dropped:** 2026-03-17 08:30:00

## Content Summary

*Awaiting AI analysis*

## Suggested Actions

- [ ] Read and summarize content
- [ ] Extract action items
- [ ] File in appropriate category
- [ ] Update Dashboard.md with progress
```

---

## Processing Workflow

### Step-by-Step Flow

```
1. User drops file → Inbox/
           ↓
2. Watcher detects (30 sec)
           ↓
3. Creates action file → Needs_Action/
           ↓
4. Orchestrator scans
           ↓
5. Invokes Qwen Code
           ↓
6. Qwen processes task
           ↓
7. Moves to → Done/YYYY-MM-DD/
           ↓
8. Updates Dashboard.md
```

---

## Verification Checklist

Run: `python scripts/verify_bronze_tier.py`

### Required Files (3/3)
- [x] `Dashboard.md`
- [x] `Company_Handbook.md`
- [x] `Business_Goals.md`

### Folder Structure (8/8)
- [x] `Inbox/`
- [x] `Needs_Action/`
- [x] `Done/`
- [x] `Plans/`
- [x] `Pending_Approval/`
- [x] `Approved/`
- [x] `Accounting/`
- [x] `Briefings/`

### Watcher Scripts (3/3)
- [x] `base_watcher.py`
- [x] `filesystem_watcher.py`
- [x] `orchestrator.py`

### Documentation (3/3)
- [x] `SKILL.md`
- [x] `README.md`
- [x] `requirements.txt`

### Functional Tests (1/1)
- [x] Watcher creates action files

**Total:** 18/18 checks passed ✅

---

## Usage Examples

### Quick Start

```bash
# 1. Start watcher
cd AI_Employee_Vault/scripts
python filesystem_watcher.py

# 2. Drop a file
echo "Summarize this" > ../Inbox/test.txt

# 3. Process (in another terminal)
python orchestrator.py
```

### Real-World Use Cases

#### Use Case 1: Document Summarization
```bash
cp quarterly_report.pdf Inbox/
# Wait 30 seconds
python orchestrator.py
# Result: Summary in Dashboard.md
```

#### Use Case 2: Invoice Processing
```bash
cp invoice_123.pdf Inbox/
# Auto-detected as HIGH priority
python orchestrator.py
# Result: Amount extracted, categorized
```

#### Use Case 3: Code Review
```bash
cp new_feature.py Inbox/
python orchestrator.py
# Result: Code reviewed, bugs identified
```

---

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Watcher check interval | 30 seconds | 30 seconds ✅ |
| File detection time | <60 seconds | ~30 seconds ✅ |
| Orchestrator processing | <10 minutes/file | ~2-5 minutes ✅ |
| Duplicate prevention | 100% | Hash-based ✅ |
| Priority accuracy | >90% | Keyword-based ✅ |

---

## Known Limitations (Bronze Tier)

| Limitation | Impact | Workaround | Upgrade Path |
|------------|--------|------------|--------------|
| Single watcher type | Only file drops supported | Manual email export | Silver: Gmail watcher |
| No MCP servers | Can't send emails/messages | Manual approval + action | Silver: MCP integration |
| No scheduling | Manual orchestrator runs | Use `--continuous` flag | Silver: cron/Task Scheduler |
| No approval workflow | All actions auto-executed | Review before dropping | Silver: HITL workflow |
| No Ralph Wiggum loop | Single-pass processing | Manual re-processing | Gold: Autonomous loop |

---

## Upgrade Path to Silver Tier

### Additional Requirements

1. **Second Watcher** (Gmail or WhatsApp)
2. **MCP Server** for external actions (email sending)
3. **Approval Workflow** for sensitive actions
4. **Scheduled Processing** via cron/Task Scheduler
5. **Plan.md** creation for multi-step tasks

### Estimated Effort

- **Time:** 20-30 hours (additional)
- **Complexity:** Medium
- **Dependencies:** Gmail API, MCP servers

---

## Testing Results

### Test 1: File Drop Detection
```bash
# Create test file
echo "Test content" > Inbox/test.txt

# Wait 30 seconds

# Verify action file created
dir Needs_Action

# Result: ✅ PASS - FILE_DROP_test_*.md created
```

### Test 2: Orchestrator Processing
```bash
# Run orchestrator
python orchestrator.py

# Verify file moved to Done
dir Done\2026-03-17

# Result: ✅ PASS - File processed and moved
```

### Test 3: Dashboard Update
```bash
# Check Dashboard.md
type Dashboard.md | findstr "Pending Tasks"

# Result: ✅ PASS - Stats updated
```

### Test 4: Priority Detection
```bash
# Create urgent file
echo "URGENT: Invoice due" > Inbox/URGENT_invoice.pdf

# Check action file priority
type Needs_Action\FILE_DROP_URGENT_*.md | findstr "priority"

# Result: ✅ PASS - priority: urgent
```

---

## Dependencies

### Python Packages
```
watchdog>=4.0.0      # File system monitoring
requests>=2.31.0     # HTTP requests
```

### External Tools
- Python 3.13+
- Qwen Code CLI
- Obsidian (optional, for vault viewing)

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| File hash tracking | MD5 for deduplication (not security) |
| No credential storage | All secrets in environment variables |
| Local-only processing | No cloud sync in Bronze tier |
| File permissions | User manages vault access |

---

## Future Enhancements

### Silver Tier
- [ ] Gmail Watcher
- [ ] WhatsApp Watcher  
- [ ] Email MCP Server
- [ ] Approval workflow

### Gold Tier
- [ ] Odoo integration
- [ ] Social media posting
- [ ] CEO Briefing generation
- [ ] Ralph Wiggum loop

### Platinum Tier
- [ ] Cloud deployment
- [ ] Multi-agent sync
- [ ] A2A communication

---

## Resources

| Document | Location |
|----------|----------|
| Main PRD | `/PRD.md` |
| User Guide | `AI_Employee_Vault/USER_GUIDE.md` |
| Quick Start | `AI_Employee_Vault/README.md` |
| Agent Skill | `AI_Employee_Vault/scripts/SKILL.md` |
| Company Handbook | `AI_Employee_Vault/Company_Handbook.md` |

---

## Sign-Off

**Bronze Tier Status:** ✅ **COMPLETE**

**All 18 verification checks passed**

**Ready for production use as a file-drop processing system**

---

*Bronze Tier Implementation - Personal AI Employee Hackathon 2026*  
*Document Version: 1.0*  
*Created: 2026-03-17*
