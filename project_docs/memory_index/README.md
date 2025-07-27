# Memory Index System

This is the central index for all memories, discoveries, and knowledge across the Haive project. Use `@memory_index/` to reference specific memories.

## 🗂️ Index Structure

```
memory_index/
├── README.md                  # This file - main index
├── by_date/                   # Chronological memories
├── by_agent/                  # Agent-specific discoveries
├── by_task/                   # Task-specific knowledge
├── by_package/                # Package-specific memories
├── by_pattern/                # Design patterns discovered
├── by_error/                  # Error solutions
└── quick_reference.md         # Most-used memories
```

## 🔍 Quick Access

### Recent Important Memories

- @memory_index/by_task/documentation/autoapi_namespace_fix.md - **COMPLETE AutoAPI fix - 1,877 RST files**
- @memory_index/by_date/2025-07-27/README.md - **July 27: Documentation system overhaul**
- @memory_index/by_error/containers_tilebag_keyerror.md - Fixed critical AutoAPI KeyError
- @memory_index/by_task/documentation_97_percent_fix.md - Reduced doc errors by 97%
- @memory_index/by_pattern/meta_state_schema.md - MetaStateSchema async pattern
- @memory_index/by_agent/multi_agent_sequential.md - ReactAgent → SimpleAgent pattern

### Most Referenced

- @memory_index/by_pattern/no_mocks_testing.md - Real component testing philosophy
- @memory_index/by_error/pydantic_init_override.md - Never override **init** in Pydantic
- @memory_index/by_task/poetry_run_everything.md - Always use poetry run
- @memory_index/by_package/autoapi_conflicts.md - AutoAPI/autosummary conflicts

## 📅 Navigation by Date

- [2025-07-27](by_date/2025-07-27/README.md) - **AutoAPI system complete overhaul - 1,877 RST files**
- [2025-01-16](by_date/2025-01-16/README.md) - Documentation fixes, error reduction
- [2025-01-15](by_date/2025-01-15/README.md) - MetaStateSchema async, Agent-as-Tool
- [2025-01-14](by_date/2025-01-14/README.md) - PostgreSQL Store fixes

## 🤖 Navigation by Agent

- [SimpleAgent](by_agent/simple_agent/README.md) - Basic agent patterns
- [ReactAgent](by_agent/react_agent/README.md) - Tool usage patterns
- [MultiAgent](by_agent/multi_agent/README.md) - Coordination patterns
- [RAGAgent](by_agent/rag_agent/README.md) - Retrieval patterns

## 📦 Navigation by Package

- [haive-core](by_package/haive-core/README.md) - Core infrastructure memories
- [haive-agents](by_package/haive-agents/README.md) - Agent implementation patterns
- [haive-tools](by_package/haive-tools/README.md) - Tool integration knowledge
- [haive-games](by_package/haive-games/README.md) - Game implementation patterns

## 🎯 Navigation by Task

- [Documentation](by_task/documentation/README.md) - Doc building, Sphinx, galleries
- [Testing](by_task/testing/README.md) - No mocks, real components
- [Debugging](by_task/debugging/README.md) - Common issues and solutions
- [Architecture](by_task/architecture/README.md) - Design decisions

## 🚨 Navigation by Error

- [Build Errors](by_error/build_errors/README.md) - Compilation and build issues
- [Import Errors](by_error/import_errors/README.md) - Module and import problems
- [Runtime Errors](by_error/runtime_errors/README.md) - Execution issues
- [Test Errors](by_error/test_errors/README.md) - Testing problems

## 📋 Usage Examples

```markdown
# Reference a specific memory

See @memory_index/by_error/containers_tilebag_keyerror.md for the solution

# Reference a pattern

Following @memory_index/by_pattern/no_mocks_testing.md philosophy

# Reference by date

As discovered on @memory_index/by_date/2025-01-16/doc_fixes.md

# Reference by agent

Using pattern from @memory_index/by_agent/react_agent/tool_usage.md
```

## 🔗 Integration with CLAUDE.md

CLAUDE.md should reference this index for specific memories:

```markdown
## 📚 Memory System

- Main index: @memory_index/README.md
- Quick ref: @memory_index/quick_reference.md
- Recent: @memory_index/by_date/
```
