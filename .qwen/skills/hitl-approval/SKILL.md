---
name: hitl-approval
description: |
  Human-in-the-Loop (HITL) Approval Workflow - Manage approval requests for
  sensitive actions like sending emails, making payments, or posting on social
  media. Ensures human oversight for critical business operations.
  
  Usage:
    # Qwen Code creates approval request
    # User moves file to Approved/ or Rejected/
    # Orchestrator executes approved actions
---

# Human-in-the-Loop (HITL) Approval Workflow

## Overview

The HITL Approval Workflow ensures that sensitive actions (sending emails, making payments, posting on social media) require human approval before execution. This is a critical safety mechanism for the AI Employee system.

**Silver Tier Deliverable** ✓

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Qwen Code    │    │ Pending_     │    │ User         │
│ Identifies   │───▶│ Approval/    │───▶│ Reviews &    │
│ Sensitive    │    │ *.md         │    │ Moves File   │
│ Action       │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                                  │
                          ┌───────────────────────┼───────────────────────┐
                          │                       │                       │
                          ▼                       ▼                       ▼
                   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
                   │ Approved/    │      │ Rejected/    │      │ Modified/    │
                   │ Execute      │      │ Log & Skip   │      │ Revise       │
                   └──────────────┘      └──────────────┘      └──────────────┘
```

## Approval Triggers

### Automatic Approval Required

| Action Type | Trigger | Example |
|-------------|---------|---------|
| Email Send | External recipient | Sending to client |
| Payment | Any amount | Bank transfer |
| Social Post | Public posting | LinkedIn, Twitter |
| File Delete | Permanent deletion | Remove documents |
| Contract | Legal documents | Signing agreements |
| Expense | >$100 | Software purchase |

### Auto-Approved (No HITL)

| Action Type | Condition | Example |
|-------------|-----------|---------|
| Email Draft | Internal only | Draft to self |
| File Move | Within vault | Organizing files |
| Data Read | No external API | Reading local files |
| Summary | No action taken | Generating reports |

## Approval Request Format

```markdown
---
type: approval_request
action: email_send
to: client@example.com
subject: Invoice #1234 Payment
created: 2026-03-17T10:30:00
expires: 2026-03-18T10:30:00
priority: high
status: pending
request_id: APR_20260317_103000_001
---

# Approval Request: Send Email

## Action Details

**Type:** Email Send  
**To:** client@example.com  
**Subject:** Invoice #1234 Payment  
**Priority:** High  
**Expires:** March 18, 2026 at 10:30 AM  

---

## Email Content

Dear Client,

Thank you for your business. Please find attached
invoice #1234 for services rendered in March 2026.

**Amount Due:** $5,000.00  
**Due Date:** April 16, 2026  

Payment can be made via bank transfer or check.

Best regards,  
Your Company

---

## Attachments

- invoice_1234.pdf (245 KB)

---

## Why This Requires Approval

This email requires approval because:
- Sending to external recipient
- Contains payment/financial information
- Represents business communication

---

## How to Respond

### ✅ To Approve
Move this file to: `/Approved/`

The email will be sent within 5 minutes.

### ❌ To Reject
Move this file to: `/Rejected/`

Add a comment explaining why (optional).

### ✏️ To Modify
1. Edit this file with changes
2. Move to: `/Approved/`

The modified version will be sent.

---

## Request Metadata

- **Requested by:** Qwen Code (AI Employee)
- **Request ID:** APR_20260317_103000_001
- **Created:** March 17, 2026 at 10:30 AM
- **Rule triggered:** Company_Handbook.md Section 3.2
```

## Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/     # Awaiting decision
│   ├── APPROVAL_Email_Client_20260317.md
│   └── APPROVAL_Payment_Vendor_20260317.md
├── Approved/             # Ready to execute
│   └── APPROVAL_Email_Client_20260317.md
├── Rejected/             # Declined actions
│   └── APPROVAL_Payment_Vendor_20260317.md
└── Logs/
    └── approvals_2026-03.json  # Audit trail
```

## Usage Examples

### Qwen Code Creates Approval Request

When Qwen Code identifies a sensitive action:

```python
# In orchestrator.py or skill
def request_approval(action_type, details):
    approval_file = create_approval_request(
        action=action_type,
        **details
    )
    move_to_pending(approval_file)
    return approval_file
```

### User Reviews and Approves

1. Check pending approvals:
   ```bash
   dir AI_Employee_Vault\Pending_Approval
   ```

2. Read the request:
   ```bash
   type AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
   ```

3. Make decision:
   - Approve: Move to `Approved/`
   - Reject: Move to `Rejected/`
   - Modify: Edit then move to `Approved/`

### Orchestrator Executes Approved Actions

```bash
# Check for approved actions
python orchestrator.py --execute-approved

# Or run continuously
python orchestrator.py --continuous
```

## Approval Rules Configuration

Edit `Company_Handbook.md` to define rules:

```markdown
## Approval Rules

### Payments
- Any payment > $0: Require approval
- Recurring payments < $50: Auto-approve if expected
- New payee: Always require approval

### Emails
- External recipients: Require approval
- Internal (company domain): Auto-approve
- Bulk emails (>10 recipients): Require approval

### Social Media
- All public posts: Require approval
- Scheduled posts: Require approval
- Replies to comments: Auto-approve if positive

### File Operations
- Delete files: Require approval
- Move within vault: Auto-approve
- Export outside vault: Require approval
```

## Audit Logging

Every approval action is logged:

```json
{
  "timestamp": "2026-03-17T10:35:00Z",
  "request_id": "APR_20260317_103000_001",
  "action_type": "email_send",
  "actor": "user_name",
  "decision": "approved",
  "execution_time": "2026-03-17T10:35:15Z",
  "execution_result": "success"
}
```

## Expiration & Escalation

### Expiration Rules

| Priority | Expires In | Action |
|----------|------------|--------|
| Urgent | 1 hour | Auto-reject + notify |
| High | 24 hours | Auto-reject |
| Normal | 7 days | Auto-reject |
| Low | 30 days | Auto-reject |

### Escalation

If approval pending too long:

1. **Reminder at 50% of expiry time**
2. **Move to top of Pending_Approval/**
3. **Notify user via email/SMS**

## Testing

### Test 1: Create Approval Request

```bash
python -c "
from hitl_approval import create_request
req = create_request(
    action='email_send',
    to='test@example.com',
    subject='Test'
)
print('Request created:', req)
"
```

### Test 2: Verify Workflow

1. Create test approval request
2. Move to Approved/
3. Run orchestrator
4. Verify execution

### Test 3: Test Rejection

1. Create test approval request
2. Move to Rejected/
3. Verify logged as rejected

## Best Practices

| Practice | Implementation |
|----------|----------------|
| Clear descriptions | Explain what, why, impact |
| Expiration times | Set based on priority |
| Audit trail | Log all decisions |
| Easy to review | Structured format |
| Quick approval | Simple move-to-approve |

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Approval response time | <4 hours | Tracked ✓ |
| False positive rate | <10% | Rule tuning ✓ |
| Audit completeness | 100% | Logged ✓ |
| User satisfaction | >90% | Feedback ✓ |

## Files Created

```
.qwen/skills/hitl-approval/
├── SKILL.md              # This file
├── scripts/
│   ├── hitl_approval.py  # Approval workflow logic
│   └── requirements.txt  # Dependencies
└── references/
    └── approval-rules.md  # Rule configuration guide
```

## Related Skills

- **Silver Tier:**
  - `gmail-watcher` - Monitor Gmail emails
  - `whatsapp-watcher` - Monitor WhatsApp messages
  - `email-mcp` - Send emails via MCP
  - `linkedin-auto-poster` - Auto-post to LinkedIn

- **Bronze Tier:**
  - `ai-employee-vault-processor` - Process action files

---

*Silver Tier Skill - Personal AI Employee Hackathon 2026*
