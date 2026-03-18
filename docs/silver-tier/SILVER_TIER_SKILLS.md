# Silver Tier Skills Overview

**Personal AI Employee Hackathon 0**  
**Tier:** Silver (Functional Assistant)  
**Status:** 📋 Skills Documented  
**Created:** 2026-03-17

---

## Silver Tier Requirements (From PRD)

| # | Requirement | Skill Implementation | Status |
|---|-------------|---------------------|--------|
| 1 | All Bronze requirements | ✅ Complete | Prerequisite |
| 2 | Two or more Watcher scripts | `gmail-watcher`, `whatsapp-watcher` | ✅ Documented |
| 3 | Auto-post to LinkedIn | `linkedin-auto-poster` | ✅ Documented |
| 4 | Plan.md creation | Built into orchestrator | 📝 TODO |
| 5 | One working MCP server | `email-mcp` | ✅ Documented |
| 6 | HITL approval workflow | `hitl-approval` | ✅ Documented |
| 7 | Scheduling (cron/Task Scheduler) | Built into watchers | 📝 TODO |
| 8 | All AI as Agent Skills | All skills documented | ✅ Complete |

---

## Silver Tier Skills Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SILVER TIER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PERCEPTION LAYER (Watchers)                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ File System  │  │    Gmail     │  │   WhatsApp   │         │
│  │ Watcher ✅   │  │   Watcher 📋 │  │  Watcher 📋  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  REASONING LAYER (Qwen Code)                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Vault Processor + Plan Generator + Content Creator  │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
│  ACTION LAYER (MCP + HITL)                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Email MCP 📋│  │  LinkedIn 📋 │  │   HITL 📋    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘

Legend: ✅ Complete (Bronze) | 📋 Documented (Silver) | 📝 TODO
```

---

## Skill 1: Gmail Watcher

**Location:** `.qwen/skills/gmail-watcher/`

### Purpose
Monitor Gmail for new emails and create action items automatically.

### Key Features
- Checks every 2 minutes
- Filters unread + important emails
- Auto-detects priority
- Creates structured action files

### Integration Points
- → Creates files in `Needs_Action/`
- → Processed by `ai-employee-vault-processor`
- → Replies via `email-mcp` (with HITL)

### Prerequisites
- Gmail API credentials
- Google API Python client
- First-time OAuth authentication

### Commands
```bash
# Start watcher
python scripts/gmail_watcher.py

# Test connection
python -c "from gmail_watcher import GmailWatcher; w = GmailWatcher('..'); print('OK')"
```

---

## Skill 2: WhatsApp Watcher

**Location:** `.qwen/skills/whatsapp-watcher/`

### Purpose
Monitor WhatsApp Web for urgent messages and create action items.

### Key Features
- Checks every 30 seconds
- Keyword detection (urgent, asap, invoice, payment, help)
- Persistent browser session
- Priority-based flagging

### Integration Points
- → Creates files in `Needs_Action/`
- → Processed by `ai-employee-vault-processor`
- → Responses via Playwright (with HITL)

### Prerequisites
- Playwright installed
- WhatsApp Web session configured
- Chromium browser

### Commands
```bash
# Start watcher
python scripts/whatsapp_watcher.py

# Login (first time)
python scripts/whatsapp_watcher.py --login
```

---

## Skill 3: Email MCP Server

**Location:** `.qwen/skills/email-mcp/`

### Purpose
Send, draft, and search emails via Model Context Protocol.

### Key Features
- Send emails via Gmail API
- Create drafts for review
- Search and read emails
- Attach files
- HITL approval workflow

### MCP Tools
| Tool | Purpose |
|------|---------|
| `send_email` | Send email immediately |
| `create_draft` | Create draft for review |
| `search_emails` | Search Gmail |
| `read_email` | Read specific email |
| `mark_as_read` | Mark as read |

### Integration Points
- ← Triggered by `ai-employee-vault-processor`
- ← Uses credentials from `gmail-watcher` setup
- → Requires HITL approval for sensitive sends

### Commands
```bash
# Start MCP server
python scripts/start_email_mcp.py

# Auth (first time)
python scripts/email_mcp_auth.py
```

---

## Skill 4: LinkedIn Auto-Poster

**Location:** `.qwen/skills/linkedin-auto-poster/`

### Purpose
Automatically generate and post content to LinkedIn for lead generation.

### Key Features
- Auto-generate posts from completed work
- Schedule for optimal engagement times
- HITL approval before posting
- Track engagement metrics
- Brand voice consistency

### Content Types
| Type | Source | Example |
|------|--------|---------|
| Project Completion | `Done/` folder | "Just completed..." |
| Business Milestone | `Business_Goals.md` | "Reached $10k MRR..." |
| Industry Insight | `Briefings/` | "Key trend in 2026..." |
| Client Testimonial | `Accounting/` | "Happy client..." |

### Integration Points
- ← Reads from `Done/`, `Business_Goals.md`, `Briefings/`
- → Creates `Pending_Approval/` files
- → Posts via Playwright browser automation

### Commands
```bash
# Generate posts
python scripts/linkedin_poster.py --generate

# Schedule approved posts
python scripts/linkedin_poster.py --schedule
```

---

## Skill 5: HITL Approval Workflow

**Location:** `.qwen/skills/hitl-approval/`

### Purpose
Manage approval requests for sensitive actions.

### Key Features
- Structured approval request format
- Folder-based workflow (Pending → Approved/Rejected)
- Automatic expiration & escalation
- Comprehensive audit logging

### Approval Triggers

| Action | Trigger |
|--------|---------|
| Email Send | External recipient |
| Payment | Any amount |
| Social Post | Public posting |
| File Delete | Permanent deletion |
| Contract | Legal documents |
| Expense | >$100 |

### Folder Workflow
```
Pending_Approval/  →  User Reviews  →  Approved/  →  Execute
                         ↓
                    Rejected/  →  Log & Skip
```

### Integration Points
- ← All sensitive actions create approval requests
- → User moves files to Approved/ or Rejected/
- → Orchestrator executes approved actions

### Commands
```bash
# Create approval request (from Python)
from hitl_approval import create_request
req = create_request(action='email_send', to='client@example.com')

# Execute approved actions
python scripts/orchestrator.py --execute-approved
```

---

## Implementation Checklist

### Phase 1: Watchers (8-10 hours)
- [ ] Setup Gmail API credentials
- [ ] Implement `gmail-watcher` skill
- [ ] Test email detection
- [ ] Setup WhatsApp Web session
- [ ] Implement `whatsapp-watcher` skill
- [ ] Test message detection

### Phase 2: MCP Servers (6-8 hours)
- [ ] Implement `email-mcp` server
- [ ] Test email sending
- [ ] Implement HITL approval workflow
- [ ] Test approval → execution flow

### Phase 3: Auto-Posting (4-6 hours)
- [ ] Implement `linkedin-auto-poster`
- [ ] Create content generation logic
- [ ] Test post scheduling
- [ ] Verify HITL integration

### Phase 4: Integration (2-4 hours)
- [ ] End-to-end testing
- [ ] Documentation review
- [ ] Performance optimization
- [ ] Silver Tier verification

---

## Testing Strategy

### Test 1: Gmail → Email Flow
```
1. Send test email to monitored account
2. Verify gmail-watcher creates action file
3. Qwen Code drafts reply
4. HITL creates approval request
5. User approves
6. Email MCP sends reply
```

### Test 2: WhatsApp → Response Flow
```
1. Send WhatsApp message with "urgent"
2. Verify whatsapp-watcher creates action file
3. Qwen Code drafts response
4. HITL creates approval request
5. User approves
6. Playwright posts response
```

### Test 3: LinkedIn Auto-Post Flow
```
1. Complete project (move file to Done/)
2. LinkedIn poster generates post
3. HITL creates approval request
4. User approves + schedules
5. Post published at scheduled time
```

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Gmail check interval | 120 seconds | Watcher config |
| WhatsApp check interval | 30 seconds | Watcher config |
| Email send latency | <5 seconds | MCP response |
| Approval response time | <4 hours | User SLA |
| Post engagement rate | >3% | LinkedIn analytics |
| Duplicate detection | 100% | Hash-based |

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Gmail credentials | Store in .env, never commit |
| WhatsApp session | Local storage only, not synced |
| LinkedIn login | Use Business API for production |
| Email sending | HITL approval for external sends |
| Social posting | All posts require approval |

---

## Upgrade Path to Gold Tier

| Silver Feature | Gold Enhancement |
|----------------|------------------|
| Gmail + WhatsApp | + Facebook, Instagram, Twitter |
| Email MCP | + Multiple MCP servers |
| LinkedIn posting | + Cross-platform social media |
| Basic HITL | + Advanced approval rules |
| Single orchestrator | + Ralph Wiggum loop |
| Manual scheduling | + Auto-scheduling with cron |

---

## Resources

| Document | Location |
|----------|----------|
| Bronze Tier PRD | `docs/bronze-tier/BRONZE_TIER_PRD.md` |
| Main PRD | `PRD.md` |
| Gmail Watcher Skill | `.qwen/skills/gmail-watcher/SKILL.md` |
| WhatsApp Watcher Skill | `.qwen/skills/whatsapp-watcher/SKILL.md` |
| Email MCP Skill | `.qwen/skills/email-mcp/SKILL.md` |
| LinkedIn Auto-Poster | `.qwen/skills/linkedin-auto-poster/SKILL.md` |
| HITL Approval | `.qwen/skills/hitl-approval/SKILL.md` |

---

*Silver Tier Skills Documentation - Personal AI Employee Hackathon 2026*  
*Document Version: 1.0*  
*Created: 2026-03-17*
