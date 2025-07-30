# Debate Conversation Outputs

Generated: 2025-07-02T22:04:14.974455

## Overview

This file provides easy access to all outputs from debate conversation agents.

## Recent Outputs (4 files found)

### 1. panel_debate.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/outputs/panel_debate.md`
**Last Modified:** 2025-06-16T19:18:56.172913
**Lines:** 77
**Title:** Debate Summary:

**Preview:**

```
Debate Summary:

[TechOptimist]:
Social media has revolutionized communication, enabling global connectivity like never before. It empowers individuals to share ideas, cultures, and experiences instan...
```

---

### 2. socratic_debate.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/outputs/socratic_debate.md`
**Last Modified:** 2025-06-16T19:18:56.172913
**Lines:** 56
**Title:** Philosophical Dialogue:

**Preview:**

```
Philosophical Dialogue:

Socrates: Tell me, young friend, what do you believe knowledge to be?

Socrates: Can we truly say we possess knowledge if we have not questioned it ourselves? Consider, if one...
```

---

### 3. oxford_debate.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/outputs/oxford_debate.md`
**Last Modified:** 2025-06-16T19:18:56.172913
**Lines:** 89
**Title:** [55:checkpoint] State at the end of step 55:

**Preview:**

```
[55:checkpoint] State at the end of step 55:
{'argument_scores': {},
'arguments_made': {'FirstOpposition': ['Ladies and gentlemen, esteemed '
'colleagues, and honorable guests,\n'
'\n'
'As the first s...
```

---

### 4. simple_debate.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/outputs/simple_debate.md`
**Last Modified:** 2025-06-16T19:18:56.172913
**Lines:** 191
**Title:** 06/12/25 21:32:16] INFO Phase transition: closing -> complete

**Preview:**

```
06/12/25 21:32:16] INFO Phase transition: closing -> complete
[42:writes] Finished step 42 with writes to 5 channels:

- current_phase -> 'complete'
- phase_transitions -> [('complete', 1)]
- messag...
```

---

## Quick Access

### View State History (JSON)

```bash
# View recent state history files
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate -name "*.json" -exec ls -la {} \;

# Pretty print JSON
cat path/to/file.json | jq '.[0].messages | length'
```

### View Conversation Outputs (Markdown)

```bash
# View markdown outputs
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/outputs -name "*.md" -exec cat {} \;
```

### Copy Files for Analysis

```bash
# Copy all outputs to a temporary directory for analysis
mkdir -p /tmp/debate_analysis
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate -name "*.json" -o -name "*.md" | xargs -I {} cp {} /tmp/debate_analysis/
```

## File Structure

```
debate/
├── outputs/           # Conversation result files (.md)
├── resources/         # State history files (.json)
│   └── state_history/
└── CONVERSATION_OUTPUTS.md  # This summary file
```
