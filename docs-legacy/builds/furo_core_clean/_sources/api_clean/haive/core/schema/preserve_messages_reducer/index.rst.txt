
haive.core.schema.preserve_messages_reducer
===========================================

.. py:module:: haive.core.schema.preserve_messages_reducer

.. autoapi-nested-parse::

   Custom message reducer for preserving BaseMessage fields.

   This module provides a custom reducer function that preserves BaseMessage objects
   intact during state updates in multi-agent systems. Unlike LangGraph's default
   add_messages reducer, this implementation avoids converting messages to dicts
   and back, which can cause loss of important fields like tool_call_id.

   The preserve_messages_reducer is critical for multi-agent tool coordination,
   ensuring that ToolMessage objects maintain their tool_call_id field when
   passed between agents. This prevents KeyError exceptions and enables proper
   tool result routing.

   .. admonition:: Example

      >>> from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer
      >>> from langchain_core.messages import ToolMessage
      >>>
      >>> # Create a ToolMessage with tool_call_id
      >>> tool_msg = ToolMessage(content="Result: 42", tool_call_id="call_123")
      >>>
      >>> # Using preserve_messages_reducer maintains the field
      >>> messages = preserve_messages_reducer([], [tool_msg])
      >>> assert messages[0].tool_call_id == "call_123"  # Preserved!

   .. note::

      This reducer is automatically used by AgentSchemaComposer for message fields
      to ensure proper multi-agent message handling.






Functions
---------

   preserve_messages_reducer
.. autofunction:: preserve_messages_reducer



Package Contents
----------------

