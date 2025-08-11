# Memory Module - Reorganized

**Status**: Work in progress - reorganizing memory functionality
**Date**: 2025-01-28

## 🏗️ Module Structure

```
memory/
├── base/           # Base classes and core interfaces
├── core/           # Core functionality (classifiers, stores, types)
├── models/         # Memory type models (semantic, episodic, procedural)
├── agents/         # Specialized memory agents
├── search/         # Search-specific agents
├── retrieval/      # Retrieval-specific agents
├── coordination/   # Multi-agent coordination
├── knowledge/      # Knowledge management
├── integrations/   # External integrations (LangMem, DeepSeek)
└── api/           # Unified public API
```

## 📋 Migration Status

This directory contains the reorganized memory functionality from:

- `memory/` - Main memory system (most mature)
- `memory_v2/` - Experimental features (token tracking, etc.)
- `ltm/` - LangMem integration
- `long_term_memory/` - Additional LTM implementation

## 🎯 Goals

1. **Single memory module** - All functionality in one place
2. **Clear organization** - Logical submodules by function
3. **Preserve features** - Token tracking, knowledge graphs, etc.
4. **Unified interface** - Simple API for all memory operations
5. **Better testing** - Proper test organization

## 🚀 Usage (Planned)

```python
# Simple usage
from haive.agents.memory import SimpleMemoryAgent

# Advanced usage
from haive.agents.memory.api import UnifiedMemoryAPI

# Specialized agents
from haive.agents.memory.search import SemanticSearchAgent
from haive.agents.memory.coordination import MultiAgentCoordinator
```

## 📝 Implementation Progress

- [x] Directory structure created
- [ ] Base classes migrated
- [ ] Core components migrated
- [ ] Agents migrated to submodules
- [ ] Tests reorganized
- [ ] Documentation updated
- [ ] Public API created
