# Supervisor Cleanup and Migration Plan

## Overview

This document outlines a step-by-step plan to clean up the supervisor implementations and organize the codebase properly.

## Current State Summary

### File Counts:

- **Test files in source directories**: ~39 files
- **Debug files**: ~6 files
- **Example/demo files**: ~10 files
- **Duplicate implementations**: ~15 files
- **Core implementations**: ~5-8 files

## Migration Plan

### Phase 1: Create Directory Structure

```bash
# Create proper directory structure
mkdir -p packages/haive-agents/tests/supervisor/experiments
mkdir -p packages/haive-agents/tests/supervisor/components
mkdir -p packages/haive-agents/tests/supervisor/integration
mkdir -p packages/haive-agents/examples/supervisor/patterns
mkdir -p packages/haive-agents/examples/supervisor/dynamic_activation
mkdir -p packages/haive-agents/docs/supervisor/patterns
```

### Phase 2: Move Test Files

#### From `/src/haive/agents/supervisor/`:

```bash
# Move test files to proper test directory
test_advanced_prebuilt.py → tests/supervisor/test_advanced_prebuilt.py
test_compatibility.py → tests/supervisor/test_compatibility.py
test_dynamic_addition_fixed.py → tests/supervisor/test_dynamic_addition_fixed.py
test_dynamic_multi_agent.py → tests/supervisor/test_dynamic_multi_agent.py
test_post_compile_addition.py → tests/supervisor/test_post_compile_addition.py
test_rebuild_verification.py → tests/supervisor/test_rebuild_verification.py
test_registry_demo.py → tests/supervisor/test_registry_demo.py
test_registry_real.py → tests/supervisor/test_registry_real.py
test_with_registry.py → tests/supervisor/test_with_registry.py
```

#### From `/src/haive/agents/experiments/supervisor/`:

```bash
# Move component tests
test_component_*.py → tests/supervisor/components/
test_dynamic_*.py → tests/supervisor/experiments/
test_multiagent_*.py → tests/supervisor/integration/
test_*.py (others) → tests/supervisor/experiments/
```

### Phase 3: Extract and Move Examples

#### High-Value Examples to Extract:

```bash
three_agent_inactive_test.py → examples/supervisor/dynamic_activation/
clean_dynamic_supervisor.py → examples/supervisor/patterns/agent_execution_node.py
dynamic_supervisor_v2.py → examples/supervisor/patterns/dynamic_tool_generation.py
component_4_dynamic_supervisor.py → examples/supervisor/patterns/state_synchronized_tools.py
```

### Phase 4: Archive Debug Files

```bash
# Create archive directory
mkdir -p packages/haive-agents/docs/supervisor/archive/debug

# Move debug files
debug_*.py → docs/supervisor/archive/debug/
```

### Phase 5: Consolidate Core Implementations

#### Keep in `/src/haive/agents/dynamic_supervisor/`:

- agent.py (main implementation)
- state.py
- tools.py
- models.py
- prompts.py
- **init**.py

#### Keep in `/src/haive/agents/supervisor/`:

- **init**.py
- registry.py (useful utility)
- integrated_supervisor.py (alternative pattern)

#### Move Documentation:

- \*.md files → docs/supervisor/

#### Remove/Archive:

- Duplicate implementations
- Incomplete experiments
- Old test runners

### Phase 6: Update Imports

After moving files, update all imports:

```python
# Old import
from haive.agents.experiments.supervisor.three_agent_inactive_test import EnhancedAgentRegistry

# New import
from haive.agents.supervisor.registry import EnhancedAgentRegistry
```

### Phase 7: Create Documentation

#### Create Pattern Documentation:

1. **Agent Execution Node Pattern** - From clean_dynamic_supervisor.py
2. **Dynamic Tool Generation** - From dynamic_supervisor_v2.py
3. **Capability-Based Activation** - From three_agent_inactive_test.py
4. **State-Synchronized Tools** - From component implementations

#### Create Usage Examples:

1. Basic supervisor usage
2. Dynamic agent activation
3. Multi-agent coordination
4. Custom routing strategies

## Implementation Script

```python
#!/usr/bin/env python3
"""Script to migrate supervisor files to proper locations."""

import os
import shutil
from pathlib import Path

def migrate_supervisor_files():
    """Migrate supervisor files to proper locations."""

    base_path = Path("packages/haive-agents")

    # Define migrations
    migrations = {
        # Test files from supervisor
        "src/haive/agents/supervisor/test_*.py": "tests/supervisor/",

        # Test files from experiments
        "src/haive/agents/experiments/supervisor/test_component_*.py": "tests/supervisor/components/",
        "src/haive/agents/experiments/supervisor/test_*.py": "tests/supervisor/experiments/",

        # Debug files
        "src/haive/agents/experiments/supervisor/debug_*.py": "docs/supervisor/archive/debug/",

        # Examples
        "src/haive/agents/experiments/supervisor/three_agent_inactive_test.py":
            "examples/supervisor/dynamic_activation/dynamic_activation_example.py",
    }

    # Execute migrations
    for pattern, destination in migrations.items():
        # Implementation here
        pass

if __name__ == "__main__":
    migrate_supervisor_files()
```

## Validation Steps

After migration:

1. **Run all tests** to ensure nothing broke
2. **Check imports** in all files
3. **Update documentation** with new paths
4. **Verify examples** still work
5. **Clean up empty directories**

## Benefits After Cleanup

1. **Clear separation** between source, tests, and examples
2. **No test files** in source directories
3. **Documented patterns** for future reference
4. **Cleaner imports** and dependencies
5. **Easier navigation** for developers

## Timeline

- Phase 1-2: Move test files (1 hour)
- Phase 3-4: Extract examples and archive (2 hours)
- Phase 5: Consolidate implementations (2 hours)
- Phase 6: Update imports (1 hour)
- Phase 7: Create documentation (2 hours)

Total estimated time: 8 hours

## Next Steps

1. Review and approve this plan
2. Create backup of current state
3. Execute migration script
4. Run full test suite
5. Update CI/CD if needed
6. Document new structure in README
