# Claude Quick Reference Guide - COMPACT

**Focus**: Fix SimpleAgent to use proper dynamic architecture patterns

## 🎯 CORE ARCHITECTURAL ISSUES

### SimpleAgent Missing Dynamic Architecture:

1. **RecompilationMixin** - Hash-based change detection, observer pattern
2. **MetaStateSchema** - `MetaStateSchema.from_agent(agent)` for embedding
3. **Enhanced Base Agent** - Not just base Agent class
4. **Engine Name References** - `engine_name=self.engine.name` not `engine=self.engine`
5. **Dynamic Tool Routing** - `Send`/`Command`, `DynamicToolRouteMixin`
6. **RecompilableBaseGraph** - Auto-recompilation on changes
7. **GenericEngineNodeConfig** - Type-safe input/output schemas

### Key References:

- `/project_docs/dynamic_tool_routing_system/` - Complete dynamic architecture
- `/project_docs/active/architecture/generalized_recompilation_system.md` - RecompilationMixin
- `/project_docs/active/architecture/meta_state_pattern.md` - MetaStateSchema usage
- `packages/haive-core/src/haive/core/graph/node/engine_node_generic.py` - Proper node config

### Current Problems with project_docs Organization

**Issues to fix**:

- Everything jumbled together
- No clear status indicators (working/broken/outdated)
- Hard to find current/accurate information
- No timestamp system for when things were last verified

## 🔧 NEXT STEPS

1. **Get specific feedback** on what's wrong with agent building patterns
2. **Design new project_docs structure** that's clear and navigable
3. **Implement fixes systematically**
4. **Test and verify all changes**

## 📝 SESSION TRACKING

**Current Session**: 2025-01-23 - CLAUDE.md Issues Identification
**Next Session**: [To be filled]
**Key Decisions**: [To be tracked]

---

**Note**: This file serves as a quick-access reference for ongoing CLAUDE.md improvements. Update as we progress.
