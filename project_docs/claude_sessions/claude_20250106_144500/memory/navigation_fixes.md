# Navigation Fixes Applied

## Issue: Mixed Documentation Paths

**Problem**: haive-core.rst had mixed references pointing to both working `modules/` directory and broken `generated/` directory, causing navigation confusion.

## Changes Made

### 1. Gallery Card Links Fixed

- Changed `generated/haive.core.graph` → `modules/haive.core.graph`

### 2. All Toctree References Updated

**Core Components Section**:

- Removed references to non-existent `generated/haive.core` and `generated/haive.core.utils`
- Updated all paths from `generated/` to `modules/`
- Simplified to only include modules we have created

**Engine System Section**:

- Simplified from 4 submodule references to single `modules/haive.core.engine`
- Removed broken paths to engine.base, engine.engine, engine.aug_llm, engine.protocol

**Graph System Section**:

- Simplified from 4 submodule references to single `modules/haive.core.graph`
- Removed broken paths to graph.state, graph.nodes, graph.edges, graph.builder

**Schema System Section**:

- Simplified from 4 submodule references to single `modules/haive.core.schema`
- Removed broken paths to schema.state_schema, schema.schema_composer, etc.

**Detailed Module Structure**:

- Updated from single `generated/haive.core` to explicit list of working modules

## Result

- All sidebar navigation now points to working manual module pages
- No more broken links to autosummary-generated stubs
- Consistent navigation experience across all API documentation
- Users can no longer accidentally navigate to broken `/api/generated/` URLs

## Next Steps for Other Packages

Apply same pattern to:

- haive-agents.rst
- haive-tools.rst
- haive-games.rst
- haive-mcp.rst
- All other API documentation files

Each should have:

1. Gallery cards pointing to `modules/` directory
2. Toctree entries pointing to manual module pages only
3. No references to autosummary `generated/` directory
