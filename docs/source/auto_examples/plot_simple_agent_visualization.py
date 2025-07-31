"""SimpleAgent Workflow Visualization.
==================================

This example demonstrates how to create a SimpleAgent from haive.agents
and visualize its workflow graph using the built-in visualization method.
"""

# %%
# Import Required Libraries
# -------------------------
# First, we'll import the necessary components from haive.

import os
import time

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Disable checkpointer for this example
os.environ["HAIVE_DISABLE_CHECKPOINTER"] = "true"

# %%
# Create and Configure SimpleAgent
# --------------------------------
# Let's create a SimpleAgent with a custom configuration.

# Create configuration
config = AugLLMConfig(
    temperature=0.7, max_tokens=500, system_message="You are a helpful AI assistant."
)

# Create the agent
agent = SimpleAgent(name="visualization_demo", engine=config)


# %%
# Compile and Visualize the Agent
# -------------------------------
# Now we'll compile the agent and generate a visualization of its workflow.

# Compile the agent
agent.compile()

# Generate visualization
visualization_path = "simple_agent_workflow_demo.png"
agent.visualize_graph(visualization_path)

# %%
# Test Agent Execution
# --------------------
# Let's test the agent with a simple query.

# Measure execution time
start_time = time.time()

# Run the agent
response = agent.run("What are the benefits of using AI agents?")

# Calculate execution time
execution_time = time.time() - start_time


# %%
# Display Agent Capabilities
# --------------------------
# Show what the agent can do.


# %%
# Workflow Structure
# ------------------
# The SimpleAgent creates a basic workflow with the following structure:
#
# .. code-block:: text
#
#     START
#       ↓
#     agent_node (processes user input)
#       ↓
#     END
#
# This simple structure makes it ideal for straightforward conversational AI tasks.
