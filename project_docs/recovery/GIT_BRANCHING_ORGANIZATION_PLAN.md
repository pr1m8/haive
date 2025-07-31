# Git Branching Strategy for haive-core and haive-agents Organization

**Date**: 2025-01-21  
**Purpose**: Organize node system and submodules with proper git branching

## 🎯 **Strategy Overview**

We'll create feature branches for organizing different parts of the codebase into proper submodules with clean `__init__.py` files for Sphinx AutoAPI.

## 🌿 **Branch Structure**

### Main Branches

- `main` - Production ready code
- `develop` - Integration branch for all feature work

### Feature Branches for Organization

#### haive-core Organization

```bash
# Core node system cleanup
feature/haive-core-node-system-organization
├── feature/core-base-nodes           # Base node classes and configs
├── feature/core-engine-nodes         # Engine node submodule
├── feature/core-agent-nodes          # Agent node submodule
├── feature/core-validation-nodes     # Validation node submodule
├── feature/core-composer-nodes       # Field mapping composer submodule
└── feature/core-node-utils           # Node utilities and factories
```

#### haive-agents Organization

```bash
# Agent system cleanup
feature/haive-agents-organization
├── feature/agents-base-refactor      # Clean base agent class
├── feature/agents-simple-cleanup     # SimpleAgent organization
├── feature/agents-multi-enhanced     # Enhanced multi-agent system
├── feature/agents-rag-organization   # RAG agents submodule
└── feature/agents-field-coordination # Multi-agent field mapping
```

#### Documentation and API

```bash
# Sphinx AutoAPI optimization
feature/sphinx-autoapi-organization
├── feature/core-api-docs            # haive-core API documentation
├── feature/agents-api-docs          # haive-agents API documentation
└── feature/api-examples-cleanup     # Clean up examples for AutoAPI
```

## 📋 **Implementation Plan**

### Phase 1: Core Node System (haive-core)

#### Step 1.1: Create Base Branch

```bash
# Create main organization branch
git checkout -b feature/haive-core-node-system-organization

# Create submodule branches
git checkout -b feature/core-base-nodes
git checkout -b feature/core-engine-nodes
git checkout -b feature/core-agent-nodes
git checkout -b feature/core-validation-nodes
git checkout -b feature/core-composer-nodes
git checkout -b feature/core-node-utils
```

#### Step 1.2: Base Nodes Organization

```bash
# Work on base nodes
git checkout feature/core-base-nodes

# Create submodule structure
mkdir -p packages/haive-core/src/haive/core/graph/node/base
mkdir -p packages/haive-core/src/haive/core/graph/node/engine
mkdir -p packages/haive-core/src/haive/core/graph/node/agent
mkdir -p packages/haive-core/src/haive/core/graph/node/validation
mkdir -p packages/haive-core/src/haive/core/graph/node/composer
mkdir -p packages/haive-core/src/haive/core/graph/node/utils

# Move and organize files
mv packages/haive-core/src/haive/core/graph/node/base_config.py \
   packages/haive-core/src/haive/core/graph/node/base/config.py

mv packages/haive-core/src/haive/core/graph/node/types.py \
   packages/haive-core/src/haive/core/graph/node/base/types.py
```

#### Step 1.3: Engine Nodes Submodule

```bash
git checkout feature/core-engine-nodes

# Organize engine node files
mv packages/haive-core/src/haive/core/graph/node/engine_node.py \
   packages/haive-core/src/haive/core/graph/node/engine/node.py

mv packages/haive-core/src/haive/core/graph/node/engine_node_generic.py \
   packages/haive-core/src/haive/core/graph/node/engine/generic.py
```

#### Step 1.4: Agent Nodes Submodule

```bash
git checkout feature/core-agent-nodes

# Organize agent node files
mv packages/haive-core/src/haive/core/graph/node/agent_node_v3.py \
   packages/haive-core/src/haive/core/graph/node/agent/node_v3.py

mv packages/haive-core/src/haive/core/graph/node/multi_agent_node.py \
   packages/haive-core/src/haive/core/graph/node/agent/multi_agent.py
```

#### Step 1.5: Validation Nodes Submodule

```bash
git checkout feature/core-validation-nodes

# Organize validation files
mv packages/haive-core/src/haive/core/graph/node/validation_node_*.py \
   packages/haive-core/src/haive/core/graph/node/validation/

mv packages/haive-core/src/haive/core/graph/node/routing_validation_node.py \
   packages/haive-core/src/haive/core/graph/node/validation/routing.py
```

#### Step 1.6: Composer Submodule (Already Good!)

```bash
git checkout feature/core-composer-nodes

# The composer/ directory already exists and is well organized
# Just need to add proper __init__.py files
```

### Phase 2: Agent System (haive-agents)

#### Step 2.1: Agents Base Refactor

```bash
git checkout -b feature/agents-base-refactor

# Clean up base agent
# Add proper field mapping integration
# Create clean public API
```

#### Step 2.2: Enhanced Multi-Agent

```bash
git checkout -b feature/agents-multi-enhanced

# Move enhanced multi-agent files to proper submodule
mkdir -p packages/haive-agents/src/haive/agents/multi/enhanced
mv packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py \
   packages/haive-agents/src/haive/agents/multi/enhanced/agent.py
```

### Phase 3: Create Proper **init**.py Files

#### Step 3.1: Core Node System **init**.py

```bash
# Create comprehensive __init__.py files for each submodule

# packages/haive-core/src/haive/core/graph/node/base/__init__.py
# packages/haive-core/src/haive/core/graph/node/engine/__init__.py
# packages/haive-core/src/haive/core/graph/node/agent/__init__.py
# packages/haive-core/src/haive/core/graph/node/validation/__init__.py
# packages/haive-core/src/haive/core/graph/node/composer/__init__.py
# packages/haive-core/src/haive/core/graph/node/utils/__init__.py
```

#### Step 3.2: Main Node **init**.py

```bash
# Create master __init__.py that imports from all submodules
# packages/haive-core/src/haive/core/graph/node/__init__.py
```

## 🔄 **Branching Workflow**

### Daily Workflow

```bash
# Start work on specific component
git checkout feature/core-engine-nodes

# Make changes to engine node files
# ... edit files ...

# Commit changes
git add .
git commit -m "refactor(core): organize engine nodes into submodule"

# Merge into main organization branch
git checkout feature/haive-core-node-system-organization
git merge feature/core-engine-nodes

# Continue with next component
git checkout feature/core-agent-nodes
# ... work on agent nodes ...
```

### Integration Workflow

```bash
# When all submodule branches are ready
git checkout feature/haive-core-node-system-organization

# Merge all feature branches
git merge feature/core-base-nodes
git merge feature/core-engine-nodes
git merge feature/core-agent-nodes
git merge feature/core-validation-nodes
git merge feature/core-composer-nodes
git merge feature/core-node-utils

# Test integration
poetry run pytest packages/haive-core/tests/

# Create PR to develop
gh pr create --title "feat(core): organize node system into submodules" --base develop
```

## 📁 **Target Directory Structure**

### haive-core Final Structure

```
packages/haive-core/src/haive/core/graph/node/
├── __init__.py                    # Main public API
├── base/                          # Base classes and types
│   ├── __init__.py
│   ├── config.py                  # Base node config (was base_config.py)
│   ├── node.py                    # Abstract base node
│   └── types.py                   # Node types and enums
├── engine/                        # Engine-based nodes
│   ├── __init__.py
│   ├── node.py                    # Main EngineNode (was engine_node.py)
│   ├── generic.py                 # Generic engine node (was engine_node_generic.py)
│   └── config.py                  # Engine node configuration
├── agent/                         # Agent-based nodes
│   ├── __init__.py
│   ├── node_v3.py                 # AgentNodeV3 (was agent_node_v3.py)
│   ├── multi_agent.py            # Multi-agent node (was multi_agent_node.py)
│   └── config.py                  # Agent node configuration
├── validation/                    # Validation and routing
│   ├── __init__.py
│   ├── routing.py                 # Routing validation (was routing_validation_node.py)
│   ├── stateful.py               # Stateful validation (consolidated)
│   └── unified.py                # Unified validation (was unified_validation_node.py)
├── composer/                      # Field mapping and composition (already good!)
│   ├── __init__.py
│   ├── field_mapping.py
│   ├── node_schema_composer.py
│   └── ...
└── utils/                         # Utilities and factories
    ├── __init__.py
    ├── factory.py                 # Node factories (was factory.py)
    ├── registry.py               # Node registry (was registry.py)
    └── helpers.py                # Utility functions (consolidated)
```

### haive-agents Final Structure

```
packages/haive-agents/src/haive/agents/
├── __init__.py                    # Main agents API
├── base/                          # Base agent classes
│   ├── __init__.py
│   ├── agent.py                  # Clean base agent
│   └── node_integration.py      # Node system integration
├── simple/                        # Simple agents
│   ├── __init__.py
│   ├── agent.py                  # Cleaned up SimpleAgent
│   └── config.py                 # Simple agent configuration
├── multi/                         # Multi-agent systems
│   ├── __init__.py
│   ├── enhanced/                 # Enhanced multi-agent
│   │   ├── __init__.py
│   │   ├── agent.py             # EnhancedMultiAgent (was enhanced_multi_agent_v3.py)
│   │   ├── field_coordination.py # Multi-agent field mapping
│   │   └── examples.py          # Usage examples
│   └── archive/                  # Legacy implementations
├── rag/                           # RAG agents (already well organized)
│   ├── __init__.py
│   ├── simple/
│   ├── base/
│   └── ...
└── examples/                      # Package-level examples
    ├── __init__.py
    ├── field_mapping_examples.py
    └── multi_agent_examples.py
```

## 🎯 **Benefits for Sphinx AutoAPI**

### Better Module Discovery

- **Clear submodules**: AutoAPI will find and document each submodule separately
- **Proper imports**: Clean `__init__.py` files expose the right public API
- **Logical grouping**: Related functionality grouped together

### Improved Documentation

- **Module pages**: Each submodule gets its own documentation page
- **Clear navigation**: Users can find specific functionality easily
- **API reference**: Clean API with proper imports and exports

### Example AutoAPI Output

```
haive.core.graph.node
├── base module
│   ├── config.NodeConfig
│   └── types.NodeType
├── engine module
│   ├── node.EngineNodeConfig
│   └── config.EngineNodeSettings
├── agent module
│   ├── node_v3.AgentNodeV3
│   └── multi_agent.MultiAgentNode
└── composer module
    ├── field_mapping.FieldMapping
    └── node_schema_composer.NodeSchemaComposer
```

## 🚀 **Getting Started**

### Step 1: Create Organization Branches

```bash
# Create main feature branch
git checkout -b feature/node-system-organization

# Start with core base nodes
git checkout -b feature/core-base-nodes
```

### Step 2: Begin Organization

```bash
# Create directory structure
mkdir -p packages/haive-core/src/haive/core/graph/node/{base,engine,agent,validation,utils}

# Start moving files to proper locations
# ... organize files ...

# Create __init__.py files with proper imports
# ... create init files ...
```

This branching strategy will let us organize everything properly while maintaining clean git history and allowing parallel work on different submodules!
