# Claude Sessions - Smart Memory Management

This directory contains Claude Code's session workspaces for agent development. Each session represents a focused development effort with its own memory and context.

## Purpose

The session-based approach provides:

- **Persistent Memory**: Context maintained across conversations
- **Organized Development**: Structured approach to agent creation
- **Knowledge Building**: Reusable patterns and solutions
- **Issue Tracking**: Document and solve problems systematically

## Creating a New Session

```bash
# Generate session ID
session_id="claude_$(date +%Y%m%d_%H%M%S)_<purpose>"

# Create workspace structure
mkdir -p "project_docs/claude_sessions/${session_id}"/{memory,agents,references}

# Start with SESSION_INFO.md
```

## Session Structure

```
claude_sessions/
├── claude_YYYYMMDD_HHMMSS_purpose/
│   ├── SESSION_INFO.md          # Overview and goals
│   ├── memory/
│   │   ├── context.md          # Current working context
│   │   ├── decisions.md        # Design decisions made
│   │   └── issues.md           # Problems and solutions
│   ├── agents/
│   │   ├── {agent_name}/       # Per-agent development
│   │   └── patterns.md         # Reusable patterns
│   └── references/
│       ├── code_snippets.md    # Useful code examples
│       └── dependencies.md     # Package dependencies
└── README.md (this file)
```

## Best Practices

1. **Start Each Session**: Create SESSION_INFO.md with clear goals
2. **Update Context**: Keep memory/context.md current with what you're working on
3. **Document Decisions**: Record why you chose specific approaches
4. **Track Issues**: Document problems and their solutions
5. **Extract Patterns**: Move reusable code to references/

## Example Sessions

- `claude_20250106_131930_example/` - Demonstration of structure
- `claude_YYYYMMDD_HHMMSS_rag_agent/` - RAG agent development
- `claude_YYYYMMDD_HHMMSS_tool_integration/` - Tool system work

## Session Lifecycle

1. **Creation**: Start when beginning new agent or feature
2. **Active Development**: Update memory files as you work
3. **Completion**: Mark objectives complete in SESSION_INFO.md
4. **Archive**: Keep for future reference and pattern extraction

## Tips for Claude Code

When starting agent development:

1. Create a new session workspace
2. Define clear objectives in SESSION_INFO.md
3. Use memory/context.md to track current focus
4. Document decisions and rationale
5. Save useful code snippets for reuse
6. Extract patterns for future agents

Remember: Your memory is your strength! Use these workspaces to build knowledge over time.
