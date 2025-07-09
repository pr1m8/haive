"""Example demonstrating the MultiAgent system.

This example shows how to create and use a multi-agent system
with different agent types and coordination strategies.
"""

import logging
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from haive.agents.multi.agent import MultiAgent
from haive.agents.simple.agent import SimpleAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchAgent(SimpleAgent):
    """Agent specialized for research tasks."""

    def setup_agent(self) -> None:
        """Set up the research agent."""
        super().setup_agent()
        # Could add research-specific tools here

    def invoke(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process input and perform research.

        This is a simplified example that just simulates research.
        """
        messages = input_data.get("messages", [])

        # Find the last human message
        human_message = None
        for msg in reversed(messages):
            if msg.type == "human":
                human_message = msg
                break

        if human_message:
            # Simulate research
            query = human_message.content
            research_results = (
                f"Research findings for '{query}':\n"
                + "1. Found relevant information source A\n"
                + "2. Found relevant information source B\n"
                + "3. Key insight: This is simulated research"
            )

            # Add to shared state
            shared_state = input_data.get("shared_state", {})
            shared_state["research_results"] = research_results

            # Add response
            response = f"I've researched '{query}' and found some relevant information."
            new_messages = messages + [AIMessage(content=response)]

            return {"messages": new_messages, "shared_state": shared_state}

        return {"messages": messages}


class WritingAgent(SimpleAgent):
    """Agent specialized for writing tasks."""

    def setup_agent(self) -> None:
        """Set up the writing agent."""
        super().setup_agent()
        # Could add writing-specific tools here

    def invoke(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process input and perform writing.

        This is a simplified example that uses research results if available.
        """
        messages = input_data.get("messages", [])
        shared_state = input_data.get("shared_state", {})

        # Find the last human message
        human_message = None
        for msg in reversed(messages):
            if msg.type == "human":
                human_message = msg
                break

        if human_message:
            # Check if we have research results
            research_results = shared_state.get(
                "research_results", "No research available"
            )

            # Generate response based on research
            response = (
                f"Based on the research:\n\n{research_results}\n\n"
                + "Here's a well-crafted response to your query:\n\n"
                + "The answer to your question is that this is a demonstration "
                + "of how multiple agents can collaborate by sharing state."
            )

            new_messages = messages + [AIMessage(content=response)]

            return {"messages": new_messages, "shared_state": shared_state}

        return {"messages": messages}


def create_research_writing_system() -> MultiAgent:
    """Create a multi-agent system with research and writing agents.

    Returns:
        MultiAgent system
    """
    # Create the agents first
    research_agent = ResearchAgent(name="Research Agent")
    writing_agent = WritingAgent(name="Writing Agent")

    # Use the class method to create the multi-agent system
    # This is the proper way to create a MultiAgent system
    system = MultiAgent.with_agents(
        agents=[research_agent, writing_agent],
        name="Research-Writing System",
        coordination_strategy="sequential",
    )

    # Debug - check if agents were added to state
    if hasattr(system, "_state_instance") and hasattr(system._state_instance, "agents"):
        logger.info(f"System has {len(system._state_instance.agents)} agents:")
        for agent_id, agent in system._state_instance.agents.items():
            logger.info(f"  Agent {agent_id}: {agent.name}")
    else:
        logger.warning("No agents in system state")

    return system


def demo_multi_agent_system():
    """Demonstrate a multi-agent system in action."""
    # Instead of the complex graph-based approach, just demonstrate
    # how research and writing agents can work together sequentially

    # Create the agents directly
    research_agent = ResearchAgent(name="Research Agent")
    writing_agent = WritingAgent(name="Writing Agent")

    # Create input with a query
    input_data = {
        "messages": [
            SystemMessage(
                content="You are a helpful assistant that researches and writes responses."
            ),
            HumanMessage(content="Tell me about multi-agent systems in AI."),
        ]
    }

    # Run the first agent (research)
    logger.info("Running Research Agent...")
    research_output = research_agent.invoke(input_data)

    # Show research output
    logger.info("Research Output:")
    if isinstance(research_output, dict) and "messages" in research_output:
        messages = research_output["messages"]
        for msg in messages:
            if hasattr(msg, "type"):
                if msg.type == "human":
                    logger.info(f"Human: {msg.content}")
                elif msg.type == "ai":
                    logger.info(f"AI: {msg.content}")
                elif msg.type == "system":
                    logger.info(f"System: {msg.content}")

    # Pass research output to writing agent
    logger.info("\nRunning Writing Agent with research results...")

    # Get shared state from research output
    shared_state = None
    if isinstance(research_output, dict) and "shared_state" in research_output:
        shared_state = research_output["shared_state"]

    # Prepare input for writing agent
    writing_input = {"messages": input_data["messages"], "shared_state": shared_state}

    # Run writing agent
    writing_output = writing_agent.invoke(writing_input)

    # Show final output
    logger.info("\nFinal Output:")
    if isinstance(writing_output, dict) and "messages" in writing_output:
        messages = writing_output["messages"]
        for msg in messages:
            if hasattr(msg, "type"):
                if msg.type == "human":
                    logger.info(f"Human: {msg.content}")
                elif msg.type == "ai":
                    logger.info(f"AI: {msg.content}")
                elif msg.type == "system":
                    logger.info(f"System: {msg.content}")

    logger.info("\nDemo completed successfully")


def create_parallel_specialist_system():
    """Create a multi-agent system with multiple specialist agents.

    This would use parallel coordination strategy.

    Returns:
        MultiAgent system
    """
    # Create specialist agents
    technical_agent = SimpleAgent(name="Technical Specialist")
    business_agent = SimpleAgent(name="Business Specialist")
    creative_agent = SimpleAgent(name="Creative Specialist")

    # Use the class method to create the multi-agent system
    system = MultiAgent.with_agents(
        agents=[technical_agent, business_agent, creative_agent],
        name="Specialist Panel",
        coordination_strategy="parallel",  # Not fully implemented yet
    )

    return system


def save_and_load_demo():
    """Demonstrate saving and loading a multi-agent system."""
    logger.info("\nSerialization demo:")

    # Create a system
    system = create_research_writing_system()

    # Add a message
    system._state_instance.add_message(HumanMessage(content="This is a test message."))

    # Instead of trying to serialize the entire state with complex objects,
    # let's just demonstrate that we can serialize the messages
    if hasattr(system._state_instance, "messages"):
        # Extract messages to a simple format
        simple_messages = []
        for msg in system._state_instance.messages:
            if hasattr(msg, "content") and hasattr(msg, "type"):
                simple_messages.append({"type": msg.type, "content": msg.content})

        # Convert to JSON
        import json

        messages_json = json.dumps(simple_messages)
        logger.info(f"Serialized messages (length: {len(messages_json)})")

        # Deserialize
        loaded_messages = json.loads(messages_json)

        # Display
        logger.info("Reconstructed messages:")
        for msg in loaded_messages:
            logger.info(f"  {msg['type']}: {msg['content']}")
    else:
        logger.info("No messages to serialize")


if __name__ == "__main__":
    # Run the demo
    demo_multi_agent_system()

    # Demonstrate serialization
    save_and_load_demo()
