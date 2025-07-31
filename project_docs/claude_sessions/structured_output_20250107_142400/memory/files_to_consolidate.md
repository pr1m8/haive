# Files to Consolidate

## Supervisor Demo Files (Created Today)

These were created while trying to demonstrate autonomous supervisor capabilities:

### Examples Directory

```
packages/haive-agents/examples/
├── autonomous_supervisor_demo.py          # First attempt - has import errors
├── simple_autonomous_supervisor.py        # Simplified version - partially works
├── supervisor_step_by_step_demo.py        # Step-by-step attempt - registry errors
└── working_autonomous_demo.py             # Latest attempt - runs but verbose
```

### Experiments Directory

```
packages/haive-agents/src/haive/agents/experiments/
└── dynamic_supervisor_enhanced.py         # Enhanced supervisor class - init issues
```

## Navigation Files (Successfully Created)

These are working and should be kept:

### Documentation Scripts

```
docs/source/
├── restructure_navigation.py              # ✅ Creates new haive-based structure
├── update_sidebar_structure.py            # ✅ Updates main index
├── generate_package_docs.py               # ✅ Original package doc generator
└── NAVIGATION_STRUCTURE.md                # ✅ Documents the new structure
```

### Static Assets

```
docs/source/_static/
├── contextual-navigation.js               # ✅ Updated for new URLs
└── haive-navigation.css                   # ✅ New navigation styles
```

## Action Plan

1. **Keep**: All navigation-related files (they work)
2. **Consolidate**: All supervisor demos into ONE working example
3. **Location**: Move demos to `project_docs/claude_sessions/structured_output_20250107_142400/consolidated_demos/`
