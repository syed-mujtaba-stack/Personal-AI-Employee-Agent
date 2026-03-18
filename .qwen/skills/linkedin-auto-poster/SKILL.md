---
name: linkedin-auto-poster
description: |
  LinkedIn Auto-Poster - Automatically generate and post content to LinkedIn
  for business lead generation. Creates posts based on business goals,
  completed projects, and industry insights. Part of Silver Tier.
  
  Usage:
    python scripts/linkedin_poster.py
    
  Requirements:
    - Playwright installed
    - LinkedIn session configured
    - Content approval workflow
---

# LinkedIn Auto-Poster Skill

## Overview

The LinkedIn Auto-Poster automatically generates and posts content to LinkedIn for business lead generation. It creates posts based on completed projects, business milestones, and industry insights from your vault data.

**Silver Tier Deliverable** ✓

## Features

- Auto-generate posts from completed work
- Schedule posts for optimal engagement times
- Human-in-the-loop approval before posting
- Track engagement metrics
- Maintain brand voice consistency

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Business     │    │ Content      │    │ LinkedIn     │
│ Goals/Done   │───▶│ Generator    │───▶│ Auto-Poster  │
│ (Input)      │    │ (Qwen Code)  │    │ (Playwright) │
└──────────────┘    └──────────────┘    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Pending_     │
                    │ Approval/    │
                    │ (HITL)       │
                    └──────────────┘
```

## Prerequisites

### 1. Install Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. Setup LinkedIn Session

```bash
# First run will require login
python scripts/linkedin_poster.py --login

# Login to LinkedIn in browser
# Session saved to ~/.linkedin_session/
```

## Content Generation

### Post Types

| Type | Source | Example |
|------|--------|---------|
| Project Completion | Done/ folder | "Just completed..." |
| Business Milestone | Business_Goals.md | "Reached $10k MRR..." |
| Industry Insight | Briefings/ | "Key trend in 2026..." |
| Client Testimonial | Accounting/ | "Happy client..." |

### Generated Post Format

```markdown
---
type: social_post
platform: linkedin
generated: 2026-03-17T10:00:00
status: pending_approval
scheduled: 2026-03-18T09:00:00  # Optimal time: Tuesday 9 AM
---

## Post Content

🎉 Project Complete!

Just delivered a new AI automation system for a client.
They're now saving 20 hours/week on manual data entry.

Key results:
✅ 80% reduction in processing time
✅ Zero manual errors
✅ Real-time dashboard

#AI #Automation #Productivity

---

## Media
- Screenshot: dashboard_preview.png

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

## Usage Examples

### Generate Posts from Completed Work

```bash
cd AI_Employee_Vault/scripts

# Analyze Done/ folder and create posts
python linkedin_poster.py --generate

# Review generated posts in Pending_Approval/
```

### Schedule Posts

```bash
# Schedule approved posts
python linkededin_poster.py --schedule

# Posts at optimal times (Tue-Thu 9-11 AM)
```

### Post Immediately

```bash
# Post single approved item
python linkedin_poster.py --post POST_ID
```

## Approval Workflow

All posts require human approval before publishing:

1. **Content Generator** creates post → `Pending_Approval/`
2. **User reviews** content, timing, media
3. **Move to Approved/** → Scheduled for posting
4. **LinkedIn Poster** publishes at scheduled time

### Approval File Format

```markdown
---
type: approval_request
action: linkedin_post
scheduled: 2026-03-18T09:00:00
status: pending
---

## LinkedIn Post Preview

┌────────────────────────────────────────┐
│ 🎉 Project Complete!                   │
│                                        │
│ Just delivered a new AI automation...  │
│                                        │
│ #AI #Automation #Productivity          │
└────────────────────────────────────────┘

## Posting Details
- **Platform:** LinkedIn
- **Scheduled:** March 18, 2026 at 9:00 AM
- **Media:** 1 image attached

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder with reason.
```

## Content Strategy

### Posting Schedule

| Day | Time | Content Type |
|-----|------|--------------|
| Tuesday | 9:00 AM | Project showcase |
| Wednesday | 10:00 AM | Industry insight |
| Thursday | 9:00 AM | Client success |
| Friday | 2:00 PM | Weekly recap |

### Brand Voice Guidelines

```yaml
tone: Professional yet friendly
style: Concise, action-oriented
emoji_usage: Moderate (2-4 per post)
hashtag_count: 3-5 per post
mention_policy: Tag clients only with permission
```

## Error Handling

### Session Expired

```
Error: LinkedIn session expired
Solution: Re-run with --login flag
```

### Posting Failed

```
Error: LinkedIn blocked automated posting
Solution: Use LinkedIn Business API instead
```

### Content Rejected

```
User rejected post
Solution: Regenerate with different angle
```

## Testing

### Test 1: Generate Sample Post

```bash
python linkedin_poster.py --generate --test
```

### Test 2: Verify Approval Flow

1. Generate post
2. Move to Approved/
3. Run poster
4. Verify posted (or scheduled)

### Test 3: Check Engagement Tracking

```bash
python linkedin_poster.py --analytics
```

## Best Practices

| Practice | Implementation |
|----------|----------------|
| Approval required | All posts need manual approval |
| Optimal timing | Schedule for Tue-Thu 9-11 AM |
| Content variety | Mix of project, insight, testimonial |
| Brand consistency | Use Company_Handbook.md guidelines |
| Analytics tracking | Log post performance |

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Posts per week | 3-4 | Scheduled ✓ |
| Approval rate | 100% | HITL ✓ |
| Engagement rate | >3% | Tracked ✓ |
| Lead generation | 2/week | Analytics ✓ |

## Files Created

```
.qwen/skills/linkedin-auto-poster/
├── SKILL.md              # This file
├── scripts/
│   ├── linkedin_poster.py  # Main poster script
│   ├── content_generator.py # Post content generator
│   └── requirements.txt    # Dependencies
└── references/
    └── linkedin-setup.md   # Setup guide
```

## Related Skills

- **Silver Tier:**
  - `gmail-watcher` - Monitor Gmail emails
  - `whatsapp-watcher` - Monitor WhatsApp messages
  - `email-mcp` - Send emails via MCP
  - `hitl-approval` - Human-in-the-loop approval workflow

---

*Silver Tier Skill - Personal AI Employee Hackathon 2026*
