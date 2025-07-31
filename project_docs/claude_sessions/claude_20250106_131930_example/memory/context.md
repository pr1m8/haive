# Current Context

## Working On

- Setting up example session structure
- File: /home/will/Projects/haive/backend/haive/CLAUDE.md
- Line: Complete rewrite

## Key Insights

- Schema composition happens in `_setup_schemas()` method
- Tool routing uses `tool_route` field in engine configuration
- Engine registration required for node discovery in graphs
- Agents auto-generate schemas from their engines

## Important Patterns

1. **Agent Initialization Flow**:

   ```
   __init__ → setup_agent() → _sync_fields_from_engine() → _setup_schemas() → _build_initial_graph()
   ```

2. **Schema Generation**:
   - SchemaComposer reads engine output fields
   - Creates dynamic Pydantic models
   - Handles field conflicts with prefixing

3. **Tool Routing**:
   - Tools assigned to engines via configuration
   - Router node directs to appropriate engine
   - Validation happens before execution

## Next Steps

1. Create agent-specific memory structure
2. Document common patterns
3. Build reusable code snippets library
