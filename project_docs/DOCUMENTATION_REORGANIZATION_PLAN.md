# Documentation Reorganization Plan

## Overview
This plan outlines the reorganization of Haive's documentation to eliminate duplicates, establish clear hierarchy, and improve navigation.

## Current Issues
1. **Duplicate Files**: Multiple versions of CLAUDE.md, frontend integration guides, RAG documentation
2. **Scattered Documentation**: Architecture docs spread across multiple directories
3. **Inconsistent Organization**: Mix of user docs and developer notes in same locations
4. **Dead References**: CLAUDE.md points to non-existent files in /project_docs/claude_documentation/
5. **Legacy Content**: Outdated documentation in legacy directories

## Proposed Structure

### 1. `/docs/` - User-Facing Documentation
```
/docs/
├── README.md                    # Documentation overview for users
├── source/                      # Sphinx source files
│   ├── index.rst               # Main documentation index
│   ├── getting_started.rst     # Quick start guide
│   ├── api/                    # API reference documentation
│   ├── guides/                 # User guides
│   │   ├── agents.rst          # Agent development guide
│   │   ├── tools.rst           # Tool usage guide
│   │   ├── games.rst           # Game development guide
│   │   └── frontend.rst        # Frontend integration guide
│   ├── examples/               # Code examples
│   └── _static/                # Static assets
└── build/                      # Generated documentation
```

### 2. `/project_docs/` - Developer Documentation
```
/project_docs/
├── README.md                    # Developer notes overview
├── DOCUMENTATION_STANDARDS.md   # Documentation writing standards
├── architecture/               # Architecture design decisions
│   ├── README.md
│   ├── schema_design/          # Schema architecture decisions
│   ├── agent_design/           # Agent system design
│   └── component_design/       # Component architecture
├── analysis/                   # Technical analysis
│   ├── agent_analysis/         # Agent implementation analysis
│   ├── performance/            # Performance analysis
│   └── issues/                 # Issue tracking and solutions
├── claude_documentation/       # Claude-specific documentation
│   ├── CLAUDE_QUICKREF.md     # Quick reference
│   ├── CLAUDE_AGENTS.md       # Agent documentation hub
│   └── templates/              # Documentation templates
└── archive/                    # Archived/legacy documentation
```

### 3. Package Documentation
```
/packages/{package-name}/
├── README.md                    # Package overview and usage
├── docs/                       # Package-specific technical docs
│   └── implementation.md       # Implementation details
└── examples/                   # Package examples
```

## Migration Tasks

### Phase 1: Clean Up Duplicates
1. **CLAUDE.md Files**
   - Keep: `/home/will/Projects/haive/backend/haive/CLAUDE.md`
   - Remove: `/project_docs/CLAUDE.md`, `/packages/haive-dataflow/docs/CLAUDE.md`

2. **Frontend Integration**
   - Merge: `FRONTEND_INTEGRATION_GUIDE.md` and `FRONTEND_INTEGRATION_GUIDANCE.md`
   - Location: `/docs/source/guides/frontend.rst`

3. **RAG Documentation**
   - Keep implementation details in: `/packages/haive-agents/src/haive/agents/rag/`
   - Move analysis to: `/project_docs/analysis/agent_analysis/`
   - Create user guide in: `/docs/source/guides/rag.rst`

### Phase 2: Reorganize Structure
1. **Architecture Documentation**
   - Move design decisions to: `/project_docs/architecture/`
   - Keep user-facing architecture in: `/docs/source/guides/architecture.rst`

2. **Schema Documentation**
   - Consolidate 19 schema files into 2-3 comprehensive documents
   - Archive outdated analyses

3. **Agent Documentation**
   - Create central hub: `/project_docs/claude_documentation/CLAUDE_AGENTS.md`
   - Link to specific implementations

### Phase 3: Update References
1. Update CLAUDE.md with correct paths
2. Fix all internal documentation links
3. Update noxfile.py if paths change
4. Update package imports/references

### Phase 4: Archive Legacy Content
1. Move `/docs/source/reference/legacy_*` to `/project_docs/archive/`
2. Archive outdated schema analyses
3. Remove duplicate discovery logs

## Implementation Order
1. Create new directory structure
2. Move and consolidate documentation files
3. Update all references and links
4. Test documentation build with nox
5. Commit changes with clear message

## Success Criteria
- No duplicate documentation files
- Clear separation between user and developer docs
- All links in CLAUDE.md work correctly
- Documentation builds without warnings
- Improved navigation and discoverability