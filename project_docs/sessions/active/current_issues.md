# Current Issues - Active Development Problems

**Updated**: 2025-01-14
**Status**: Active tracking of known issues

## 🚨 Critical Issues

### 1. Schema Field Conflicts

- **Problem**: Multiple engines with same field names cause conflicts
- **Impact**: Agent state composition fails
- **Status**: Under investigation
- **Reference**: [MEM-004-CORE-G-001] Schema Composition Analysis

### 2. Import Cycle Dependencies

- **Problem**: Circular imports between agent and engine modules
- **Impact**: Import errors during development
- **Status**: Needs refactoring
- **Reference**: [MEM-002-A] Import Structure Issues

### 3. Multi-Agent State Coordination

- **Problem**: No clear pattern for multi-agent state sharing
- **Impact**: Complex agent workflows fail
- **Status**: Design phase
- **Reference**: [MEM-003-B] Multi-Agent Architecture

## ⚠️ Medium Priority Issues

### 1. Validation Node Performance

- **Problem**: Dynamic validation nodes are slow
- **Impact**: Agent response latency
- **Status**: Optimization needed

### 2. Tool Registry Conflicts

- **Problem**: Tool name conflicts across packages
- **Impact**: Tool selection errors
- **Status**: Needs naming convention

## 📝 Low Priority Issues

### 1. Documentation Gaps

- **Problem**: Some components lack comprehensive docs
- **Impact**: Developer experience
- **Status**: Ongoing improvement

### 2. Test Coverage Gaps

- **Problem**: Some edge cases not tested
- **Impact**: Potential bugs
- **Status**: Gradual improvement

## 🔄 Recently Resolved

### 1. Package Import Structure (Fixed 2025-01-08)

- **Solution**: Standardized haive.core.\* imports
- **Status**: ✅ Resolved

### 2. Documentation Build Errors (Fixed 2025-01-07)

- **Solution**: Fixed Sphinx configuration
- **Status**: ✅ Resolved

### 3. PostgreSQL Store Prepared Statement Conflicts (Fixed 2025-01-14)

- **Problem**: "prepared statement '\_pg3_X' already exists" errors with PostgreSQL store and connection pooling
- **Root Cause**: LangGraph pipeline mode creates conflicting prepared statements with pgBouncer/Supabase
- **Solution**: Three-part fix: `prepare_threshold=None`, `DEALLOCATE ALL`, and `supports_pipeline=False`
- **Status**: ✅ Resolved

### 4. Agent-as-Tool Pattern Implementation (Fixed 2025-01-14)

- **Problem**: Need all agents to have class method `as_tool()` for easy composition
- **Solution**: Added `as_tool()` and `create_retriever_tool()` class methods to base Agent class
- **Impact**: All agents can now be converted to tools for use in other agents
- **Documentation**: [Agent-as-Tool Pattern](../architecture/agent_as_tool_pattern.md)
- **Status**: ✅ Resolved

## 📊 Issue Tracking

- **Total Active**: 5 issues
- **Critical**: 3 issues
- **Medium**: 2 issues
- **Low**: 0 issues
- **Resolved This Week**: 4 issues

## 🎯 Next Steps

1. **Priority Focus**: Schema field conflicts
2. **Investigation**: Import cycle mapping
3. **Design**: Multi-agent state patterns
4. **Testing**: Add edge case coverage

---

**Note**: This file is updated regularly. Check before starting new work to avoid duplicate efforts.
