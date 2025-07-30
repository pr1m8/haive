# Collaberative Conversation Outputs

Generated: 2025-07-02T22:04:14.973179

## Overview

This file provides easy access to all outputs from collaberative conversation agents.

## Recent Outputs (9 files found)

### 1. ProductManager_agent_20250702_215328.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history/ProductManager_agent_20250702_215328.json`
**Last Modified:** 2025-07-02T21:53:55.668287
**Messages:** 90

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline...
- system: Start the 'Problem Statement' section. Provide a solid foundation for others to build on....

---

### 2. Designer_agent_20250702_215319.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history/Designer_agent_20250702_215319.json`
**Last Modified:** 2025-07-02T21:53:44.074886
**Messages:** 34

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline

Current content:
[Pr...

- system: Build upon or enhance the existing content. Be constructive and collaborative....

---

### 3. ProductManager_agent_20250702_211722.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/resources/state_history/ProductManager_agent_20250702_211722.json`
**Last Modified:** 2025-07-02T21:18:28.293416
**Messages:** 62

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline...
- system: Start the 'Problem Statement' section. Provide a solid foundation for others to build on....

---

### 4. Engineer_agent_20250702_211753.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/resources/state_history/Engineer_agent_20250702_211753.json`
**Last Modified:** 2025-07-02T21:17:56.682381
**Messages:** 11

**Sample Messages:**

- system: Current Section: Product Ideas
  Your total contributions: 0
  Format: outline

Current content:
[Produc...

- system: Build upon or enhance the existing content. Be constructive and collaborative....

---

### 5. Designer_agent_20250702_211732.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/resources/state_history/Designer_agent_20250702_211732.json`
**Last Modified:** 2025-07-02T21:17:37.613788
**Messages:** 11

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline

Current content:
[Pr...

- system: Build upon or enhance the existing content. Be constructive and collaborative....

---

### 6. ProductManager_agent_20250702_210704.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history/ProductManager_agent_20250702_210704.json`
**Last Modified:** 2025-07-02T21:07:28.818221
**Messages:** 18

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline...
- system: Start the 'Problem Statement' section. Provide a solid foundation for others to build on....

---

### 7. Designer_agent_20250702_210710.json

**Type:** state_history
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history/Designer_agent_20250702_210710.json`
**Last Modified:** 2025-07-02T21:07:20.315243
**Messages:** 11

**Sample Messages:**

- system: Current Section: Problem Statement
  Your total contributions: 0
  Format: outline

Current content:
[Pr...

- system: Build upon or enhance the existing content. Be constructive and collaborative....

---

### 8. code_review.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/outputs/code_review.md`
**Last Modified:** 2025-06-16T19:18:56.168913
**Lines:** 450
**Title:** 🔍 Code Review Results:

**Preview:**

```
🔍 Code Review Results:

---

# Code Review

## Overview

[SecurityExpert]: # Overview
...
```

---

### 9. brainstorming.md

**Type:** markdown
**File:** `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/outputs/brainstorming.md`
**Last Modified:** 2025-06-16T19:18:56.168913
**Lines:** 393
**Title:** 📄 Final Brainstorming Document:

**Preview:**

```
📄 Final Brainstorming Document:

============================================================
Brainstorming: Eco-friendly smart home device ideas
===================================================

P...
```

---

## Quick Access

### View State History (JSON)

```bash
# View recent state history files
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative -name "*.json" -exec ls -la {} \;

# Pretty print JSON
cat path/to/file.json | jq '.[0].messages | length'
```

### View Conversation Outputs (Markdown)

```bash
# View markdown outputs
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/outputs -name "*.md" -exec cat {} \;
```

### Copy Files for Analysis

```bash
# Copy all outputs to a temporary directory for analysis
mkdir -p /tmp/collaberative_analysis
find /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative -name "*.json" -o -name "*.md" | xargs -I {} cp {} /tmp/collaberative_analysis/
```

## File Structure

```
collaberative/
├── outputs/           # Conversation result files (.md)
├── resources/         # State history files (.json)
│   └── state_history/
└── CONVERSATION_OUTPUTS.md  # This summary file
```
