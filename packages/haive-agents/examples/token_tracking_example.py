"""Example of using TokenTrackingAgent for cost-aware agent development.

This example demonstrates how to use the TokenTrackingAgent base class to
automatically track token usage and costs for LLM-based agents.
"""

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.state_graph.state_graph import StateGraph
from haive.core.llm import LLMConfig

from haive.agents.base import TokenTrackingAgent


class CostAwareAssistant(TokenTrackingAgent):
    """Example agent that tracks token usage and costs.

    This agent demonstrates:
    - Automatic token usage tracking
    - Cost calculation based on provider pricing
    - Token usage reporting
    """

    def setup_agent(self) -> None:
        """Configure the agent with cost tracking."""
        # Set pricing for the model (example: GPT-4 pricing)
        self.input_cost_per_1k = 0.03  # $0.03 per 1k input tokens
        self.output_cost_per_1k = 0.06  # $0.06 per 1k output tokens

        # Enable cost tracking
        self.track_costs = True

    def build_graph(self) -> BaseGraph:
        """Build a simple conversational graph."""
        graph = StateGraph(state_schema=self.state_schema)

        # Add conversation node
        def chat_node(state):
            """Simple chat interaction."""
            # Get messages from state
            messages = state.get("messages", [])

            # Call LLM (token usage will be tracked automatically)
            response = self.engine.invoke({"messages": messages})

            # The state schema will automatically track tokens
            return {"messages": response.messages}

        # Build graph
        graph.add_node("chat", chat_node)
        graph.set_entry_point("chat")
        graph.set_finish_point("chat")

        return graph


def main():
    """Run the cost-aware assistant example."""
    # Create LLM engine
    llm = LLMConfig(model="gpt-4", temperature=0.7).to_engine()

    # Create agent with token tracking
    agent = CostAwareAssistant(name="cost_aware_assistant", engine=llm)

    # Have a conversation

    # First message
    result1 = agent.invoke(
        {"messages": [{"role": "user", "content": "What is quantum computing?"}]}
    )

    # Get token usage after first interaction
    agent.get_token_usage_summary()

    # Second message
    agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "What is quantum computing?"},
                {"role": "assistant", "content": result1["messages"][-1].content},
                {"role": "user", "content": "Can you explain superposition?"},
            ]
        }
    )

    # Get cumulative token usage
    agent.get_token_usage_summary()

    # Get detailed cost analysis
    if hasattr(agent._state, "get_conversation_cost_analysis"):
        agent._state.get_conversation_cost_analysis()


if __name__ == "__main__":
    main()
