# Documentation Issues & Status

**Date**: 2025-01-08
**Purpose**: Track documentation build issues and import failures

## Import Failures

These modules are failing to import during documentation build:

### High Priority Failures

1. **haive.agents.reasoning_and_critique.reflection**
   - Missing module or incorrect import path
   - Should be: `haive.agents.reasoning_and_critique.reflexion` (typo?)

2. **haive.agents.rag.self_rag**
   - Module not found in the rag directory
   - May need to be implemented or is misnamed

3. **haive.tools.utility**
   - ❌ CONFIRMED: Does not exist in tools package
   - Tools are organized under `tools/` and `toolkits/` directories
   - No centralized utility module

4. **haive.core.schema.compatibility**
   - Missing from schema module
   - May be deprecated or moved

5. **haive.agents.planning.llm_compiler**
   - Not found in planning agents
   - Check if this is implemented

6. **haive.tools.api**
   - ❌ CONFIRMED: Does not exist in tools package
   - API-related tools are in `toolkits/{service_name}/` directories
   - No centralized API module

### Additional Known Issues
- **haive.agents.conversation.collaborative** (misspelled - should be "collaborative")
- **haive.agents.reasoning_and_critique.mcts** - Import path issue
- **haive.tools.code** - ❌ CONFIRMED: Does not exist (code tools are in `toolkits/dev/`)
- **haive.agents.supervisor** - Various supervisor examples failing

### Tools Package Structure (DISCOVERED)

The haive-tools package is organized as:

```
haive-tools/src/haive/tools/
├── __init__.py (exports only: arxiv, duckduckgo, google search)
├── tools/        # Individual tool implementations
│   ├── arxiv.py
│   ├── duckduckgo_search.py
│   └── google/   # Google-specific tools
└── toolkits/     # Tool collections
    ├── base.py   # Base toolkit classes
    └── dev/      # Development tools (where code tools actually are!)
        ├── tools.py (AST code editing)
        ├── python/  # Python-specific tools
        └── shell/   # Shell operation tools
```

**Key Finding**: Code-related tools are in `toolkits/dev/`, not in a top-level `code` module!

## Current Documentation Structure

### Working Well ✅
- Main navigation with beautiful gradients
- Agent gallery with code examples
- Agent showcase with interactive cards
- Game demos with playable interfaces
- JavaScript visualization system (graph, state, execution trace)
- CSS styling and overrides

### Issues to Fix ❌
1. Import failures causing build warnings
2. Long build times (needs optimization)
3. CSS file redundancy (15+ CSS files)
4. Some missing guide pages referenced in toctrees

## Examples Location Reference

Examples are distributed throughout the codebase:

- **Agent Examples**: `packages/haive-agents/examples/`
- **Individual Agent Examples**: Each agent has `example.py` in its module
- **Game Examples**: `packages/haive-games/examples/`
- **Core Examples**: `packages/haive-core/examples/`
- **MCP Examples**: `packages/haive-mcp/examples/`

## Next Steps

1. Fix typos in import paths (reflection → reflexion)
2. Check if missing modules need to be implemented
3. Add autodoc_mock_imports for truly missing modules
4. Optimize build performance
5. Consolidate CSS files

## Build Commands

```bash
# Start documentation server
cd /home/will/Projects/haive/backend/haive/docs
./start_docs.sh start

# Check status
./start_docs.sh status

# View logs
./start_docs.sh logs

# Manual build
poetry run sphinx-build -b html source _build/html
```

## Notes

- Documentation is served at http://localhost:8003
- Autobuild watches for changes and rebuilds automatically
- Current PID tracking in docs_server.pid