# AI Employee Vault

**Personal AI Employee** - Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r scripts/requirements.txt
```

### 2. Start the File System Watcher (Bronze Tier)

```bash
# Run in background
python scripts/filesystem_watcher.py

# Or with custom drop folder
python scripts/filesystem_watcher.py /path/to/vault /path/to/drop_folder
```

### 3. Drop Files for Processing

Place any file in the `Inbox/` folder:
- Documents (.pdf, .doc, .txt) - for summarization
- Images (.jpg, .png) - for analysis
- Data files (.csv, .xlsx) - for processing
- Code files (.py, .js) - for review

### 4. Process Items

```bash
# Run orchestrator once
python scripts/orchestrator.py

# Or run continuously
python scripts/orchestrator.py --continuous
```

### 5. With Qwen Code

```bash
# Process all pending items
qwen --prompt "Process all items in Needs_Action folder"
```

## Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md           # 📊 Real-time status dashboard
├── Company_Handbook.md    # 📖 Rules of engagement
├── Business_Goals.md      # 🎯 Objectives and metrics
├── Inbox/                 # 📥 Drop files here
├── Needs_Action/          # ⏳ Pending action items
├── Done/                  # ✅ Completed items
├── Plans/                 # 📋 Multi-step task plans
├── Pending_Approval/      # ⚠️ Awaiting approval
├── Approved/              # ✔️ Ready for execution
├── Accounting/            # 💰 Financial records
├── Briefings/             # 📝 CEO briefings
└── scripts/               # 🔧 Automation scripts
```

## Bronze Tier Deliverables

✅ **Completed:**

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] File System Watcher script (monitors Inbox folder)
- [x] Claude Code integration for processing
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] Agent skill documentation (SKILL.md)

## Scripts

| Script | Purpose |
|--------|---------|
| `base_watcher.py` | Base class for all watchers |
| `filesystem_watcher.py` | Monitors Inbox for new files |
| `orchestrator.py` | Processes Needs_Action folder |
| `SKILL.md` | Claude Code agent skill documentation |

## Usage Examples

### Example 1: Process a Document

```bash
# Drop a PDF for summarization
cp quarterly_report.pdf Inbox/

# Wait 30 seconds - watcher creates action file
# Then process
python scripts/orchestrator.py
```

### Example 2: Process an Invoice

```bash
# Drop an invoice (auto-detected as high priority)
cp invoice_123.pdf Inbox/

# The watcher will:
# 1. Detect the new file
# 2. Create action file with priority: high
# 3. Suggest actions: read, extract amount, categorize

# Process with Claude
claude --prompt "Process the invoice in Needs_Action"
```

## Configuration

### Watcher Settings

Edit `scripts/filesystem_watcher.py`:

```python
FileSystemWatcher(
    vault_path="/path/to/vault",
    drop_folder="/path/to/Inbox",  # Default: <vault>/Inbox
    check_interval=30               # Seconds between checks
)
```

### Priority Detection

Files are auto-prioritized based on filename:

| Priority | Keywords |
|----------|----------|
| Urgent | urgent, asap, emergency, immediate |
| High | invoice, payment, contract, legal, tax |
| Normal | (default) |
| Low | archive, reference, FYI |

## Troubleshooting

### Watcher not detecting files?

```bash
# Check if watcher is running
ps aux | grep filesystem_watcher

# Check logs
cat scripts/filesystem_watcher.log

# Restart watcher
pkill -f filesystem_watcher
python scripts/filesystem_watcher.py
```

### Claude Code not found?

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

### Action files not being created?

```bash
# Check Inbox folder permissions
ls -la Inbox/

# Check watcher logs
tail -f scripts/filesystem_watcher.log

# Manually trigger a check
python -c "from filesystem_watcher import *; w = FileSystemWatcher('.'); print(w.check_for_updates())"
```

## Next Steps (Silver Tier)

To upgrade to Silver Tier:

1. Add Gmail Watcher for email monitoring
2. Add WhatsApp Watcher for message monitoring
3. Implement MCP server for sending emails
4. Add human-in-the-loop approval workflow
5. Set up scheduled processing via cron/Task Scheduler

## Resources

- [PRD.md](../../PRD.md) - Full architecture blueprint
- [QWEN.md](../../QWEN.md) - Project context
- [Company_Handbook.md](./Company_Handbook.md) - Operating rules

---

*Bronze Tier Implementation - Personal AI Employee Hackathon 2026*
