# Haive Documentation Guide

## Quick Commands

### Auto-rebuild (Best for Development)

```bash
cd docs
make livehtml
```

Opens browser at http://localhost:8003 and auto-rebuilds on changes.

### Manual Build

```bash
make html        # Quick build
make clean html  # Full rebuild
```

## Documentation Philosophy

### What Gets a Showcase Page?

✅ **Yes - Visual/Interactive Components**:

- Games with playable UI
- Agents with graph visualization
- Components with state tracking
- Interactive demos

❌ **No - Pure API/Code**:

- Utility modules
- Configuration classes
- Basic helper functions
- Simple data structures

### Proper Linking

**Showcase → Demo Pages**:

```rst
.. grid-item-card:: 🤖 ReAct Agent
   :link: /agents/demos/react-visualization
   :link-type: doc

   See reasoning + acting in real-time
```

**NOT Showcase → Generic API**:

```rst
.. grid-item-card:: 🤖 All Agents
   :link: /api/haive-agents  ❌ Too generic!
```

**API Docs → Related Showcase**:

```rst
.. seealso::
   - :doc:`/agents/demos/react-visualization` - Interactive demo
   - :doc:`/examples/react-agent` - Code examples
```

## Fix Current Issues

1. **Games showcase cards** should link to:
   - Individual game demo pages
   - OR specific game API docs
   - NOT generic `/api/haive-games`

2. **Agent showcase** should show:
   - Graph visualizations
   - State history
   - Execution traces
   - NOT just list all 373 agents

3. **Module pages** should:
   - Focus on API documentation
   - Link TO showcase demos where relevant
   - Include code examples
