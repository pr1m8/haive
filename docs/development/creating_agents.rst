Creating Custom Agents
====================

This guide explains how to create custom agents using the Haive framework.

Agent Interface
-------------

All agents should implement a common interface:

.. code-block:: python

    from haive.agents.base import BaseAgent
    
    class CustomAgent(BaseAgent):
        def __init__(self, config=None):
            super().__init__(config)
            # Additional initialization
        
        def run(self, input_data):
            """Main method to execute the agent's logic"""
            # Implement your agent's logic here
            return result

State Management
--------------

Agents typically need to manage state:

.. code-block:: python

    from haive.agents.base import BaseAgent
    from haive.core.state import State
    
    class CustomState(State):
        def __init__(self):
            self.history = []
            self.current_step = 0
            
        def update(self, new_info):
            self.history.append(new_info)
            self.current_step += 1
    
    class StatefulAgent(BaseAgent):
        def __init__(self, config=None):
            super().__init__(config)
            self.state = CustomState()
        
        def run(self, input_data):
            # Process using state
            self.state.update({"input": input_data})
            # More processing...
            return result

Testing Your Agent
----------------

Create comprehensive tests for your agent:

.. code-block:: python

    import pytest
    from haive.agents.custom import CustomAgent
    
    def test_custom_agent_basic():
        agent = CustomAgent()
        result = agent.run("test input")
        assert result is not None
        
    def test_custom_agent_complex_input():
        agent = CustomAgent()
        result = agent.run({"key": "value", "nested": {"data": 123}})
        assert "processed" in result
