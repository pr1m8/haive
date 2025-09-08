# Haive Architecture Analysis Plan

## Phase 1: Core Schema System Analysis

### 1.1 Base Schema Infrastructure

- [ ] Examine `haive-core/src/haive/core/schema/`
  - [ ] `state_schema.py` - Base state schema class
  - [ ] `schema_composition.py` - How schemas are composed
  - [ ] `field_mapping.py` - Field mapping and resolution
  - [ ] Document inheritance hierarchy
  - [ ] Note field conflict resolution patterns

### 1.2 Prebuilt Schemas

- [ ] Analyze `haive-core/src/haive/core/schema/prebuilt/`
  - [ ] `messages_state.py` - Message handling schema
  - [ ] `meta_state.py` - Meta state pattern
  - [ ] `agent_state.py` - Agent-specific state
  - [ ] Document schema relationships
  - [ ] Note composition patterns

### 1.3 Schema Composition System

- [ ] How schemas merge fields
- [ ] Conflict resolution mechanisms
- [ ] Dynamic schema creation
- [ ] Schema validation process
- [ ] Type safety guarantees

**Key Questions:**

- How are field conflicts handled?
- What happens with nested schemas?
- How does dynamic composition work?
- Where is type information preserved?

---

## Phase 2: Engine System Analysis

### 2.1 Base Engine Architecture

- [ ] Examine `haive-core/src/haive/core/engine/`
  - [ ] `base_engine.py` - Base engine interface
  - [ ] `aug_llm/` - Augmented LLM engine
  - [ ] `tool_engine.py` - Tool management
  - [ ] `validation_engine.py` - Validation logic

### 2.2 AugLLMConfig Deep Dive

- [ ] Configuration structure
- [ ] Tool registration mechanism
- [ ] Routing system integration
- [ ] Structured output handling
- [ ] Dynamic recompilation triggers

### 2.3 Engine-Schema Integration

- [ ] How engines use schemas
- [ ] State passing mechanisms
- [ ] Schema requirements for engines
- [ ] Engine composition patterns

**Key Questions:**

- How do engines declare schema requirements?
- What triggers engine recompilation?
- How are tools integrated with schemas?
- Where does routing information live?

---

## Phase 3: Graph Node System

### 3.1 Node Infrastructure

- [ ] Examine `haive-core/src/haive/core/graph/node/`
  - [ ] `base_node.py` - Base node class
  - [ ] `agent_node.py` - Agent execution nodes
  - [ ] `tool_node.py` - Tool execution nodes
  - [ ] `validation_node.py` - Validation nodes
  - [ ] `router_node.py` - Routing logic

### 3.2 Node Routing System

- [ ] Message passing between nodes
- [ ] Route determination logic
- [ ] Conditional routing patterns
- [ ] Dynamic route modification
- [ ] Error handling in routing

### 3.3 Node-Schema Integration

- [ ] How nodes access state
- [ ] Schema requirements per node type
- [ ] State transformation in nodes
- [ ] Output schema validation

**Key Questions:**

- How do nodes declare input/output schemas?
- What determines routing decisions?
- How are node chains constructed?
- Where does state transformation happen?

---

## Phase 4: Graph Construction & Compilation

### 4.1 StateGraph Architecture

- [ ] Graph building process
- [ ] Node registration
- [ ] Edge creation
- [ ] Compilation process
- [ ] Runtime graph modification

### 4.2 Graph-Schema-Engine Integration

- [ ] How components connect
- [ ] Compilation dependencies
- [ ] Recompilation triggers
- [ ] State flow through graph

**Key Questions:**

- What triggers graph recompilation?
- How are schemas validated during compilation?
- Where are routing tables stored?
- How do dynamic modifications work?

---

## Phase 5: Technical Debt & Issues

### 5.1 Identified Problems

- [ ] Schema composition conflicts
- [ ] Circular dependencies
- [ ] Type safety gaps
- [ ] Performance bottlenecks
- [ ] Code duplication

### 5.2 Architectural Anti-patterns

- [ ] God objects
- [ ] Tight coupling
- [ ] Hidden dependencies
- [ ] Inconsistent patterns

### 5.3 Improvement Opportunities

- [ ] Refactoring targets
- [ ] Pattern standardization
- [ ] Performance optimizations
- [ ] Type safety improvements

---

## Phase 6: Documentation & Centralization

### 6.1 Create Central Architecture Doc

- [ ] Link all findings
- [ ] Create dependency maps
- [ ] Document flow diagrams
- [ ] Establish patterns guide

### 6.2 Issue Tracking

- [ ] Create issues list
- [ ] Prioritize by impact
- [ ] Define solution approaches
- [ ] Track dependencies

---

## Analysis Approach

1. **Start with schemas** - Understanding data flow
2. **Move to engines** - Understanding processing
3. **Examine nodes** - Understanding execution
4. **Study routing** - Understanding control flow
5. **Review graph compilation** - Understanding assembly
6. **Document issues** - Creating action items

## Output Documents

1. `architecture_analysis.md` - Main findings
2. `schema_system.md` - Schema deep dive
3. `engine_system.md` - Engine analysis
4. `node_routing.md` - Node & routing details
5. `technical_debt.md` - Issues and solutions
6. `ARCHITECTURE_HUB.md` - Central linking document

## Notes Section

(Your comments on graph node routing, schema system, and node infrastructure will be added here as we analyze)
