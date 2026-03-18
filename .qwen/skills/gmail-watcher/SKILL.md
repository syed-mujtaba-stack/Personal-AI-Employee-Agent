---
name: gmail-watcher
description: |
  Gmail Watcher - Monitor Gmail for new emails and create action items.
  Watches for unread, important emails and creates .md action files in
  Needs_Action folder for Qwen Code to process. Part of Silver Tier.
  
  Usage:
    python scripts/gmail_watcher.py
    
  Requirements:
    - Gmail API credentials (credentials.json)
    - Google API Python client installed
---

# Gmail Watcher Skill

## Overview

The Gmail Watcher monitors your Gmail inbox for new, unread, important emails and automatically creates action files in the `Needs_Action/` folder. This enables your AI Employee to process emails autonomously.

**Silver Tier Deliverable** ✓

## Features

- Monitors Gmail every 2 minutes
- Filters for unread + important emails only
- Auto-detects priority based on email content
- Tracks processed emails (no duplicates)
- Creates structured action files with full email metadata

## Prerequisites

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json`

### 2. Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3. First-Time Authentication

```bash
# Run the watcher - it will open browser for auth
python scripts/gmail_watcher.py

# Follow browser prompts to authorize
# Token will be saved as token.json
```

## Configuration

Edit `gmail_watcher.py` to customize:

```python
GmailWatcher(
    vault_path="/path/to/vault",
    credentials_path="/path/to/credentials.json",
    check_interval=120,  # Check every 2 minutes
    label_filter="is:unread is:important"  # Gmail search query
)
```

## Action File Format

Each email creates an action file like:

```markdown
---
type: email
source: gmail
from: client@example.com
subject: Invoice Payment Request
received: 2026-03-17T10:30:00
priority: high
status: pending
gmail_id: 18e4f123a5b6c789
attachments: invoice.pdf
---

## Email Content

**From:** client@example.com  
**To:** me@mybusiness.com  
**Subject:** Invoice Payment Request  
**Date:** March 17, 2026 at 10:30 AM

---

Hi,

Please find attached the invoice for this month's services.
Payment is due within 30 days.

Best regards,
Client

---

## Suggested Actions

- [ ] Reply to sender
- [ ] Process invoice payment
- [ ] Forward to accounting
- [ ] Archive after processing
```

## Priority Detection

| Condition | Priority |
|-----------|----------|
| Subject contains "urgent", "asap", "emergency" | Urgent |
| Subject contains "invoice", "payment", "due" | High |
| From VIP contact list | High |
| Normal email | Normal |
| Newsletters, promotions | Low |

## Usage Examples

### Start the Watcher

```bash
cd AI_Employee_Vault/scripts
python gmail_watcher.py
```

### Expected Output

```
2026-03-17 10:00:00 - GmailWatcher - Starting GmailWatcher (interval: 120s)
2026-03-17 10:02:00 - GmailWatcher - Found 3 new email(s)
2026-03-17 10:02:01 - GmailWatcher - Created action file for: EMAIL_18e4f123a5b6c789.md
2026-03-17 10:02:01 - GmailWatcher - Created action file for: EMAIL_18e4f123a5b6c790.md
2026-03-17 10:02:02 - GmailWatcher - Created action file for: EMAIL_18e4f123a5b6c791.md
```

### Process Emails with Qwen Code

```bash
# Process all pending emails
qwen --prompt "Process all email action items in Needs_Action folder"

# Or use orchestrator
python orchestrator.py
```

## Integration with Email MCP

For full email automation, combine with `email-mcp` skill:

1. **Gmail Watcher** detects new email → creates action file
2. **Qwen Code** processes email → drafts reply
3. **Email MCP** sends reply (after approval)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Gmail        │    │ Qwen Code    │    │ Email MCP    │
│ Watcher      │───▶│ Processing   │───▶│ Send Email   │
│ (Read)       │    │ (Draft)      │    │ (Send)       │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Human-in-the-Loop Workflow

For sensitive actions (sending emails, payments):

1. Watcher creates action file in `Needs_Action/`
2. Qwen Code drafts reply → creates `Pending_Approval/` file
3. User reviews → moves to `Approved/` or `Rejected/`
4. Email MCP sends approved emails

## Error Handling

### Authentication Errors

```
Error: Token expired
Solution: Delete token.json and re-authenticate
```

### API Rate Limits

```
Error: 429 Too Many Requests
Solution: Increase check_interval to 300+ seconds
```

### Network Issues

```
Error: Connection timeout
Solution: Watcher auto-retries on next check cycle
```

## Testing

### Test 1: Verify Connection

```bash
python -c "from gmail_watcher import GmailWatcher; w = GmailWatcher('..', 'credentials.json'); print('OK')"
```

### Test 2: Send Test Email

1. Send yourself an email with subject "TEST"
2. Wait 2 minutes
3. Check `Needs_Action/` for action file

### Test 3: Verify Priority Detection

```bash
# Send email with subject "URGENT: Invoice Due"
# Should create action file with priority: urgent
```

## Security Best Practices

| Practice | Implementation |
|----------|----------------|
| Never commit credentials | Add `credentials.json` to `.gitignore` |
| Store tokens securely | Token saved in vault, not synced |
| Minimal permissions | Gmail API read-only scope |
| Rotate credentials | Regenerate OAuth credentials every 90 days |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No emails detected | Check Gmail search query, verify labels |
| Duplicate action files | Clear processed_log.txt |
| Auth failure | Delete token.json, re-run auth flow |
| Slow performance | Increase check_interval |

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Check interval | 120 seconds | 120s ✓ |
| Email detection | <5 minutes | ~2 minutes ✓ |
| Duplicate rate | 0% | Hash-based ✓ |
| Priority accuracy | >90% | Keyword-based ✓ |

## Files Created

```
.qwen/skills/gmail-watcher/
├── SKILL.md              # This file
├── scripts/
│   ├── gmail_watcher.py  # Main watcher script
│   └── requirements.txt  # Python dependencies
└── references/
    └── gmail-api-setup.md  # Setup guide
```

## Related Skills

- **Silver Tier:**
  - `whatsapp-watcher` - Monitor WhatsApp messages
  - `email-mcp` - Send emails via MCP
  - `hitl-approval` - Human-in-the-loop approval workflow

- **Bronze Tier:**
  - `ai-employee-vault-processor` - Process action files
  - `browsing-with-playwright` - Browser automation

---

*Silver Tier Skill - Personal AI Employee Hackathon 2026*
