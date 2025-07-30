"""Dynamic Supervisor using DynamicChoiceModel for agent selection.

The supervisor uses DynamicChoiceModel as a tool to select from available agents,
and creates new ReactAgents when needed.
"""

import logging
from typing import Any

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import Field, PrivateAttr

from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class AgentSelectionTool(BaseTool):
    """Tool that uses DynamicChoiceModel to select best agent."""

    name: str = "select_agent"
    description: str = """Select the best agent for the current task.
    Use this tool to determine which agent should handle the request."""

    def __init__(self, choice_model: DynamicChoiceModel, **kwargs):
        super().__init__(**kwargs)
        self.choice_model = choice_model

    def _run(self, task_description: str) -> str:
        """Select agent based on task description."""
        # Get available options
        available_agents = self.choice_model.option_names

        if not available_agents or available_agents == ["END"]:
            return "CREATE_NEW_AGENT"

        # For now, simple selection logic
        # In real implementation, this could use embeddings or LLM reasoning
        task_lower = task_description.lower()

        # Check each available agent
        for agent_name in available_agents:
            if agent_name == "END":
                continue

            # Simple matching based on agent name
            if "research" in agent_name.lower() and any(
                word in task_lower
                for word in ["research", "find", "search", "investigate"]
            ):
                return agent_name

        # If no specific match, try first available agent
        if available_agents:
            return available_agents[0]

        return "CREATE_NEW_AGENT"


class AgentCreationTool(BaseTool):
    """Tool to create new ReactAgents based on task type."""

    name: str = "create_agent"
    description: str = """Create a new ReactAgent when no suitable agent exists.
    Specify the agent type and capability needed."""

    def __init__(self, supervisor, **kwargs) -> None:
        super().__init__(**kwargs)
        self.supervisor = supervisor

    def _run(self, agent_type: str, capability_description: str) -> str:
        """Create a new ReactAgent."""
        # Define agent types we can create
        agent_templates = {
            "research": {
                "name": "research_agent",
                "system_message": "You are a research specialist. Find and analyze information thoroughly. Use tools when available.",
                "tools": [],  # Could add web search, etc.
            },
            "writing": {
                "name": "writing_agent",
                "system_message": "You are a professional writer. Create engaging, well-structured content.",
                "tools": [],
            },
            "coding": {
                "name": "coding_agent",
                "system_message": "You are a software developer. Write clean, efficient code and debug issues.",
                "tools": [],  # Could add code execution tools
            },
            "analysis": {
                "name": "analysis_agent",
                "system_message": "You are a data analyst. Analyze data and provide actionable insights.",
                "tools": [],
            },
            "math": {
                "name": "math_agent",
                "system_message": "You are a mathematician. Solve problems step by step using tools when helpful.",
                "tools": [],  # Could add calculator tools
            },
        }

        if agent_type not in agent_templates:
            return f"Unknown agent type: {agent_type}"

        template = agent_templates[agent_type]
        agent_name = template["name"]

        # Check if already exists
        if agent_name in self.supervisor.agents:
            return f"Agent {agent_name} already exists"

        try:
            # Create engine
            from haive.core.engine.aug_llm import AugLLMConfig

            engine = AugLLMConfig(
                name=f"{agent_name}_engine",
                system_message=template["system_message"],
                temperature=0.4,
            )

            # Create ReactAgent
            new_agent = ReactAgent(
                name=agent_name, engine=engine, tools=template["tools"]
            )

            # Add to supervisor
            self.supervisor.agents[agent_name] = new_agent

            # Update choice model
            self.supervisor._update_choice_model()

            logger.info(f"✅ Created new ReactAgent: {agent_name}")
            return f"Created {agent_name} successfully"

        except Exception as e:
            logger.exception(f"Failed to create agent {agent_name}: {e}")
            return f"Failed to create agent: {e!s}"


class ChoiceModelSupervisor(ReactAgent):
    """Supervisor that uses DynamicChoiceModel for agent selection.

    This supervisor:
    1. Uses DynamicChoiceModel to track available agents
    2. Uses tools to select best agent for each task
    3. Creates new ReactAgents when needed
    4. Routes to selected agents for execution
    """

    # Configuration
    max_agents: int = Field(default=8, description="Maximum agents to maintain")

    # Private attributes
    _agents: dict[str, ReactAgent] = PrivateAttr(default_factory=dict)
    _choice_model: DynamicChoiceModel | None = PrivateAttr(default=None)
    _agent_selection_tool: AgentSelectionTool | None = PrivateAttr(default=None)
    _agent_creation_tool: AgentCreationTool | None = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Set up supervisor with choice model and tools."""
        # Initialize agents dict
        self._agents = {}

        # Create choice model
        self._choice_model = DynamicChoiceModel(
            option_names=["END"], option_descriptions=["End the conversation"]
        )

        # Create tools
        self._agent_selection_tool = AgentSelectionTool(self._choice_model)
        self._agent_creation_tool = AgentCreationTool(self)

        # Add tools to supervisor
        self.tools = [self._agent_selection_tool, self._agent_creation_tool]

        # Call parent setup
        super().setup_agent()

        logger.info("✅ Choice model supervisor initialized")

    @property
    def agents(self) -> dict[str, ReactAgent]:
        """Get current agents."""
        return self._agents

    def _update_choice_model(self):
        """Update choice model with current agents."""
        agent_names = [*list(self._agents.keys()), "END"]
        agent_descriptions = []

        for name in agent_names:
            if name == "END":
                agent_descriptions.append("End the conversation")
            else:
                agent = self._agents[name]
                # Try to get capability from agent
                capability = getattr(agent, "capability", f"General tasks for {name}")
                agent_descriptions.append(f"Route to {name}: {capability}")

        # Update choice model
        self._choice_model.option_names = agent_names
        self._choice_model.option_descriptions = agent_descriptions

        logger.info(f"Updated choice model with {len(agent_names)} options")

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with choice model integration."""
        logger.info("Building choice model supervisor graph")

        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor node (this ReactAgent itself)
        supervisor_node = self._create_supervisor_decision_node()
        graph.add_node("supervisor", supervisor_node)

        # Add dynamic executor node
        executor_node = self._create_agent_executor_node()
        graph.add_node("executor", executor_node)

        # Set entry point
        graph.set_entry_point("supervisor")

        # Routing
        graph.add_conditional_edges(
            "supervisof",
            self._route_from_supervisor,
            {"executor": "executor", "END": "__end__"},
        )

        # Executor loops back to supervisor
        graph.add_edge("executor", "supervisor")

        logger.info("✅ Built choice model supervisor graph")
        return graph

    def _create_supervisor_decision_node(self):
        """Create supervisor node that uses tools for decisions."""

        async def supervisor_node(state: Any) -> dict[str, Any]:
            """Supervisor makes decisions using DynamicChoiceModel."""
            logger.info("=" * 60)
            logger.info("CHOICE MODEL SUPERVISOR")
            logger.info("=" * 60)

            # Extract state
            state_dict = self._extract_state_dict(state)

            # Check completion
            if state_dict.get("is_complete"):
                return {"is_complete": True}

            # Get messages
            messages = state_dict.get("messages", [])
            if not messages:
                return {"is_complete": True}

            # Get last message for analysis
            last_message = messages[-1]

            # Skip if we just executed an agent (avoid loops)
            if isinstance(last_message, AIMessage) and state_dict.get("last_agent"):
                # Check if there's a new human message after the AI response
                human_messages = [m for m in messages if isinstance(m, HumanMessage)]
                if human_messages:
                    last_human_idx = messages.index(human_messages[-1])
                    if last_human_idx < len(messages) - 1:
                        # AI already responded, end conversation
                        return {"is_complete": True}

            # Analyze the request using this supervisor (ReactAgent)
            content = getattr(last_message, "content", "")

            # Create input for this ReactAgent to analyze
            supervisor_input = {
                "messages": [
                    HumanMessage(
                        content=f"Analyze this request and select the best agent or create one if needed: {content}"
                    )
                ]
            }

            # Use this ReactAgent's capabilities to make decision
            try:
                decision_result = await super().ainvoke(supervisor_input)

                # Extract decision from the result
                decision_messages = decision_result.get("messages", [])

                # Look for tool calls in the decision
                selected_agent = None

                for msg in decision_messages:
                    if isinstance(msg, ToolMessage):
                        if "select_agent" in getattr(msg, "name", ""):
                            selected_agent = msg.content
                        elif "create_agent" in getattr(msg, "name", ""):
                            # Agent was created, update our tracking
                            self._update_choice_model()
                    elif isinstance(msg, AIMessage):
                        # Check for tool calls
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                if tool_call["name"] == "select_agent":
                                    # Will be resolved by tool message
                                    pass
                                elif tool_call["name"] == "create_agent":
                                    pass

                # Determine target agent
                if selected_agent and selected_agent not in {"CREATE_NEW_AGENT", "END"}:
                    logger.info(f"Selected agent: {selected_agent}")
                    return {
                        "target_agent": selected_agent,
                        "original_request": content,
                        "is_complete": False,
                    }
                if selected_agent == "END":
                    return {"is_complete": True}
                if self._agents:
                    first_agent = next(iter(self._agents.keys()))
                    logger.info(f"Using default agent: {first_agent}")
                    return {
                        "target_agent": first_agent,
                        "original_request": content,
                        "is_complete": False,
                    }
                logger.info("No agents available")
                return {"is_complete": True}

            except Exception as e:
                logger.exception(f"Error in supervisor decision: {e}")
                return {"is_complete": True}

        return supervisor_node

    def _create_agent_executor_node(self):
        """Create node that executes the selected agent."""

        async def executor_node(state: Any) -> dict[str, Any]:
            """Execute the selected ReactAgent."""
            logger.info("=" * 60)
            logger.info("AGENT EXECUTOR")
            logger.info("=" * 60)

            state_dict = self._extract_state_dict(state)

            target_agent = state_dict.get("target_agent")
            state_dict.get("original_request", "")

            if not target_agent:
                return {"error": "No target agent specified"}

            logger.info(f"Executing ReactAgent: {target_agent}")

            # Get the ReactAgent
            agent = self._agents.get(target_agent)
            if not agent:
                logger.error(f"Agent {target_agent} not found")
                return {"error": f"Agent {target_agent} not found"}

            try:
                # Prepare input for the ReactAgent
                messages = state_dict.get("messages", [])

                # Create input focused on the original request
                agent_input = {"messages": messages}

                # Execute the ReactAgent
                result = await agent.ainvoke(agent_input)

                # Extract the response
                result_messages = result.get("messages", [])

                # Update state with the result
                update = {
                    "messages": result_messages,
                    "last_agent": target_agent,
                    "execution_complete": True,
                }

                logger.info(f"✅ ReactAgent {target_agent} executed successfully")
                return update

            except Exception as e:
                logger.exception(f"Error executing {target_agent}: {e}")
                return {"error": str(e), "last_agent": target_agent}

        return executor_node

    def _extract_state_dict(self, state: Any) -> dict[str, Any]:
        """Extract state dict preserving messages."""
        if isinstance(state, dict):
            return state

        state_dict = state.model_dump() if hasattr(state, "model_dump") else {}

        # Preserve BaseMessage objects
        if hasattr(state, "messages"):
            messages = getattr(state, "messages", [])
            if hasattr(messages, "root"):
                state_dict["messages"] = messages.root
            else:
                state_dict["messages"] = list(messages)

        return state_dict

    def _route_from_supervisor(self, state: Any) -> str:
        """Route from supervisor based on decision."""
        state_dict = self._extract_state_dict(state)

        if state_dict.get("is_complete"):
            return "END"

        if state_dict.get("target_agent"):
            return "executor"

        return "END"

    def get_available_agents(self) -> list[str]:
        """Get list of available agents."""
        return list(self._agents.keys())

    def get_choice_model_status(self) -> dict[str, Any]:
        """Get status of choice model."""
        return {
            "available_options": (
                self._choice_model.option_names if self._choice_model else []
            ),
            "total_agents": len(self._agents),
            "max_agents": self.max_agents,
        }


# Test the choice model supervisor
if __name__ == "__main__":
    import asyncio

    async def test_choice_model_supervisor():
        """Test the choice model supervisor."""
        # Create supervisor (starts empty)
        supervisor = ChoiceModelSupervisor(name="choice_supervisof", max_agents=5)

        # Test 1: Research request
        await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content="Research the latest developments in machine learning"
                    )
                ]
            }
        )

        # Test 2: Coding request
        await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Write Python code to implement quicksort")
                ]
            }
        )

        # Test 3: Use existing agent
        await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Find information about quantum computing")
                ]
            }
        )

    asyncio.run(test_choice_model_supervisor())
