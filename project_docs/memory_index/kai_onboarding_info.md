# Kai ⚡ - Development Specialist Onboarding

**Welcome Kai!** You're the development specialist working with Doc 📚 (documentation specialist).

## 🎯 YOUR ROLE

- **Development Specialist** - Code quality, testing, integration
- **Primary Focus Options**:
  - Reflection pattern integration with LangGraph
  - Performance testing with real LLM workflows
  - Code quality improvements across packages
  - New agent pattern development

## 📁 KEY FILES TO WATCH

### **PRIMARY COORDINATION** (Check every 10 mins)

```
/project_docs/memory_index/coordination_board.md
```

**This is our main communication hub!** Update your status here and check for messages.

### **CONTEXT DOCUMENTS** (Read once)

```
/CLAUDE.md - Main project memory
/project_docs/memory_index/claude_working_memory.md - Doc's session context
/project_docs/memory_index/documentation_audit_status.md - Documentation work details
```

### **YOUR WORK AREAS**

```
/packages/haive-agents/src/haive/agents/reflection/ - Reflection agents (complete, ready for integration)
/packages/haive-agents/tests/reflection/ - Test suite
/packages/haive-core/src/haive/core/ - Core system for integration work
```

## 🚀 DEVELOPMENT FOCUS OPTIONS

### Option 1: **Reflection Pattern Integration** ⭐ (Recommended)

- **Status**: Complete implementation, needs LangGraph integration
- **Task**: Connect reflection agents with real workflows
- **Testing**: Multi-agent message transformation validation
- **Files**: `/packages/haive-agents/src/haive/agents/reflection/`

### Option 2: **Performance & Quality**

- **Task**: Performance testing across agent systems
- **Focus**: Real LLM execution, memory optimization
- **Testing**: Load testing, concurrent agent execution

### Option 3: **New Agent Patterns**

- **Task**: Develop new agent architectures
- **Focus**: Based on gaps you identify in current system
- **Innovation**: Your choice of cutting-edge patterns

## 💬 COMMUNICATION PROTOCOL

### **Status Updates** (Required)

Update your row in the coordination board dashboard:

```
| Kai ⚡ | WORKING | Reflection Integration | 25% | 2 hours | [timestamp] |
```

### **Messages** (As needed)

Add to the messages section:

```
- **[time] Kai → Doc**: Your message here
- **[time] Kai → Will**: Status or questions
```

### **Task Claims** (Important)

Claim tasks to avoid conflicts:

```
- **[time] Kai**: Taking: Reflection pattern LangGraph integration
```

## 🛠️ DEVELOPMENT ENVIRONMENT

### **Required Commands**

```bash
# Test imports work
poetry run python -c "from haive.core import *; print('Core OK')"
poetry run python -c "from haive.agents.reflection import *; print('Reflection OK')"

# Run reflection tests
poetry run pytest packages/haive-agents/tests/reflection/ -v

# Run all tests
poetry run pytest

# Code quality
poetry run ruff check
poetry run mypy packages/
```

### **Current State**

- **Reflection agents**: ✅ Complete, 4 agent types implemented
- **Testing**: ✅ Comprehensive test suite (no mocks)
- **Integration**: ❌ Needs LangGraph workflow connection
- **Documentation**: ✅ Patterns documented

## 📊 CURRENT PROJECT STATUS

### **Doc 📚 is handling:**

- ✅ Parse error fixes (26/63 fixed, 37 remaining)
- ⏳ Documentation audit (20K+ issues)
- ⏳ Sphinx build improvements

### **Available for you:**

- 🎯 Reflection pattern integration (recommended)
- 🎯 Performance testing and optimization
- 🎯 Code quality improvements
- 🎯 New agent development

## 🚨 URGENT: CHOOSE YOUR FOCUS

**Please update the coordination board with:**

1. **Your chosen focus area**
2. **Your estimated timeline**
3. **Any questions or blockers**

## 🤝 MEETING REQUEST

Will asked: "Who wants to do what and when should we meet?"

**Please respond in coordination board with:**

- Your preferred development focus
- Meeting availability
- Any coordination needs

---

**Ready to start! Check the coordination board and claim your tasks! 🚀**
