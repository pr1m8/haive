# Master Restructuring Plan - Architecture v3.0

**Created**: 2025-01-30  
**Purpose**: Complete phase-based restructuring plan with detailed subphases  
**Timeline**: 7-8 weeks total  
**Status**: Ready for Execution

## 🎯 Executive Summary

Complete transformation of Haive from monolithic architecture to clean, modular system:

- **Current**: 50,000 LOC, 74 files, 7 monolithic classes, circular dependencies
- **Target**: 30,500 LOC, 91 files, modular components, clean interfaces
- **Approach**: Protocol-first, domain-driven, test-backed transformation

## 📊 Transformation Overview

```
┌─────────────────────────────────────────────┐
│          HAIVE ARCHITECTURE v3.0            │
├─────────────────────────────────────────────┤
│                                             │
│   Phase 0: Preparation (Week 0)            │
│   ├── Setup branches                       │
│   ├── Document current state               │
│   └── Create safety backups                │
│                    ↓                        │
│   Phase 1: Foundation (Weeks 1-2)          │
│   ├── 1.1 Protocol Contracts               │
│   ├── 1.2 Schema Modularization            │
│   └── 1.3 Testing Infrastructure           │
│                    ↓                        │
│   Phase 2: Core Systems (Weeks 3-4)        │
│   ├── 2.1 Engine Decomposition             │
│   ├── 2.2 Node Consolidation               │
│   └── 2.3 Graph Simplification             │
│                    ↓                        │
│   Phase 3: Abstractions (Weeks 5-6)        │
│   ├── 3.1 Workflow Creation                │
│   ├── 3.2 Agent Cleanup                    │
│   └── 3.3 Tool Integration                 │
│                    ↓                        │
│   Phase 4: Composition (Week 7)            │
│   ├── 4.1 MultiAgent Patterns              │
│   ├── 4.2 Integration Testing              │
│   └── 4.3 Performance Optimization         │
│                    ↓                        │
│   Phase 5: Release (Week 8)                │
│   ├── 5.1 Migration Guides                 │
│   ├── 5.2 Documentation                    │
│   └── 5.3 Coordinated Release              │
│                                             │
└─────────────────────────────────────────────┘
```

## 📅 Phase 0: Preparation (3-5 days)

### Objectives

- Set up development environment
- Create branch structure
- Document baseline metrics
- Establish safety mechanisms

### Subphases

#### 0.1 Environment Setup (Day 1)

```bash
# Create main transformation branch
git checkout -b feature/arch-v3-transformation

# Set up submodule branches
for pkg in packages/*; do
    cd $pkg
    git checkout -b feature/arch-v3
    git push -u origin feature/arch-v3
    cd ../..
done

# Update main repo
git add packages/
git commit -m "chore: initialize arch-v3 branches"
```

#### 0.2 Baseline Documentation (Day 2)

- [ ] Run metrics collection script
- [ ] Document current LOC per file
- [ ] Map circular dependencies
- [ ] Capture performance benchmarks
- [ ] Create architecture diagrams

#### 0.3 Safety Setup (Day 3)

- [ ] Create backup branches
- [ ] Set up CI/CD for arch-v3
- [ ] Configure test environments
- [ ] Document rollback procedures

### Deliverables

- ✅ Branch structure created
- ✅ Baseline metrics documented
- ✅ Safety mechanisms in place

---

## 📅 Phase 1: Foundation (Weeks 1-2)

### Objectives

- Establish protocol interfaces
- Modularize state management
- Build comprehensive testing

### Subphases

#### 1.1 Protocol Contracts (3-4 days)

**Location**: `packages/haive-core/src/haive/core/contracts/`

##### Day 1-2: Define Core Protocols

```python
# execution_contract.py
class ExecutionContract(Protocol):
    input_schema: Type[StateSchema]
    output_schema: Type[StateSchema]

    def validate_input(self, state: StateSchema) -> bool
    def validate_output(self, state: StateSchema) -> bool
    def execute(self, state: StateSchema) -> StateSchema
```

##### Day 3: Integration Protocols

- [ ] EngineProtocol
- [ ] NodeProtocol
- [ ] AgentProtocol
- [ ] GraphProtocol

##### Day 4: Validation & Testing

- [ ] Type checking with mypy
- [ ] Protocol compliance tests
- [ ] Documentation

#### 1.2 Schema Modularization (6-7 days)

**Location**: `packages/haive-core/src/haive/core/schema/`

##### Day 1-2: Core Schema Components

```python
# modular/state_data.py
class StateData:
    """Pure data container"""

# modular/state_validator.py
class StateValidator:
    """Validation logic"""

# modular/state_serializer.py
class StateSerializer:
    """Serialization logic"""
```

##### Day 3-4: Domain Schemas

- [ ] MessageSchema
- [ ] ConfigSchema
- [ ] ResultSchema
- [ ] MetadataSchema

##### Day 5-6: Schema Composition

- [ ] ComposableSchema base
- [ ] Field mapping system
- [ ] Dynamic composition

##### Day 7: Migration Layer

- [ ] Backward compatibility
- [ ] Conversion utilities
- [ ] Testing

#### 1.3 Testing Infrastructure (5-6 days)

##### Day 1-2: Hypothesis Setup

```python
# tests/property/test_contracts.py
from hypothesis import given, strategies as st

@given(st.from_type(ExecutionContract))
def test_contract_properties(contract):
    """Property-based testing"""
```

##### Day 3-4: Golden Tests

```python
# tests/golden/test_compatibility.py
def test_backward_compatibility(golden):
    old_behavior = golden.load("v2_behavior")
    new_behavior = execute_v3()
    golden.assert_compatible(old_behavior, new_behavior)
```

##### Day 5-6: Fixture Hierarchies

```python
@pytest.fixture(scope="session")
def engine_suite():
    """Complete engine testing suite"""

@pytest.fixture
def node_hierarchy():
    """Node testing hierarchy"""
```

### Deliverables

- ✅ Protocol interfaces defined
- ✅ Modular schema system
- ✅ Testing infrastructure ready

---

## 📅 Phase 2: Core Systems (Weeks 3-4)

### Objectives

- Decompose monolithic components
- Consolidate overlapping systems
- Simplify complex patterns

### Subphases

#### 2.1 Engine Decomposition (8-10 days)

**Target**: Break apart 2,647 LOC AugLLMConfig

##### Day 1-3: Extract Configurations

```python
# llm_config.py (200 LOC)
class LLMConfig:
    """Pure LLM configuration"""

# tool_config.py (250 LOC)
class ToolConfig:
    """Tool management configuration"""

# structured_output_config.py (200 LOC)
class StructuredOutputConfig:
    """Structured output configuration"""
```

##### Day 4-6: Create Managers

- [ ] ToolManager - tool lifecycle
- [ ] OutputParser - response parsing
- [ ] PromptManager - prompt handling

##### Day 7-8: Build Executor

```python
class LLMExecutor:
    def __init__(self, config, tool_mgr, output_parser):
        """Composed from focused components"""
```

##### Day 9-10: Migration & Testing

- [ ] Adapter for old AugLLMConfig
- [ ] Performance benchmarks
- [ ] Integration tests

#### 2.2 Node Consolidation (5-6 days)

**Target**: 12 node types → 4 core types

##### Day 1-2: Core Node Types

```python
# Four core types only
class ContractNode:  # Base execution
class EngineNode:    # LLM operations
class ToolNode:      # Tool execution
class RouterNode:    # Routing logic
```

##### Day 3-4: Node Behaviors

- [ ] Validation behavior
- [ ] Retry behavior
- [ ] Caching behavior
- [ ] Monitoring behavior

##### Day 5-6: Migration

- [ ] Map old nodes to new
- [ ] Create compatibility layer
- [ ] Update graphs

#### 2.3 Graph Simplification (4-5 days)

##### Day 1-2: Simple Builders

```python
# simple_builder.py (400 LOC)
class SimpleGraphBuilder:
    """Basic graph construction"""
```

##### Day 3: Graph Patterns

- [ ] Sequential pattern
- [ ] Parallel pattern
- [ ] Conditional pattern

##### Day 4-5: Testing & Documentation

- [ ] Pattern examples
- [ ] Migration guide
- [ ] Performance tests

### Deliverables

- ✅ Engine decomposed into 6 focused configs
- ✅ Nodes consolidated to 4 core types
- ✅ Graph construction simplified

---

## 📅 Phase 3: Abstractions (Weeks 5-6)

### Objectives

- Create pure orchestration layer
- Clean up agent implementations
- Integrate tool ecosystem

### Subphases

#### 3.1 Workflow Creation (5-6 days)

##### Day 1-2: Base Workflow

```python
class Workflow:
    """Pure orchestration, no LLM"""
    def __init__(self, nodes: List[Node]):
        self.graph = self._build_graph(nodes)
```

##### Day 3-4: Workflow Patterns

- [ ] Sequential workflows
- [ ] Parallel workflows
- [ ] Conditional workflows
- [ ] Loop workflows

##### Day 5-6: Integration

- [ ] State management
- [ ] Error handling
- [ ] Monitoring

#### 3.2 Agent Cleanup (6-7 days)

**Target**: 25 files → 12 focused agents

##### Day 1-2: Core Agents

```python
# Four foundational agents
class SimpleAgent(Agent):      # Basic Q&A
class ReactAgent(Agent):        # Reasoning loop
class PlannerAgent(Agent):      # Planning first
class ResearchAgent(Agent):     # Research tools
```

##### Day 3-4: Specialized Agents

- [ ] AnalyzerAgent
- [ ] WriterAgent
- [ ] CoderAgent
- [ ] ValidatorAgent

##### Day 5-6: Meta Agents

- [ ] RouterAgent
- [ ] SupervisorAgent
- [ ] OrchestratorAgent
- [ ] MemoryAgent

##### Day 7: Testing & Examples

- [ ] Agent examples
- [ ] Performance tests
- [ ] Documentation

#### 3.3 Tool Integration (3-4 days)

##### Day 1-2: Tool Registry

```python
class ToolRegistry:
    """Central tool management"""
    def register(self, tool: Tool)
    def get(self, name: str) -> Tool
    def list_available() -> List[str]
```

##### Day 3-4: Tool Categories

- [ ] Research tools
- [ ] Analysis tools
- [ ] Generation tools
- [ ] Validation tools

### Deliverables

- ✅ Pure workflow orchestration
- ✅ 12 focused agent implementations
- ✅ Unified tool system

---

## 📅 Phase 4: Composition (Week 7)

### Objectives

- Implement multi-agent patterns
- Complete integration testing
- Optimize performance

### Subphases

#### 4.1 MultiAgent Patterns (4-5 days)

##### Day 1-2: Core Patterns

```python
# Six clear patterns
class SequentialMultiAgent:     # A → B → C
class ParallelMultiAgent:        # A || B || C
class HierarchicalMultiAgent:   # Supervisor → Workers
class CollaborativeMultiAgent:  # Agents work together
class CompetitiveMultiAgent:    # Best response wins
class AdaptiveMultiAgent:       # Dynamic selection
```

##### Day 3-4: Pattern Implementation

- [ ] State coordination
- [ ] Communication protocols
- [ ] Result aggregation

##### Day 5: Testing

- [ ] Pattern validation
- [ ] Performance benchmarks
- [ ] Examples

#### 4.2 Integration Testing (3-4 days)

##### Day 1: End-to-End Tests

- [ ] Complete workflows
- [ ] Multi-agent scenarios
- [ ] Real LLM execution

##### Day 2: Performance Testing

- [ ] Latency benchmarks
- [ ] Memory profiling
- [ ] Scalability tests

##### Day 3-4: Bug Fixes

- [ ] Issue resolution
- [ ] Edge case handling
- [ ] Documentation updates

#### 4.3 Performance Optimization (2-3 days)

##### Day 1: Profiling

- [ ] Identify bottlenecks
- [ ] Memory analysis
- [ ] CPU profiling

##### Day 2-3: Optimization

- [ ] Caching strategies
- [ ] Async improvements
- [ ] Resource pooling

### Deliverables

- ✅ 6 multi-agent patterns
- ✅ Full integration tested
- ✅ Performance optimized

---

## 📅 Phase 5: Release (Week 8)

### Objectives

- Complete migration guides
- Finalize documentation
- Coordinate release

### Subphases

#### 5.1 Migration Guides (2-3 days)

##### Day 1: Breaking Changes

- [ ] Document all breaking changes
- [ ] Provide migration scripts
- [ ] Update examples

##### Day 2-3: Compatibility

- [ ] Compatibility layer testing
- [ ] Gradual migration path
- [ ] Rollback procedures

#### 5.2 Documentation (2-3 days)

##### Day 1: API Documentation

- [ ] Update all docstrings
- [ ] Generate API docs
- [ ] Review accuracy

##### Day 2-3: Guides

- [ ] Getting started guide
- [ ] Architecture overview
- [ ] Best practices

#### 5.3 Coordinated Release (2-3 days)

##### Day 1: Pre-release

- [ ] Final testing
- [ ] Version bumps
- [ ] Changelog

##### Day 2: Release

```bash
# Coordinate across all packages
for pkg in packages/*; do
    cd $pkg
    git checkout main
    git merge feature/arch-v3
    git tag v3.0.0
    git push --tags
    cd ../..
done
```

##### Day 3: Post-release

- [ ] Monitor issues
- [ ] Hotfix preparation
- [ ] Communication

### Deliverables

- ✅ Complete migration guides
- ✅ Updated documentation
- ✅ v3.0.0 released

---

## 🎯 Success Metrics

### Technical Metrics

- [ ] **39% LOC reduction** achieved
- [ ] **Zero circular dependencies**
- [ ] **<100ms agent startup time**
- [ ] **>95% test coverage**
- [ ] **All tests passing**

### Quality Metrics

- [ ] **Single responsibility** per component
- [ ] **Clean interfaces** between domains
- [ ] **Type safety** throughout
- [ ] **No monolithic files** (>1000 LOC)

### Process Metrics

- [ ] **On-time delivery** per phase
- [ ] **Zero breaking changes** without migration
- [ ] **Documentation complete** before release
- [ ] **All PRs reviewed** and approved

## 🚨 Risk Management

### High Risk Items

1. **Breaking changes** → Compatibility layer + gradual migration
2. **Performance regression** → Continuous benchmarking
3. **Submodule coordination** → Daily sync meetings
4. **Test failures** → Fix-forward approach

### Contingency Plans

- **Rollback strategy** documented for each phase
- **Feature flags** for gradual rollout
- **Hotfix process** established
- **Communication plan** for issues

## 📊 Resource Allocation

### Team Structure

- **2 Backend Engineers**: Engine + Node + Graph
- **2 Architecture Engineers**: Contracts + Schema + Workflow
- **2 AI/ML Engineers**: Agent + MultiAgent
- **1 QA Engineer**: Testing strategy
- **1 DevOps**: CI/CD + Release

### Parallel Work Streams

```
Week 1-2: [Contracts Team] + [Schema Team] + [Testing Team]
Week 3-4: [Engine Team] + [Node Team] + [Graph Team]
Week 5-6: [Workflow Team] + [Agent Team]
Week 7:   [Integration Team]
Week 8:   [Release Team]
```

## 🎉 Completion Checklist

### Phase 0 ✅

- [ ] Branches created
- [ ] Baseline documented
- [ ] Safety setup

### Phase 1 🔄

- [ ] Protocols defined
- [ ] Schemas modularized
- [ ] Testing ready

### Phase 2 📅

- [ ] Engine decomposed
- [ ] Nodes consolidated
- [ ] Graphs simplified

### Phase 3 📅

- [ ] Workflows created
- [ ] Agents cleaned
- [ ] Tools integrated

### Phase 4 📅

- [ ] MultiAgent patterns
- [ ] Integration tested
- [ ] Performance optimized

### Phase 5 📅

- [ ] Migration guides
- [ ] Documentation complete
- [ ] Released v3.0.0

---

**This master plan provides the complete roadmap from current monolithic architecture to clean, modular v3.0 architecture. Each phase builds on the previous, with clear subphases, deliverables, and success metrics.**
