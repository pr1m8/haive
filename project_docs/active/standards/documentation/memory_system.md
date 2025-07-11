# Memory System Core - Haive Framework

**Version**: 3.0  
**Purpose**: Core memory system architecture and principles  
**Last Updated**: 2025-01-09

## 🧠 Core Memory Principles

1. **Hierarchical Structure**: Global → Project → Package → Component
2. **Import-Based Modularity**: Use `@path/to/file` for detailed information
3. **Living Documentation**: Memory evolves with the codebase
4. **Cross-Referenced Navigation**: [MEM-XXX] tags for easy linking
5. **Global Memory Protection**: Never modify ~/.claude/CLAUDE.md without permission

## 📁 Memory Organization

### Hierarchy Structure

```
Global Memory (User Level)
├── ~/.claude/CLAUDE.md (Protected - universal patterns)
│
Project Memory (Repository Level)
├── CLAUDE.md (Central hub - routing and quick access)
├── project_docs/
│   ├── MEMORY_SYSTEM_CORE.md (This file)
│   ├── CODING_STYLE_GUIDE.md (Code standards)
│   ├── TESTING_PHILOSOPHY.md (Testing approach)
│   ├── GIT_WORKFLOW.md (Git best practices)
│   ├── claude_documentation/ (Claude-specific guides)
│   ├── claude_sessions/ (Session memories)
│   ├── progress_tracking/ (Current work status)
│   └── {package_name}/ (Package-specific docs)
```

### Memory File Types

#### **Hub Files** (Small, import-based)

- `CLAUDE.md` - Central routing and quick access
- Package `README.md` - Overview with imports to details

#### **Reference Files** (Detailed information)

- `CODING_STYLE_GUIDE.md` - Code standards and patterns
- `TESTING_PHILOSOPHY.md` - Testing methodology
- `GIT_WORKFLOW.md` - Git best practices

#### **Session Files** (Working memory)

- `claude_sessions/{session_id}/` - Session-specific memories
- `progress_tracking/current_sprint.md` - Active work status
- `claude_sessions/current_issues.md` - Active problems

## 🔗 Cross-Reference System

### Memory Tags

- `[MEM-XXX]` - Top-level memory area
- `[MEM-XXX-Y]` - Sub-area within memory
- `[MEM-XXX-Y-ZZZ]` - Specific component/file

### Navigation Pattern

```markdown
**Memory References:**

- **Parent**: [MEM-002-A] Main Project Routing
- **Related**: [MEM-004-CORE] Haive Core Package Documentation
- **Child**: [MEM-004-CORE-G-001] ReactAgent Component Analysis
- **See Also**: [MEM-005-B] Claude Quick Reference
```

## 🚨 Global Memory Protection

### Protected Files

```bash
# ❌ NEVER MODIFY without explicit permission
~/.claude/CLAUDE.md                    # Global coding principles
~/.claude/projects/{project}.md        # Project-specific patterns

# ✅ ALWAYS preserve global memory content
# ✅ ALWAYS backup before any global changes
# ✅ ALWAYS ask permission before global modifications
```

## 📏 File Size Guidelines

### Target Sizes (for performance)

- **Hub files**: <5k chars (quick loading)
- **Reference files**: <15k chars (detailed but manageable)
- **Session files**: <10k chars (working memory)
- **Component docs**: <8k chars (focused scope)

### Size Management

```bash
# Check file sizes
find project_docs/ -name "*.md" -exec wc -c {} + | sort -n

# Large file indicators (need splitting)
# >40k chars: Performance impact warning
# >20k chars: Consider splitting
# >15k chars: Review for modularity
```

## 🔄 Memory Maintenance

### Daily

- Update session memory with progress
- Mark completed todos
- Document decisions and patterns

### Weekly

- Review and consolidate duplicate information
- Update navigation documents
- Validate cross-references
- Archive completed work

### Monthly

- Audit file sizes for performance
- Reorganize if hierarchy grows complex
- Update methodology based on learnings

## 🎯 Usage Patterns

### Starting New Work

1. Read `CLAUDE.md` for current context
2. Load relevant package memory
3. Create session workspace
4. Use TodoWrite for planning

### During Development

1. Track progress in session memory
2. Document issues in `current_issues.md`
3. Save patterns for reuse
4. Cross-reference with [MEM-XXX] tags

### Completing Work

1. Update status files
2. Document learnings
3. Clean up temporary files
4. Archive session memory

## 📊 Success Metrics

### Memory Quality

- **Navigation Speed**: Find any info in <3 clicks
- **Cross-Reference Coverage**: 100% of documents linked
- **Information Currency**: Updated within 24 hours
- **File Size Performance**: No files >40k chars

### Development Efficiency

- **Context Loading**: <2 minutes to understand current state
- **Decision Speed**: Standards clearly documented
- **Knowledge Retention**: Previous work discoverable
- **Quality Consistency**: All code follows standards

---

**Remember**: Memory is our competitive advantage. Keep it organized, current, and performant.
