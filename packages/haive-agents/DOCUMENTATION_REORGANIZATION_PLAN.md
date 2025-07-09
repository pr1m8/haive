# Documentation Reorganization Plan

## Current State Analysis

### Issues Identified

1. **81 README files** in haive-agents - many with minimal content
2. **Multiple overlapping documents** (Multi-Agent has 3 different READMEs)
3. **Scattered standalone .md files** at various levels
4. **Inconsistent naming** (README.md vs readme.md)
5. **Output examples mixed with source code**
6. **Historical files not archived**
7. **System analysis docs at wrong levels**

## Proposed New Structure

```
packages/
├── haive-agents/
│   ├── README.md (Main package overview)
│   ├── docs/ (NEW - Centralized documentation)
│   │   ├── architecture/
│   │   │   ├── system-analysis.md
│   │   │   ├── agent-patterns.md
│   │   │   └── improvement-plan.md
│   │   ├── guides/
│   │   │   ├── getting-started.md
│   │   │   ├── multi-agent-development.md
│   │   │   ├── rag-implementation.md
│   │   │   └── testing-patterns.md
│   │   ├── api/
│   │   │   ├── base-agents.md
│   │   │   ├── conversation-agents.md
│   │   │   ├── rag-agents.md
│   │   │   └── specialized-agents.md
│   │   └── examples/
│   │       ├── conversation-outputs/
│   │       ├── implementation-examples/
│   │       └── testing-examples/
│   └── src/haive/agents/
│       ├── README.md (Agent overview with links to docs/)
│       ├── base/
│       │   └── README.md (Focused on base classes only)
│       ├── conversation/
│       │   └── README.md (Links to main docs)
│       └── [other agent categories]/
│           └── README.md (Brief + links to docs/)
├── haive-core/
│   ├── README.md (Core package overview)
│   ├── docs/ (NEW - Core-specific docs)
│   │   ├── architecture/
│   │   ├── api/
│   │   └── guides/
│   └── src/
└── docs/ (NEW - Project-wide documentation)
    ├── README.md (Documentation index)
    ├── architecture/
    │   ├── overview.md
    │   ├── core-concepts.md
    │   └── system-design.md
    ├── user-guides/
    │   ├── quickstart.md
    │   ├── agent-development.md
    │   └── advanced-patterns.md
    └── developer-guides/
        ├── contributing.md
        ├── testing.md
        └── architecture-decisions.md
```

## Implementation Steps

### Phase 1: Create New Structure

1. Create `docs/` directories at package and project levels
2. Create standardized templates for different doc types
3. Set up clear documentation hierarchy

### Phase 2: Consolidate Redundant Documentation

1. Merge 3 multi-agent docs into single comprehensive guide
2. Consolidate implementation status documents
3. Combine related RAG documentation

### Phase 3: Reorganize and Standardize

1. Move system analysis docs to appropriate architecture sections
2. Relocate output examples to examples directories
3. Archive historical documentation
4. Standardize all README formats

### Phase 4: Streamline Module READMEs

1. Convert detailed module READMEs to brief overviews + links
2. Maintain only essential information at module level
3. Create clear navigation paths to detailed docs

### Phase 5: Create Navigation and Cross-references

1. Add clear navigation in main READMEs
2. Create cross-reference links between related docs
3. Ensure no information is lost in reorganization

## Documentation Standards

### README.md Template (Module Level)

```markdown
# [Module Name]

Brief description (1-2 sentences)

## Quick Start

Basic usage example

## Available Components

- Component 1 - Brief description
- Component 2 - Brief description

## Documentation

- [Detailed Guide](../../docs/guides/module-guide.md)
- [API Reference](../../docs/api/module-api.md)
- [Examples](../../docs/examples/module-examples.md)

## See Also

- Related modules
- External resources
```

### Documentation File Template

```markdown
# [Title]

## Overview

What this document covers

## Table of Contents

Auto-generated or manual TOC

## Content sections...

## Related Documentation

Links to related docs

## Last Updated

Date and version info
```

## Migration Rules

### What to Keep

- All unique technical content
- Code examples and patterns
- API documentation
- Implementation guides

### What to Consolidate

- Overlapping explanations
- Multiple versions of same information
- Scattered implementation details

### What to Archive

- Historical versions (move to archive/)
- Outdated implementation details
- Superseded documentation

### What to Remove

- Empty or placeholder READMEs
- Duplicate content with no added value
- Broken or outdated examples

## Success Criteria

1. **Single Source of Truth** - No duplicate information
2. **Clear Navigation** - Easy to find relevant documentation
3. **Consistent Format** - All docs follow same structure
4. **Maintainable** - Easy to update and keep current
5. **Complete Coverage** - All features documented
6. **Accessible** - Clear entry points for different user types
