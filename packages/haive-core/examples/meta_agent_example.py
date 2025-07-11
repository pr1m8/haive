"""Example usage of MetaStateSchema and MetaAgentNodeConfig.

This example demonstrates how to create and use meta agents - agents that contain
other agents as part of their state. This enables sophisticated agent composition
patterns and nested execution scenarios.

The example shows:
1. Creating a simple agent to embed
2. Creating a meta state with the embedded agent
3. Using the meta agent node to execute the embedded agent
4. Building a graph that orchestrates meta agent execution
5. Advanced patterns like agent swapping and conditional execution
"""

from typing import Any, Dict, List

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from haive.core.graph.node.meta_agent_node import MetaAgentNodeConfig

# Import the meta state and meta agent node
from haive.core.schema.prebuilt.meta_state import MetaStateSchema


# Example agent classes (simplified for demonstration)
class ExampleAgent:
    """A simple example agent for demonstration."""

    def __init__(self, name: str, behavior: str = "helpful"):
        self.name = name
        self.behavior = behavior

    def run(self, input_data: dict[str, Any], **config) -> dict[str, Any]:
        """Run the agent with the given input."""
        messages = input_data.get("messages", [])

        # Simple response based on behavior
        if self.behavior == "helpful":
            response_content = f"Hello! I'm {self.name}, a helpful assistant. How can I help you today?"
        elif self.behavior == "creative":
            response_content = f"Greetings! I'm {self.name}, your creative companion. Let's explore ideas together!"
        elif self.behavior == "analytical":
            response_content = (
                f"Hello, I'm {self.name}. I'll analyze your request systematically."
            )
        else:
            response_content = f"Hi, I'm {self.name}. What would you like to discuss?"

        # Create response message
        response_message = AIMessage(content=response_content)

        # Return updated messages
        return {
            "messages": [*messages, response_message],
            "agent_response": response_content,
            "agent_name": self.name,
        }


def create_basic_meta_agent_example():
    """Create a basic example of meta agent usage."""

    # 1. Create a simple agent to embed
    helpful_agent = ExampleAgent(name="HelperBot", behavior="helpful")

    # 2. Create meta state with the embedded agent
    meta_state = MetaStateSchema(
        agent=helpful_agent,
        agent_input={"messages": [HumanMessage(content="Hello, I need some help!")]},
        meta_context={"purpose": "customer_support", "priority": "high"},
    )


    # 3. Execute the embedded agent
    meta_state.execute_agent()


    return meta_state


def create_meta_agent_graph_example():
    """Create a graph that uses meta agent nodes."""

    # Create a meta agent node configuration
    meta_node = MetaAgentNodeConfig(
        name="execute_embedded_agent",
        input_preparation="auto",
        output_handling="merge",
        error_handling="capture",
        include_messages=True,
        sync_messages=True,
    )

    # Create a preparation node
    def prepare_meta_state(state: dict[str, Any]) -> dict[str, Any]:
        """Prepare meta state for execution."""

        # Create different agents based on request type
        user_input = state.get("user_input", "")

        if "creative" in user_input.lower():
            agent = ExampleAgent(name="CreativeBot", behavior="creative")
        elif "analyze" in user_input.lower():
            agent = ExampleAgent(name="AnalyzerBot", behavior="analytical")
        else:
            agent = ExampleAgent(name="HelperBot", behavior="helpful")

        # Create meta state
        meta_state = MetaStateSchema(
            agent=agent,
            agent_input={"messages": [HumanMessage(content=user_input)]},
            meta_context={
                "purpose": "dynamic_assistance",
                "request_type": (
                    "creative" if "creative" in user_input.lower() else "general"
                ),
            },
        )

        return meta_state.model_dump()

    # Create a finalization node
    def finalize_response(state: dict[str, Any]) -> dict[str, Any]:
        """Finalize the response from meta agent execution."""

        execution_status = state.get("execution_status", "unknown")
        agent_output = state.get("agent_output", {})

        if execution_status == "completed":
            final_response = f"Task completed successfully by {agent_output.get('agent_name', 'agent')}"
        elif execution_status == "error":
            error_info = state.get("error_info", {})
            final_response = f"Task failed: {error_info.get('error', 'Unknown error')}"
        else:
            final_response = f"Task status: {execution_status}"

        return {**state, "final_response": final_response, "completed": True}

    # Build the graph
    graph = StateGraph(MetaStateSchema)

    # Add nodes
    graph.add_node("prepare", prepare_meta_state)
    graph.add_node("execute_meta_agent", meta_node)
    graph.add_node("finalize", finalize_response)

    # Add edges
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", "execute_meta_agent")
    graph.add_edge("execute_meta_agent", "finalize")
    graph.add_edge("finalize", END)

    # Compile graph
    compiled_graph = graph.compile()


    # Test with different inputs
    test_inputs = [
        "Help me with a general question",
        "I need creative ideas for my project",
        "Please analyze this data for me",
    ]

    for user_input in test_inputs:

        try:
            result = compiled_graph.invoke({"user_input": user_input})
        except Exception as e:
            pass

    return compiled_graph


def create_advanced_meta_agent_example():
    """Create an advanced example with multiple embedded agents."""

    # Create multiple agents
    agents = {
        "researcher": ExampleAgent(name="ResearchBot", behavior="analytical"),
        "writer": ExampleAgent(name="WriterBot", behavior="creative"),
        "reviewer": ExampleAgent(name="ReviewBot", behavior="helpful"),
    }

    # Create meta state with multiple potential agents
    meta_state = MetaStateSchema(
        agent=agents["researcher"],  # Start with researcher
        agent_input={
            "messages": [HumanMessage(content="Research the topic of AI agents")]
        },
        meta_context={
            "workflow": "research_write_review",
            "current_stage": "research",
            "available_agents": list(agents.keys()),
        },
    )


    # Simulate workflow stages
    workflow_stages = [
        ("research", "researcher", "Research the topic of AI agents"),
        ("write", "writer", "Write a summary based on the research"),
        ("review", "reviewer", "Review and improve the written summary"),
    ]

    for stage, agent_type, task in workflow_stages:

        # Switch to appropriate agent
        meta_state.agent = agents[agent_type]
        meta_state.agent_name = agents[agent_type].name
        meta_state.meta_context["current_stage"] = stage

        # Update input for this stage
        meta_state.agent_input = {
            "messages": [HumanMessage(content=task)],
            "previous_output": meta_state.agent_output,
        }

        # Execute agent
        try:
            meta_state.execute_agent()
        except Exception as e:
            pass")

    # Display execution summary
    summary = meta_state.get_execution_summary()

    return meta_state


def demonstrate_meta_state_features():
    """Demonstrate various MetaStateSchema features."""

    # Create agent
    agent = ExampleAgent(name="DemoBot", behavior="helpful")

    # Create meta state
    meta_state = MetaStateSchema.from_agent(
        agent=agent,
        initial_input={"messages": [HumanMessage(content="Hello")]},
        meta_context={"demo": True},
    )



    # Execute agent
    meta_state.execute_agent()


    new_agent = ExampleAgent(name="CloneBot", behavior="creative")
    cloned_state = meta_state.clone_with_agent(new_agent, reset_history=True)

    prepared_input = meta_state.prepare_agent_input(
        additional_input={"custom_field": "test"},
        include_messages=True,
        include_context=True,
    )

    return meta_state


if __name__ == "__main__":
    """Run all meta agent examples."""

    try:
        # Run basic example
        basic_meta_state = create_basic_meta_agent_example()

        # Run graph example
        meta_graph = create_meta_agent_graph_example()

        # Run advanced example
        advanced_meta_state = create_advanced_meta_agent_example()

        # Demonstrate features
        demo_meta_state = demonstrate_meta_state_features()


    except Exception as e:
        import traceback

        traceback.print_exc()
