#!/usr/bin/env python

import logging


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Try to import SimpleAgentState
try:
    from agents.simple.state import SimpleAgentState

    logger.info(f"Successfully imported SimpleAgentState: {SimpleAgentState}")

    # Create an instance
    state = SimpleAgentState()
    logger.info(f"Created SimpleAgentState instance: {state}")

    # Check its fields
    fields = [f for f in dir(state) if not f.startswith("_")]
    logger.info(f"Fields in SimpleAgentState: {fields}")

    # Check if it has messages
    if hasattr(state, "messages"):
        logger.info(f"Messages: {state.messages}")

    # Try adding a message
    from langchain_core.messages import HumanMessage

    msg = HumanMessage(content="Hello, my name is TestUser")

    if hasattr(state, "messages"):
        state.messages.append(msg)
        logger.info(f"Updated messages: {state.messages}")

    # Test serialization
    state_dict = state.model_dump()
    logger.info(f"State dict: {state_dict}")

except ImportError as e:
    logger.exception(f"Failed to import SimpleAgentState: {e}")

    # Let's see what SchemaComposer can create
    try:
        from haive.core.schema.schema_composer import SchemaComposer

        # Create a simple state schema with messages
        SimpleAgentState = SchemaComposer.create_message_state(
            name="SimpleAgentState", additional_fields={"user_name": (str, None)}
        )

        logger.info(f"Created SimpleAgentState via SchemaComposer: {SimpleAgentState}")

        # Create an instance
        state = SimpleAgentState()
        logger.info(f"Created SimpleAgentState instance: {state}")

        # Test with a message
        from langchain_core.messages import HumanMessage

        msg = HumanMessage(content="Hello, my name is TestUser")
        state.messages = [msg]

        logger.info(f"State with messages: {state}")

        # Test saving user name
        state.user_name = "TestUser"
        logger.info(f"State with user_name: {state}")

        # Test serialization
        state_dict = state.model_dump()
        logger.info(f"State dict: {state_dict}")

    except ImportError as e:
        logger.exception(f"Failed to import SchemaComposer: {e}")
