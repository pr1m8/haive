# Conversation Agent Outputs Index

Generated: 2025-07-02T22:04:14.974828

## Available Conversation Types

### [Collaberative](./collaberative/CONVERSATION_OUTPUTS.md)

**Files:** 9
**Summary:** `./collaberative/CONVERSATION_OUTPUTS.md`

### [Round_Robin](./round_robin/CONVERSATION_OUTPUTS.md)

**Files:** 0
**Summary:** `./round_robin/CONVERSATION_OUTPUTS.md`

### [Debate](./debate/CONVERSATION_OUTPUTS.md)

**Files:** 4
**Summary:** `./debate/CONVERSATION_OUTPUTS.md`

### [Directed](./directed/CONVERSATION_OUTPUTS.md)

**Files:** 0
**Summary:** `./directed/CONVERSATION_OUTPUTS.md`

### [Social_Media](./social_media/CONVERSATION_OUTPUTS.md)

**Files:** 0
**Summary:** `./social_media/CONVERSATION_OUTPUTS.md`

### [**Pycache**](./__pycache__/CONVERSATION_OUTPUTS.md)

**Files:** 0
**Summary:** `./__pycache__/CONVERSATION_OUTPUTS.md`

## Global State History

**Location:** `packages/haive-agents/resources/state_history/`
**Conversation files:** 4

## Quick Commands

```bash
# View all conversation summaries
find packages/haive-agents/src/haive/agents/conversation -name "CONVERSATION_OUTPUTS.md" -exec cat {} \;

# Copy all conversation outputs to analysis directory
mkdir -p /tmp/conversation_analysis
find packages/haive-agents/src/haive/agents/conversation -name "*.json" -o -name "*.md" | xargs -I {} cp {} /tmp/conversation_analysis/
```
