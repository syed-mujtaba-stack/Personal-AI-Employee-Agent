# AI Employee User Guide

**Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

---

## Quick Start (5 Minutes)

### Step 1: Start the Watcher

```bash
cd E:\hackathon-0\Personal-AI-Employee-Agent\AI_Employee_Vault\scripts
python filesystem_watcher.py
```

**Keep this terminal open** - the watcher runs continuously.

### Step 2: Drop a File

Drag any file into the `Inbox/` folder, or:

```bash
echo "Please summarize this document" > Inbox\myfile.txt
```

### Step 3: Process It

```bash
python orchestrator.py
```

### Step 4: Check Results

```bash
type ..\Dashboard.md
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR AI EMPLOYEE SYSTEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. WATCHER (Senses)        2. ORCHESTRATOR (Brain)             │
│     ┌──────────────┐           ┌──────────────┐                 │
│     │ filesystem   │  ────────▶│   Qwen       │                 │
│     │ _watcher.py  │           │    Code      │                 │
│     └──────────────┘           └──────────────┘                 │
│          │                        │                              │
│          ▼                        ▼                              │
│  ┌──────────────┐          ┌──────────────┐                     │
│  │   Inbox/     │          │ Needs_Action/│                     │
│  │ (drop files) │          │ (action files)│                    │
│  └──────────────┘          └──────────────┘                     │
│                                  │                              │
│                                  ▼                              │
│                          ┌──────────────┐                       │
│                          │   Done/      │                       │
│                          │ (completed)  │                       │
│                          └──────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## How It Works: Step-by-Step

### Step 1: Start the Watcher (The "Senses")

**Command:**
```bash
cd E:\hackathon-0\Personal-AI-Employee-Agent\AI_Employee_Vault\scripts
python filesystem_watcher.py
```

**What it does:**
- Runs continuously in the background
- Checks `Inbox/` folder every 30 seconds
- When you drop a file, it creates an action file in `Needs_Action/`
- Tracks processed files (won't process same file twice)

**Why you need it:**
The watcher is like having a secretary who constantly monitors your inbox. Without it, you'd have to manually tell the system "hey, a new file arrived."

**Keep it running** - minimize the terminal window, don't close it.

---

### Step 2: Drop a File for Processing

**Command:**
```bash
echo "Please summarize this quarterly report..." > Inbox\report.txt
```

Or simply drag-and-drop files into the `Inbox/` folder using File Explorer.

**What happens:**
1. Watcher detects the new file (within 30 seconds)
2. Creates an action file like: `FILE_DROP_report_20260317_120000.md`
3. Saves it in `Needs_Action/` folder
4. Action file contains:
   - File metadata (size, type, hash)
   - Suggested actions (read, summarize, categorize)
   - Priority level (normal, high, urgent)

---

### Step 3: Process the Action File (The "Brain")

**Option A: Run Orchestrator Once**

**Command:**
```bash
python orchestrator.py
```

**What it does:**
- Scans `Needs_Action/` for pending files
- Invokes Qwen Code with the action file content
- Qwen Code analyzes and performs the requested tasks
- Moves completed file to `Done/2026-03-17/`
- Updates `Dashboard.md` with stats

**Option B: Run Orchestrator Continuously**

**Command:**
```bash
python orchestrator.py --continuous
```

**What it does:**
- Same as above, but runs every 5 minutes automatically
- Good for "set it and forget it" operation

**Option C: Use Qwen Code Directly**

**Command:**
```bash
qwen --prompt "Process all items in Needs_Action folder"
```

**What it does:**
- Direct Qwen Code invocation
- More interactive - you can ask follow-up questions

---

### Step 4: Review Results

**Check what was processed:**
```bash
# View completed items
dir Done\2026-03-17

# View updated dashboard
type Dashboard.md
```

---

## Complete Demo: End-to-End

Open **3 terminal windows**:

### Terminal 1: Start Watcher
```bash
cd E:\hackathon-0\Personal-AI-Employee-Agent\AI_Employee_Vault\scripts
python filesystem_watcher.py
```

**Expected Output:**
```
=== File System Watcher ===
Vault: E:\...\AI_Employee_Vault
Drop Folder: E:\...\AI_Employee_Vault\Inbox
Press Ctrl+C to stop

2026-03-17 08:00:00 - FileSystemWatcher - Watching folder: ...\Inbox
2026-03-17 08:00:00 - FileSystemWatcher - Starting FileSystemWatcher (interval: 30s)
```

### Terminal 2: Drop a Test File
```bash
echo "This is a test document. Please summarize it and extract any action items." > Inbox\test_task.txt
```

**Wait 30 seconds**, then check Terminal 1 - you should see:
```
2026-03-17 08:00:30 - FileSystemWatcher - Found 1 new item(s)
2026-03-17 08:00:30 - FileSystemWatcher - Created action file for: test_task.txt
```

### Terminal 3: Process the Item
```bash
python orchestrator.py
```

**Expected Output:**
```
=== AI Employee Orchestrator ===
Vault: E:\...\AI_Employee_Vault
Found 1 pending item(s)
=== Processing: FILE_DROP_test_task_20260317_080030.md ===

[Qwen Code will process here...]

✓ Moved to: Done\2026-03-17\FILE_DROP_test_task_20260317_080030.md
Summary: Task completed successfully

=== Summary ===
Processed: 1
Errors: 0
```

---

## Command Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `python filesystem_watcher.py` | Start file monitoring | Once at startup, keep running |
| `python orchestrator.py` | Process pending items once | When you want to process now |
| `python orchestrator.py --continuous` | Auto-process every 5 min | Set-and-forget mode |
| `qwen --prompt "..."` | Direct Qwen Code processing | Interactive work |
| `python verify_bronze_tier.py` | Check system health | After setup or troubleshooting |

---

## Real-World Use Cases

### Use Case 1: Document Summarization

```bash
# Drop a PDF report
cp quarterly_report.pdf Inbox/

# Wait 30 sec, then process
python orchestrator.py

# Result: Summary in Dashboard.md, file archived in Done/
```

---

### Use Case 2: Invoice Processing

```bash
# Drop an invoice (auto-detected as HIGH priority)
cp invoice_123.pdf Inbox/

# Process
python orchestrator.py

# Result: Amount extracted, categorized in Accounting/, ready for payment
```

---

### Use Case 3: Code Review

```bash
# Drop a code file
cp new_feature.py Inbox/

# Process
python orchestrator.py

# Result: Code reviewed, suggestions provided, bugs identified
```

---

### Use Case 4: Image Analysis

```bash
# Drop an image
cp screenshot.png Inbox/

# Process
python orchestrator.py

# Result: Image described, text extracted (OCR), actions identified
```

---

## Priority System

Files are automatically prioritized based on filename:

| Priority | Keywords | Response Time |
|----------|----------|---------------|
| **Urgent** | urgent, asap, emergency, immediate | Process first |
| **High** | invoice, payment, contract, legal, tax | Within 4 hours |
| **Normal** | (default) | Within 24 hours |
| **Low** | archive, reference, FYI | When time permits |

**Examples:**
- `URGENT_client_contract.pdf` → Urgent priority
- `invoice_march_2026.pdf` → High priority
- `meeting_notes.txt` → Normal priority

---

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # 📊 Real-time status dashboard
├── Company_Handbook.md    # 📖 Rules of engagement
├── Business_Goals.md      # 🎯 Objectives and metrics
├── README.md              # 📝 Usage instructions
├── Inbox/                 # 📥 Drop files here
├── Needs_Action/          # ⏳ Pending action items
├── Done/                  # ✅ Completed items (organized by date)
├── Plans/                 # 📋 Multi-step task plans
├── Pending_Approval/      # ⚠️ Awaiting human approval
├── Approved/              # ✔️ Ready for execution
├── Accounting/            # 💰 Financial records
├── Briefings/             # 📝 CEO briefings
└── scripts/               # 🔧 Automation scripts
    ├── base_watcher.py        # Base watcher class
    ├── filesystem_watcher.py  # File system watcher
    ├── orchestrator.py        # Processing orchestrator
    ├── SKILL.md               # Qwen Code agent skill
    ├── requirements.txt       # Python dependencies
    └── verify_bronze_tier.py  # Verification script
```

---

## Troubleshooting

### Watcher not detecting files?

```bash
# Check if running (Windows)
tasklist | findstr python

# Check logs
type scripts\filesystem_watcher.log

# Restart watcher
pkill -f filesystem_watcher  # Linux/Mac
taskkill /F /IM python.exe   # Windows
python filesystem_watcher.py
```

---

### Qwen Code not installed?

```bash
# Install Qwen Code CLI
# Follow installation instructions for Qwen Code

# Verify
qwen --version
```

---

### Action files not being created?

```bash
# Check Inbox folder permissions
dir Inbox

# Check watcher logs
type scripts\filesystem_watcher.log

# Manually test
python -c "from filesystem_watcher import FileSystemWatcher; w = FileSystemWatcher('..'); print(w.check_for_updates())"
```

---

### Need to stop the watcher?

**In the watcher terminal, press:** `Ctrl+C`

---

## Daily Workflow

### Morning (8:00 AM)
```bash
# Start watcher
python filesystem_watcher.py

# Check dashboard
type Dashboard.md
```

### During Day
- Drop files into `Inbox/` as they arrive
- Watcher automatically creates action items
- Orchestrator processes every 5 minutes (if running in continuous mode)

### Evening (5:00 PM)
```bash
# Process any remaining items
python orchestrator.py

# Review completed work
dir Done\%date%

# Stop watcher (optional)
# Press Ctrl+C in watcher terminal
```

---

## Best Practices

### ✅ Do:
- Keep the watcher running during work hours
- Use descriptive filenames (helps with priority detection)
- Review `Dashboard.md` daily
- Move sensitive items to `Pending_Approval/` manually if needed
- Check logs weekly for errors

### ❌ Don't:
- Drop multiple files with the same name (hash tracking prevents duplicates)
- Delete files from `Needs_Action/` while processing
- Run multiple watchers simultaneously
- Forget to install Python dependencies

---

## Installation Checklist

- [ ] Python 3.13+ installed
- [ ] Dependencies installed: `pip install -r scripts/requirements.txt`
- [ ] Qwen Code CLI installed and configured
- [ ] Verification passed: `python verify_bronze_tier.py`

---

## Next Steps (Silver Tier)

Ready to upgrade? Add:

1. **Gmail Watcher** - Monitor email automatically
2. **WhatsApp Watcher** - Track messages for urgent keywords
3. **MCP Server** - Send emails and messages autonomously
4. **Approval Workflow** - Human-in-the-loop for sensitive actions
5. **Scheduled Processing** - Cron/Task Scheduler integration

---

## Support & Resources

| Resource | Description |
|----------|-------------|
| [PRD.md](../../PRD.md) | Full architecture blueprint |
| [QWEN.md](../../QWEN.md) | Project context |
| [Company_Handbook.md](./Company_Handbook.md) | Operating rules |
| [SKILL.md](./scripts/SKILL.md) | Qwen Code agent documentation |

---

*Bronze Tier Implementation - Personal AI Employee Hackathon 2026*

**Last Updated:** 2026-03-17
