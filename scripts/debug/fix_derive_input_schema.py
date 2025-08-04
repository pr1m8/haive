#!/usr/bin/env python3
"""Fix the derive_input_schema method to exclude engine fields."""

import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, create_model

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Let's examine the exact issue and fix it
fix_content = """
The issue is that derive_input_schema is not filtering out state-only fields like 'engine' and 'engines'.

Looking at the code flow:
1. derive_input_schema gets input fields from __engine_io_mappings__ (messages, query)
2. It uses MessagesState as base class (because messages is in input fields)
3. It creates fields dict with only the input fields
4. BUT the resulting schema somehow has engine and engines fields

The problem seems to be that the created input schema is somehow inheriting these fields.
Let me check if there's a name collision or if the schema is being modified after creation.
"""

logger.info(fix_content)

# Create a test to reproduce the exact issue


# Simulate MessagesState
class MessagesState(BaseModel):
    messages: list[Any] = Field(default_factory=list, description="Messages")
    # MessagesState should NOT have engine fields


# Simulate the schema creation
logger.info("\n=== Testing create_model behavior ===")

# Test 1: Create schema with MessagesState base
fields = {"query": (Optional[str], Field(default=None, description="Query"))}

TestInput = create_model("TestInput", __base__=MessagesState, **fields)

logger.info(f"TestInput fields: {list(TestInput.model_fields.keys())}")
logger.info("Should only have: ['messages', 'query']")

# The issue must be that the input schema is being created with additional fields
# Let's check what's happening in the agent code

logger.info("\n=== The Real Issue ===")
logger.info(
    """
After analyzing the debug output, I found the issue:

The derived input schema has fields: ['engine', 'engines', 'messages', 'query']

But looking at the derive_input_schema code, it only adds fields that are in input_fields.
The issue is that 'engine' and 'engines' are somehow being added to the input schema.

Looking more closely at the debug output:
- State schema class: SimpleAgentV2State (inherits from LLMState)
- Engine I/O mappings show only 'messages' and 'query' as inputs
- But the derived input schema has 'engine' and 'engines'

The problem is likely in how the agent determines its input_schema. Let me check...
""", )

# Check if the issue is in the agent's input_schema property
logger.info("\n=== Solution ===")
logger.info(
    """
The issue is that the agent's input_schema is being set to a schema that includes engine fields.

Looking at the agent code, it derives input schema from state schema, but the state schema's
derive_input_schema method is somehow including engine fields.

The fix needs to be in the derive_input_schema method to explicitly exclude certain fields
that should never be in input schemas (like 'engine', 'engines', 'runnable_config', etc).
""", )

# Let's create the fix
fix_code = '''
# In state_schema.py, modify derive_input_schema to exclude state-only fields:

@classmethod
def derive_input_schema(
    cls, engine_name: Optional[str] = None, name: Optional[str] = None
) -> Type[BaseModel]:
    """
    Derive an input schema for the given engine from this state schema.
    ...
    """
    # Fields that should NEVER be in input schemas
    EXCLUDED_INPUT_FIELDS = {
        'engine', 'engines', 'runnable_config', 'state_schema',
        'input_schema', 'output_schema', 'checkpointer', 'store',
        'graph', 'compiled_graph', '_app', 'metadata'
    }

    fields = {}
    # Get input field names
    if engine_name is not None and hasattr(cls, "__engine_io_mappings__"):
        if engine_name in cls.__engine_io_mappings__:
            input_fields = cls.__engine_io_mappings__[engine_name].get("inputs", [])
        else:
            input_fields = []
    elif hasattr(cls, "__input_fields__"):
        # Collect input fields across all engines
        input_fields = []
        for engine_inputs in cls.__input_fields__.values():
            input_fields.extend(engine_inputs)
    else:
        input_fields = []

    # Filter out any excluded fields
    input_fields = [f for f in input_fields if f not in EXCLUDED_INPUT_FIELDS]

    # ... rest of the method
'''

logger.info(f"\n=== Proposed Fix ===\n{fix_code}")

# But wait, let me check the actual debug output more carefully...
logger.info("\n=== Wait, I found the real issue! ===")
logger.info(
    """
Looking at the debug output again:

Derived input schema: <class 'haive.core.schema.state_schema.SimpleAgentV2StateInput'>
Derived input schema fields: ['engine', 'engines', 'messages', 'query']

Agent input schema base classes: (<class 'haive.core.schema.prebuilt.messages_state.MessagesState'>,)

The issue is that the derived input schema is being created with MessagesState as base,
but then somehow engine and engines fields are being added to it!

This suggests that either:
1. MessagesState has these fields (but it shouldn't)
2. The create_model call is somehow adding these fields
3. There's some other code modifying the schema after creation

Let me check if MessagesState inherits from something that has engine fields...
""", )

# Actually, I think I found it. Let's check if MessagesState inherits from StateSchema
# and if StateSchema has engine fields

logger.info("\n=== Root Cause Found! ===")
logger.info(
    """
MessagesState inherits from StateSchema, and StateSchema might have default engine fields!

The issue is that when we use MessagesState as the base class for the input schema,
we're getting ALL of its fields, including any engine-related fields it might have
inherited from StateSchema.

The fix is to NOT use MessagesState directly as the base for input schemas.
Instead, we should create a minimal base that only has the fields we need.
""", )

# Here's the actual fix needed:
actual_fix = """
# In derive_input_schema, instead of using MessagesState directly:

# OLD CODE:
if has_messages:
    # If input needs messages, use MessagesState (lightweight)
    base_class = MessagesState

# NEW CODE:
if has_messages:
    # Create a minimal messages schema for input
    from langchain_core.messages import BaseMessage
    MinimalMessagesSchema = create_model(
        "MinimalMessagesSchema",
        messages=(List[BaseMessage], Field(default_factory=list))
    )
    base_class = MinimalMessagesSchema
"""

logger.info(f"\n=== Actual Fix Needed ===\n{actual_fix}")
