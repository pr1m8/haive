from typing import List

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import Field

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.agent.config import AgentConfig
from haive.core.engine.agent.persistence.postgres_config import (
    PostgresCheckpointerConfig,
)
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.state_schema import StateSchema


# Create a proper state schema with serializable reducers
class PersistentAgentState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)

    # Set up serializable reducers correctly
    # __serializable_reducers__ = {"messages": "add_messages"}

    # Set reducer fields manually after class definition
    # We'll do this outside the class to avoid serialization issues


# Manually assign the reducer function after class definition
PersistentAgentState.__reducer_fields__ = {"messages": add_messages}


# Define your agent configuration
class MyPersistentAgentConfig(AgentConfig):
    """A persistent agent configuration for testing."""

    node_name: str = "process"

    def derive_schema(self):
        # Return our pre-defined schema instead of dynamically creating one
        return PersistentAgentState


# Create the agent implementation
@register_agent(MyPersistentAgentConfig)
class MyPersistentAgent(Agent[MyPersistentAgentConfig]):
    """A simple agent implementation for testing persistence."""

    def setup_workflow(self) -> None:
        """Set up a simple single-node workflow."""
        # Create engine if not provided
        if not hasattr(self, "engine"):
            self.engine = self.config.resolve_engine()

        # Create a simple graph with one node
        self.graph_builder.add_node(
            self.config.node_name,
            self.engine,
            command_goto="END",  # Make sure to add the END routing!
        )

        self.graph_builder.add_edge("START", self.config.node_name)

        # Set the graph
        self.graph = self.graph_builder.build(checkpointer=self.checkpointer)


# Create the PostgreSQL config
postgres_config = PostgresCheckpointerConfig(
    db_host="localhost",
    db_port=5432,
    db_name="postgres",
    db_user="postgres",
    db_pass="postgres",
    setup_needed=True,  # Will create the necessary tables
)

# Create agent config
llm_engine = AugLLMConfig(name="gpt4", model="gpt-4o")
agent_config = MyPersistentAgentConfig(
    name="persistent_agent", engine=llm_engine, persistence=postgres_config
)

# Build agent instance
agent = agent_config.build_agent()

# Define thread ID for persistence
thread_id = "conversation-123"

# Run the agent
result1 = agent.run("Hello, I'm new here!", thread_id=thread_id)
print(f"First interaction - message count: {len(result1['messages'])}")

# Run again to test persistence
result2 = agent.run("Do you remember our previous conversation?", thread_id=thread_id)
print(f"Second interaction - message count: {len(result2['messages'])}")
print(f"Result2: {result2}")
