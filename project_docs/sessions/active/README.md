# Active Sessions - Claude Code Working Memory

**Purpose**: Current Claude Code session tracking and working memory  
**Last Updated**: 2025-01-09

## 📊 Current Status

### 🚨 Active Issues
- **File**: [current_issues.md](current_issues.md)
- **Purpose**: Track active development problems and blockers
- **Updated**: Continuously during development

### 🎯 Current Sprint
- **File**: [current_sprint.md](current_sprint.md)
- **Purpose**: Track sprint progress and goals
- **Updated**: Daily during active development

### 📝 Session Folders
Individual session workspaces for specific development tasks:

```
sessions/active/
├── current_issues.md          # Active problems tracking
├── current_sprint.md          # Sprint progress
└── claude_YYYYMMDD_HHMMSS_purpose/  # Individual sessions
    ├── SESSION_INFO.md        # Session metadata
    ├── memory/               # Session memory files
    │   ├── context.md        # Working context
    │   ├── decisions.md      # Design decisions
    │   └── issues.md         # Session-specific issues
    └── references/           # Session references
        └── code_snippets.md  # Useful code examples
```

## 🎯 Using Active Sessions

### Starting New Work
1. **Check current issues**: Review [current_issues.md](current_issues.md)
2. **Review sprint**: Check [current_sprint.md](current_sprint.md)
3. **Create session**: Use TodoWrite to plan work
4. **Document progress**: Update session memory as you work

### During Development
- **Track issues**: Add problems to [current_issues.md](current_issues.md)
- **Update progress**: Mark completed items in [current_sprint.md](current_sprint.md)
- **Document decisions**: Record choices in session memory
- **Cross-reference**: Link related sessions and issues

### Completing Work
- **Update status**: Mark issues resolved or todos complete
- **Document outcomes**: Record learnings and patterns
- **Archive session**: Move completed sessions to [archive](../archive/)
- **Clean up**: Remove temporary files and outdated information

## 📋 Session Management

### Active Session Guidelines
- **One session per major task**: Keep sessions focused
- **Regular updates**: Update memory files as you progress
- **Clear documentation**: Write for future reference
- **Cross-reference**: Link to related issues and sessions

### Memory Structure
```markdown
# Session Memory Template

## Current Focus
- Working on: [specific component/feature]
- Goal: [clear objective]
- Status: [current progress]

## Key Decisions
- Decision 1: [rationale]
- Decision 2: [rationale]

## Issues Encountered
- Issue 1: [description and resolution]
- Issue 2: [description and status]

## Next Steps
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
```

## 🔗 Related Documentation

### Project Standards
- **Memory System**: [Memory System](../active/standards/documentation/memory_system.md)
- **Development Workflow**: [Development Workflow](../active/standards/coding/development_workflow.md)
- **Documentation Standards**: [Documentation Standards](../active/standards/documentation/)

### Session Archive
- **Completed Sessions**: [Archive](../archive/)
- **Historical Context**: Previous session learnings
- **Pattern Library**: Reusable solutions from past sessions

---

**Note**: Active sessions are working memory - keep them current and actionable. Archive completed sessions regularly to maintain clarity.