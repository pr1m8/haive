"""Internal Dynamic Supervisor - Agents Added by Supervisor Decisions.

The supervisor itself decides when to add/remove agents based on requests,
not external management calls.
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import Field, PrivateAttr

from haive.agents.base.agent import Agent
from haive.agents.multi.agent import MultiAgent

logger = logging.getLogger(__name__)


class InternalDynamicSupervisor(MultiAgent):
    """Supervisor that internally decides when to add/remove agents.

    The supervisor analyzes requests and:
    1. Checks if existing agents can handle the task
    2. If not, creates/adds appropriate agents
    3. Routes to the best available agent
    4. Can remove agents when no longer needed
    """

    # Configuration
    coordination_mode: Literal["internal_dynamic"] = Field(
        default="internal_dynamic", description="Internal dynamic coordination"
    )

    enable_internal_agent_creation: bool = Field(
        default=True, description="Allow supervisor to create agents internally"
    )

    max_agents: int = Field(
        default=10, description="Maximum number of agents to maintain"
    )

    # Private attributes
    _agent_templates: dict[str, dict[str, Any]] = PrivateAttr(default_factory=dict)
    _creation_history: list[dict[str, Any]] = PrivateAttr(default_factory=list)

    def setup_agent(self) -> None:
        """Set up with agent creation templates."""
        super().setup_agent()

        # Define templates for agents the supervisor can create
        self._setup_agent_templates()
        self._creation_history = []

    def _setup_agent_templates(self):
        """Set up templates for agents the supervisor can create."""
        self._agent_templates = {
            "research": {
                "type": "SimpleAgent",
                "capability": "research, information gathering, fact-finding",
                "system_message": "You are a research specialist. Find and analyze information thoroughly.",
                "keywords": [
                    "research",
                    "find",
                    "search",
                    "investigate",
                    "study",
                    "analyze",
                ],
            },
            "writing": {
                "type": "SimpleAgent",
                "capability": "writing, content creation, documentation",
                "system_message": "You are a professional writer. Create engaging, well-structured content.",
                "keywords": [
                    "write",
                    "create",
                    "draft",
                    "compose",
                    "document",
                    "article",
                ],
            },
            "coding": {
                "type": "ReactAgent",
                "capability": "coding, programming, software development",
                "system_message": "You are a software developer. Write clean, efficient code and debug issues.",
                "keywords": [
                    "code",
                    "program",
                    "implement",
                    "debug",
                    "develop",
                    "software",
                ],
            },
            "analysis": {
                "type": "SimpleAgent",
                "capability": "data analysis, pattern recognition, insights",
                "system_message": "You are a data analyst. Analyze data and provide actionable insights.",
                "keywords": [
                    "analyze",
                    "data",
                    "pattern",
                    "insight",
                    "trend",
                    "statistics",
                ],
            },
            "math": {
                "type": "ReactAgent",
                "capability": "mathematics, calculations, problem solving",
                "system_message": "You are a mathematician. Solve mathematical problems step by step.",
                "keywords": [
                    "calculate",
                    "math",
                    "solve",
                    "equation",
                    "compute",
                    "formula",
                ],
            },
        }

        logger.info(f"Set up {len(self._agent_templates)} agent templates")

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with internal decision making."""
        logger.info("Building internal dynamic supervisor graph")

        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor decision node
        supervisor_node = self._create_internal_supervisor_node()
        graph.add_node("supervisor", supervisor_node)

        # Add agent creator node
        creator_node = self._create_agent_creator_node()
        graph.add_node("agent_creator", creator_node)

        # Add dynamic executor node
        executor_node = self._create_dynamic_executor_node()
        graph.add_node("executor", executor_node)

        # Set entry point
        graph.set_entry_point("supervisor")

        # Routing logic
        graph.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {
                "agent_creator": "agent_creator",
                "executor": "executor",
                "END": "__end__",
            },
        )

        # Creator routes back to supervisor
        graph.add_edge("agent_creator", "supervisor")

        # Executor routes back to supervisor
        graph.add_edge("executor", "supervisor")

        logger.info("✅ Built internal dynamic supervisor graph")
        return graph

    def _create_internal_supervisor_node(self):
        """Create supervisor that makes internal decisions about agent management."""

        async def supervisor_node(state: Any) -> dict[str, Any]:
            """Make decisions about agent creation and routing."""
            logger.info("=" * 60)
            logger.info("INTERNAL DYNAMIC SUPERVISOR")
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

            # Analyze current request
            last_message = messages[-1]
            content = getattr(last_message, "content", "")

            logger.info(f"Analyzing request: '{content[:100]}...'")

            # Step 1: Check if we have a suitable agent
            suitable_agent = self._find_suitable_existing_agent(content)

            if suitable_agent:
                logger.info(f"Found suitable existing agent: {suitable_agent}")
                return {
                    "target_agent": suitable_agent,
                    "action": "execute",
                    "is_complete": False,
                }

            # Step 2: Check if we should create a new agent
            if (
                self.enable_internal_agent_creation
                and len(self.agents) < self.max_agents
            ):
                needed_agent_type = self._determine_needed_agent_type(content)

                if needed_agent_type:
                    logger.info(f"Need to create agent of type: {needed_agent_type}")
                    return {
                        "agent_type_to_create": needed_agent_type,
                        "original_request": content,
                        "action": "create_agent",
                        "is_complete": False,
                    }

            # Step 3: Use best available agent or end
            if self.agents:
                best_agent = next(iter(self.agents.keys()))  # Simple fallback
                logger.info(f"Using fallback agent: {best_agent}")
                return {
                    "target_agent": best_agent,
                    "action": "execute",
                    "is_complete": False,
                }

            logger.info("No agents available and cannot create")
            return {"is_complete": True}

        return supervisor_node

    def _create_agent_creator_node(self):
        """Create node that actually creates new agents."""

        async def agent_creator_node(state: Any) -> dict[str, Any]:
            """Create a new agent based on supervisor decision."""
            logger.info("=" * 60)
            logger.info("AGENT CREATOR NODE")
            logger.info("=" * 60)

            state_dict = self._extract_state_dict(state)

            agent_type = state_dict.get("agent_type_to_create")
            original_request = state_dict.get("original_request", "")

            if not agent_type or agent_type not in self._agent_templates:
                logger.error(f"Invalid agent type: {agent_type}")
                return {"error": f"Cannot create agent type: {agent_type}"}

            logger.info(f"Creating agent of type: {agent_type}")

            # Create the agent
            success = await self._create_agent_from_template(
                agent_type, original_request
            )

            if success:
                # Record creation
                self._creation_history.append(
                    {
                        "agent_type": agent_type,
                        "request": original_request,
                        "timestamp": "now",
                        "success": True,
                    }
                )

                # Set target for next execution
                new_agent_name = f"{agent_type}_agent"
                logger.info(f"✅ Created agent: {new_agent_name}")

                return {
                    "target_agent": new_agent_name,
                    "agent_created": True,
                    "created_agent_type": agent_type,
                }
            logger.error(f"Failed to create {agent_type} agent")
            return {"error": f"Failed to create {agent_type} agent"}

        return agent_creator_node

    def _create_dynamic_executor_node(self):
        """Create executor that runs the selected agent."""

        async def executor_node(state: Any) -> dict[str, Any]:
            """Execute the target agent."""
            logger.info("=" * 60)
            logger.info("DYNAMIC EXECUTOR")
            logger.info("=" * 60)

            state_dict = self._extract_state_dict(state)

            target_agent = state_dict.get("target_agent")
            if not target_agent:
                return {"error": "No target agent specified"}

            logger.info(f"Executing agent: {target_agent}")

            # Get agent
            agent = self.agents.get(target_agent)
            if not agent:
                logger.error(f"Agent {target_agent} not found")
                return {"error": f"Agent {target_agent} not found"}

            try:
                # Prepare input
                agent_input = self._extract_agent_input(target_agent, agent, state_dict)

                # Execute
                if hasattr(agent, "ainvoke"):
                    result = await agent.ainvoke(agent_input)
                else:
                    result = agent.invoke(agent_input)

                # Process result
                update = self._create_agent_output(
                    target_agent, agent, result, state_dict
                )
                update["last_agent"] = target_agent
                update["execution_complete"] = True

                logger.info(f"✅ Executed {target_agent} successfully")
                return update

            except Exception as e:
                logger.exception(f"Error executing {target_agent}: {e}")
                return {"error": str(e), "last_agent": target_agent}

        return executor_node

    def _find_suitable_existing_agent(self, content: str) -> str | None:
        """Find if we have an existing agent that can handle the request."""
        content_lower = content.lower()

        # Check each existing agent
        for agent_name in self.agents:
            # Simple keyword matching for now
            # In real implementation, this could use embeddings or LLM classification

            # Check against agent templates to see what this agent was designed for
            for template_type, template in self._agent_templates.items():
                if f"{template_type}_agent" == agent_name:
                    # Check if any template keywords match the content
                    if any(
                        keyword in content_lower for keyword in template["keywords"]
                    ):
                        return agent_name

        return None

    def _determine_needed_agent_type(self, content: str) -> str | None:
        """Determine what type of agent is needed for this request."""
        content_lower = content.lower()

        # Score each template
        best_score = 0
        best_type = None

        for template_type, template in self._agent_templates.items():
            score = 0

            # Count keyword matches
            for keyword in template["keywords"]:
                if keyword in content_lower:
                    score += 1

            # Direct type mention
            if template_type in content_lower:
                score += 2

            if score > best_score:
                best_score = score
                best_type = template_type

        # Only create if we have reasonable confidence
        if best_score >= 1:
            return best_type

        return None

    async def _create_agent_from_template(self, agent_type: str, request: str) -> bool:
        """Actually create an agent from a template."""
        if agent_type not in self._agent_templates:
            return False

        template = self._agent_templates[agent_type]
        agent_name = f"{agent_type}_agent"

        # Check if agent already exists
        if agent_name in self.agents:
            logger.info(f"Agent {agent_name} already exists")
            return True

        try:
            # Create engine
            from haive.core.engine.aug_llm import AugLLMConfig

            engine = AugLLMConfig(
                name=f"{agent_name}_engine",
                system_message=template["system_message"],
                temperature=0.3 if template["type"] == "SimpleAgent" else 0.4,
            )

            # Create agent based on type
            if template["type"] == "SimpleAgent":
                from haive.agents.simple.agent import SimpleAgent

                agent = SimpleAgent(name=agent_name, engine=engine)
            elif template["type"] == "ReactAgent":
                from haive.agents.react.agent import ReactAgent

                agent = ReactAgent(
                    name=agent_name,
                    engine=engine,
                    tools=[],  # Could add tools based on agent type
                )
            else:
                return False

            # Add to agents dict
            self.agents[agent_name] = agent

            # Update agent order if it exists
            if hasattr(self, "_agent_order"):
                self._agent_order.append(agent_name)

            logger.info(f"✅ Successfully created {agent_name}")
            return True

        except Exception as e:
            logger.exception(f"Failed to create agent {agent_name}: {e}")
            return False

    def _extract_state_dict(self, state: Any) -> dict[str, Any]:
        """Extract state dict preserving messages."""
        if isinstance(state, dict):
            return state

        state_dict = state.model_dump()

        # Preserve BaseMessage objects
        if hasattr(state, "messages"):
            messages = getattr(state, "messages", [])
            if hasattr(messages, "root"):
                state_dict["messages"] = messages.root
            else:
                state_dict["messages"] = list(messages)

        return state_dict

    def _route_from_supervisor(self, state: Any) -> str:
        """Route from supervisor based on action decided."""
        state_dict = self._extract_state_dict(state)

        action = state_dict.get("action", "")

        if action == "create_agent":
            return "agent_creator"
        if action == "execute":
            return "executor"
        if state_dict.get("is_complete"):
            return "END"

        return "END"

    def get_creation_history(self) -> list[dict[str, Any]]:
        """Get history of agents created by supervisor."""
        return self._creation_history.copy()

    def get_available_templates(self) -> dict[str, dict[str, Any]]:
        """Get available agent templates."""
        return self._agent_templates.copy()


# Test the internal dynamic supervisor
if __name__ == "__main__":
    import asyncio

    async def test_internal_dynamic():
        """Test the internal dynamic supervisor."""
        # Create supervisor with no initial agents
        supervisor = InternalDynamicSupervisor(
            name="internal_dynamic",
            agents=[],  # Start empty!
            enable_internal_agent_creation=True,
            max_agents=5,
        )

        # Test 1: Research request (should create research agent)
        await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Research the latest AI trends")]}
        )

        # Test 2: Coding request (should create coding agent)
        await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Write code to implement a binary search")
                ]
            }
        )

        # Test 3: Analysis request (should create analysis agent)
        await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Analyze the data patterns")]}
        )

        # Test 4: Another research request (should use existing)
        await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Find information about quantum computing")
                ]
            }
        )

    asyncio.run(test_internal_dynamic())
