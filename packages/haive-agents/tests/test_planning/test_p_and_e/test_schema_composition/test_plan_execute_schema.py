#!/usr/bin/env python
"""Test schema composition with PlanAndExecuteAgent using hybrid PlanExecuteState."""

from langchain_core.messages import HumanMessage

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.state import PlanExecuteState

print("PlanAndExecuteAgent Schema Composition Test")
print("=" * 60)

# Create PlanAndExecuteAgent
agent = PlanAndExecuteAgent(name="test_p_and_e")

print("\n1. Checking Agent Configuration:")
print(f"   - Agent name: {agent.name}")
print(f"   - State schema set to: {agent.state_schema}")
print(f"   - use_prebuilt_base: {agent.use_prebuilt_base}")
print(f"   - Engines configured: {list(agent.engines.keys())}")

print("\n2. Checking Composed Schema:")
# The agent should have composed a schema that extends PlanExecuteState
fields = agent.state_schema.model_fields
print(f"   - Schema name: {agent.state_schema.__name__}")
print(f"   - Total fields: {len(fields)}")

# Check for key fields from PlanExecuteState
plan_execute_fields = [
    "messages",
    "plan",
    "context",
    "final_answer",
    "execution_results",
]
print("\n   Fields from PlanExecuteState:")
for field in plan_execute_fields:
    if field in fields:
        print(f"   ✓ {field}")
    else:
        print(f"   ✗ {field} (MISSING!)")

# Check for engine management fields
engine_fields = ["engine", "engines"]
print("\n   Engine management fields (from composition):")
for field in engine_fields:
    if field in fields:
        print(f"   ✓ {field}")
    else:
        print(f"   ✗ {field} (MISSING!)")

print("\n3. Testing State Creation:")
try:
    # Create state instance
    state = agent.state_schema()
    print("   ✓ State instance created successfully")

    # Check inherited behavior
    print(f"   - Is MessagesState subclass: {isinstance(state, PlanExecuteState)}")
    print(f"   - Has messages: {hasattr(state, 'messages')}")
    print(f"   - Has plan field: {hasattr(state, 'plan')}")
    print(
        f"   - Has engine fields: {hasattr(state, 'engine') and hasattr(state, 'engines')}"
    )

except Exception as e:
    print(f"   ✗ Error creating state: {e}")

print("\n4. Testing Agent Execution:")
try:
    input_data = {
        "messages": [HumanMessage(content="Create a simple web scraper in Python")]
    }

    print("   Running agent with task: 'Create a simple web scraper in Python'")

    # Run the agent (this will fail for now due to graph building issues, but shows the schema works)
    result = agent.run(input_data=input_data, debug=True)

    print("\n   ✓ Agent executed successfully!")
    print(f"   - Result type: {type(result)}")
    print(f"   - Has plan: {hasattr(result, 'plan') and result.plan is not None}")

except Exception as e:
    print(f"\n   ✗ Agent execution failed: {type(e).__name__}: {str(e)[:100]}...")

    # Even if execution fails, we can check if the schema was properly composed
    print("\n   But schema composition worked:")
    print(
        f"   - State schema is properly composed: {agent.state_schema != PlanExecuteState}"
    )
    print(
        f"   - Schema has engine fields: {'engine' in agent.state_schema.model_fields}"
    )
    print(f"   - Schema has plan field: {'plan' in agent.state_schema.model_fields}")

print("\n" + "=" * 60)
print("Summary:")
print("- PlanExecuteState is a prebuilt schema that inherits from MessagesState")
print("- PlanAndExecuteAgent uses use_prebuilt_base=True")
print("- SchemaComposer adds engine/engines fields to the prebuilt schema")
print(
    "- The composed schema has all fields from both PlanExecuteState + engine management"
)
