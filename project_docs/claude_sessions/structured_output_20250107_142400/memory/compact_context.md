# Compact Context - Agent Building in Haive

## What I Know

### Agent Basics

- **Inherit from `Agent[TState]`** with typed state
- **Two key methods**: `setup_agent()` and `build_graph()`
- **State-driven**: Everything flows through StateSchema
- **Graph-based**: Nodes connected by edges define workflow

### SimpleAgent Deep Dive

- **Magic**: Modifies engine's output schema at runtime
- **Smart routing**: Auto-detects tool/parser/validation needs
- **Key innovation**: `_modify_engine_schema()` method
- **Pattern**: Agent → Validation → Tool/Parser → End

### Multi-Agent Power

- **Composition pattern**: Wrap agents without modification
- **Coordination modes**: sequential, parallel, conditional
- **State flows**: Automatic between agents
- **Our use**: StructuredOutputAgent wraps any agent

### Schema System

- **SchemaComposer**: Builds schemas dynamically
- **Field syncing**: Engine fields ↔ Agent fields
- **Output schemas**: Can be modified at runtime
- **Compatibility**: Analyzable between agents

### Tool Ecosystem

- **Tool routes**: Map tools to execution paths
- **Three types**: langchain_tool, pydantic_model, function
- **Registration**: Tools must be in engine
- **Execution**: ToolNode vs ParserNode vs direct

### Output Handling

- **Engine-level**: structured_output_model
- **Mixin-level**: OutputMixin.transform_output()
- **Wrapper-level**: StructuredOutputAgent
- **Adapter pattern**: Field mapping, extraction, validation

## What We Built

1. **OutputAdapter**: Transformation pipeline with field mapping
2. **OutputMixin**: Adds output capabilities to any class
3. **StructuredOutputAgent**: Multi-agent wrapper for structured output
4. **Tests**: 11 passing tests covering all functionality

## Key Patterns Discovered

- **Wrapper > Modification**: Cleaner to wrap than modify
- **Composition works**: Multi-agent is powerful for extensions
- **Type annotations matter**: Pydantic v2 is strict
- **Defaults help**: Better UX with sensible fallbacks

## Ready for Next Task

The supervisor.py file suggests we're moving to:

- Multi-agent orchestration
- Dynamic agent selection
- Supervisor patterns
- Agent handoffs

I have a solid foundation in Haive's agent architecture and am ready to tackle more complex multi-agent scenarios!
