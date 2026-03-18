---
name: ai-employee-vault-processor
description: |
  AI Employee Vault Processor - Process action items from the Obsidian vault.
  Reads files from /Needs_Action, analyzes content, performs actions, and moves
  completed items to /Done. Implements the Bronze Tier foundation for the
  Personal AI Employee system.
  
  Usage:
    qwen --prompt "Process all items in /Needs_Action folder"
---

# AI Employee Vault Processor Skill

## Overview

This skill enables Qwen Code to function as an AI Employee that:
- Reads action files from the `/Needs_Action` folder
- Analyzes content and performs requested tasks
- Updates the Dashboard.md with progress
- Moves completed items to `/Done`

## Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Real-time status dashboard
├── Company_Handbook.md    # Rules and guidelines
├── Business_Goals.md      # Objectives and metrics
├── Inbox/                 # Drop folder for new files
├── Needs_Action/          # Pending action items
├── Done/                  # Completed items (organized by date)
├── Plans/                 # Multi-step task plans
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Ready for execution
├── Accounting/            # Financial records
├── Briefings/             # CEO briefings
└── scripts/               # Automation scripts
    ├── base_watcher.py    # Base class for watchers
    ├── filesystem_watcher.py  # File system watcher
    └── orchestrator.py    # Processing orchestrator
```

## Processing Workflow

### Step 1: Read Action Files

```bash
# List pending items
ls AI_Employee_Vault/Needs_Action/*.md

# Read an action file
cat AI_Employee_Vault/Needs_Action/FILE_DROP_example_20260317_120000.md
```

### Step 2: Analyze Frontmatter

Each action file contains YAML frontmatter:

```yaml
---
type: file_drop
source: filesystem
created: 2026-03-17T12:00:00
priority: normal
status: pending
original_name: report.pdf
file_size: 1.5 MB
file_type: .PDF
---
```

**Priority Levels:**
- `urgent`: Process immediately (contains "urgent", "asap", "emergency")
- `high`: Process within 4 hours (invoices, payments, contracts)
- `normal`: Process within 24 hours (default)
- `low`: Process when time permits

### Step 3: Perform Actions

Based on the action file type and suggested actions:

#### For File Drops:
1. Read the file content
2. Summarize key information
3. Extract action items
4. Categorize and archive

#### For Emails:
1. Analyze sender and subject
2. Draft response if needed
3. Flag for approval if sensitive
4. Archive after processing

#### For Messages:
1. Identify urgency level
2. Draft professional response
3. Route to appropriate channel
4. Log interaction

### Step 4: Update Dashboard

After processing each item, update `Dashboard.md`:

```markdown
## 📊 Quick Stats

| Metric | Value | Trend |
|--------|-------|-------|
| Pending Tasks | 3 | ⬇️ |
| Completed Today | 5 | ⬆️ |
```

### Step 5: Move to Done

When all suggested actions are complete:

```bash
# Create dated folder
mkdir -p AI_Employee_Vault/Done/2026-03-17

# Move completed file
mv AI_Employee_Vault/Needs_Action/completed.md AI_Employee_Vault/Done/2026-03-17/
```

## Action File Format

```markdown
---
type: file_drop
source: filesystem
created: 2026-03-17T12:00:00
priority: normal
status: pending
original_name: quarterly_report.pdf
---

## File Information

- **Original Name:** quarterly_report.pdf
- **Size:** 1.5 MB
- **Type:** .PDF
- **Dropped:** 2026-03-17 12:00:00

## Content Summary

*Awaiting AI analysis*

## Suggested Actions

- [ ] Read and summarize content
- [ ] Extract action items
- [ ] File in appropriate category
- [ ] Move original file to appropriate archive folder
- [ ] Update Dashboard.md with progress
```

## Response Templates

### Acknowledgment
```
I've received the task to process [filename]. Let me analyze the content and create a plan.

**Initial Assessment:**
- Type: [type]
- Priority: [priority]
- Estimated time: [time]

**Plan:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

Starting now...
```

### Completion Summary
```
**Task Complete: [filename]**

**Summary:**
- [Key finding/action 1]
- [Key finding/action 2]
- [Key finding/action 3]

**Actions Taken:**
- [x] Read and analyzed content
- [x] Extracted 3 action items
- [x] Filed in /Accounting/2026-Q1
- [x] Updated Dashboard.md

**Follow-up Required:**
- [ ] [Any pending items requiring human action]

<promise>TASK_COMPLETE</promise>
```

## Rules from Company Handbook

### Always:
- Log all actions taken
- Be transparent about decisions
- Flag payments over $500 for approval
- Respond within 24 hours
- Move completed items to /Done

### Never:
- Delete files without approval
- Send external communications without approval
- Share sensitive information outside vault
- Modify Company_Handbook.md without explicit request

## Error Handling

### If Qwen Code is not available:
```
Error: Qwen Code not found
Solution: Install Qwen Code CLI
```

### If file cannot be read:
```
Unable to read [filename]. Possible causes:
- File is locked by another process
- File path is incorrect
- Permissions issue

Creating error report in /Needs_Action/ERROR_[filename].md
```

### If action requires approval:
```
This action requires human approval per Company Handbook rules.

**Action Required:** [description]
**Reason:** [why approval is needed]

Created approval request: /Pending_Approval/APPROVAL_[description].md

Please review and move to /Approved when ready.
```

## Testing the Skill

### Test 1: Process a file drop
```bash
# Create a test file
echo "Test content for AI processing" > AI_Employee_Vault/Inbox/test_document.txt

# Wait 30 seconds for watcher to create action file
# Then run Qwen Code
qwen --prompt "Process all items in Needs_Action folder"
```

### Test 2: Verify Dashboard update
```bash
# Check Dashboard.md was updated
cat AI_Employee_Vault/Dashboard.md | grep -A5 "Quick Stats"
```

### Test 3: Verify file movement
```bash
# Check Done folder for processed items
ls -la AI_Employee_Vault/Done/$(date +%Y-%m-%d)/
```

## Integration with Watchers

The watcher scripts create action files that this skill processes:

```python
# Watcher creates action file
watcher.create_action_file(item)

# Orchestrator invokes Claude
subprocess.run(['claude', '--prompt', prompt])

# Claude processes and moves to Done
# Dashboard is updated automatically
```

## Continuous Processing Mode

For autonomous operation, use the orchestrator:

```bash
# Run once
python scripts/orchestrator.py

# Run continuously (checks every 5 minutes)
python scripts/orchestrator.py --continuous
```

## Metrics to Track

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Response time | <24 hours | created → processed timestamp |
| Completion rate | >95% | Done / (Done + Errors) |
| Approval accuracy | 100% | Manual review |
| Dashboard freshness | <1 hour | Last sync timestamp |

---

*This skill is part of the Bronze Tier deliverables for the Personal AI Employee Hackathon.*
