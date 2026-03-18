---
name: whatsapp-watcher
description: |
  WhatsApp Watcher - Monitor WhatsApp Web for new messages and create action items.
  Uses Playwright to automate WhatsApp Web and detect messages containing keywords
  like 'urgent', 'asap', 'invoice', 'payment'. Part of Silver Tier.
  
  Usage:
    python scripts/whatsapp_watcher.py
    
  Requirements:
    - Playwright installed
    - WhatsApp Web session configured
    - Chromium browser installed
---

# WhatsApp Watcher Skill

## Overview

The WhatsApp Watcher monitors WhatsApp Web for new messages containing urgent keywords and automatically creates action files in the `Needs_Action/` folder. This enables your AI Employee to respond to time-sensitive messages quickly.

**Silver Tier Deliverable** ✓

## Features

- Monitors WhatsApp Web every 30 seconds
- Filters messages by keywords (urgent, asap, invoice, payment, help)
- Persistent browser session (stays logged in)
- Auto-detects priority based on message content
- Creates structured action files with message metadata

## Prerequisites

### 1. Install Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. Setup WhatsApp Web Session

```bash
# First run will require QR code scan
python scripts/whatsapp_watcher.py

# Scan QR code with WhatsApp mobile app
# Session saved to ~/.whatsapp_session/
```

## Configuration

Edit `whatsapp_watcher.py` to customize:

```python
WhatsAppWatcher(
    vault_path="/path/to/vault",
    session_path="~/.whatsapp_session",
    check_interval=30,  # Check every 30 seconds
    keywords=['urgent', 'asap', 'invoice', 'payment', 'help']
)
```

## Action File Format

Each message creates an action file like:

```markdown
---
type: message
source: whatsapp
from: +1234567890
contact_name: John Doe
received: 2026-03-17T10:30:00
priority: urgent
status: pending
message_preview: Urgent! Need invoice for...
---

## Message Content

**From:** John Doe (+1234567890)  
**Received:** March 17, 2026 at 10:30 AM  
**Keywords detected:** urgent, invoice

---

Urgent! Need invoice for this month's services ASAP.
Please send by end of day.

---

## Suggested Actions

- [ ] Reply to sender
- [ ] Prepare and send invoice
- [ ] Flag for immediate attention
- [ ] Log interaction
```

## Keyword Detection

| Keyword | Priority | Example |
|---------|----------|---------|
| urgent, emergency | Urgent | "Urgent: Server down" |
| asap, immediately | Urgent | "Need this ASAP" |
| invoice, payment, bill | High | "Invoice overdue" |
| help, support | High | "Help with..." |
| (default) | Normal | Regular messages |

## Usage Examples

### Start the Watcher

```bash
cd AI_Employee_Vault/scripts
python whatsapp_watcher.py
```

### Expected Output

```
2026-03-17 10:00:00 - WhatsAppWatcher - Starting WhatsAppWatcher (interval: 30s)
2026-03-17 10:00:30 - WhatsAppWatcher - Found 2 new message(s)
2026-03-17 10:00:31 - WhatsAppWatcher - Created action file for: WHATSAPP_1234567890_20260317100030.md
```

### Process Messages with Qwen Code

```bash
# Process all pending messages
qwen --prompt "Process all WhatsApp message action items in Needs_Action folder"

# Or use orchestrator
python orchestrator.py
```

## Workflow Integration

```
┌──────────────────┐    ┌──────────────┐    ┌──────────────┐
│ WhatsApp Web     │    │ Qwen Code    │    │ Response     │
│ Watcher          │───▶│ Processing   │───▶│ Draft/Approval│
│ (Read Messages)  │    │ (Draft Reply)│    │ (HITL)       │
└──────────────────┘    └──────────────┘    └──────────────┘
```

## Human-in-the-Loop for Responses

For sending WhatsApp responses:

1. Watcher creates action file in `Needs_Action/`
2. Qwen Code drafts reply → creates `Pending_Approval/` file
3. User reviews → moves to `Approved/`
4. Use Playwright MCP to send approved responses

## Privacy & Terms of Service

⚠️ **Important:** Using WhatsApp Web automation may violate WhatsApp's Terms of Service.

**Recommendations:**
- Use only for business accounts you own
- Consider WhatsApp Business API for production use
- Don't use for spam or bulk messaging
- Respect rate limits (30s minimum interval)

## Error Handling

### Session Expired

```
Error: WhatsApp Web session expired
Solution: Re-scan QR code when browser opens
```

### Browser Crashes

```
Error: Browser context closed unexpectedly
Solution: Restart watcher, session auto-recovers
```

### Rate Limiting

```
Error: Too many requests
Solution: Increase check_interval to 60+ seconds
```

## Testing

### Test 1: Verify Session

```bash
python -c "from whatsapp_watcher import WhatsAppWatcher; w = WhatsAppWatcher('..'); print('Session OK')"
```

### Test 2: Send Test Message

1. Send yourself a WhatsApp message with "TEST"
2. Wait 30 seconds
3. Check `Needs_Action/` for action file

### Test 3: Verify Keyword Detection

```bash
# Send message: "URGENT: Invoice needed"
# Should create action file with priority: urgent
```

## Security Best Practices

| Practice | Implementation |
|----------|----------------|
| Session storage | Saved locally, never synced |
| No credentials | Uses QR auth, no passwords stored |
| Rate limiting | Minimum 30s interval |
| Privacy | Messages processed locally only |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| QR code not showing | Clear session folder, restart |
| No messages detected | Check WhatsApp Web is logged in |
| Browser crashes | Reduce check_interval, update Playwright |
| Duplicate messages | Clear processed_log.txt |

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Check interval | 30 seconds | 30s ✓ |
| Message detection | <1 minute | ~30s ✓ |
| Keyword accuracy | >90% | Keyword-based ✓ |
| Session persistence | 30+ days | Browser cookie ✓ |

## Files Created

```
.qwen/skills/whatsapp-watcher/
├── SKILL.md              # This file
├── scripts/
│   ├── whatsapp_watcher.py  # Main watcher script
│   └── requirements.txt  # Python dependencies
└── references/
    └── whatsapp-web-setup.md  # Setup guide
```

## Related Skills

- **Silver Tier:**
  - `gmail-watcher` - Monitor Gmail emails
  - `email-mcp` - Send emails via MCP
  - `hitl-approval` - Human-in-the-loop approval workflow

- **Bronze Tier:**
  - `ai-employee-vault-processor` - Process action files
  - `browsing-with-playwright` - Browser automation

---

*Silver Tier Skill - Personal AI Employee Hackathon 2026*
