"""Reflection Agent Implementation."""

import logging
from datetime import datetime
from typing import Any

from agents.reflection.config import ReflectionAgentConfig
from agents.reflection.state import ReflectionAgentState
from agents.simple.agent import SimpleAgent
from haive.core.engine.agent.agent import register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(ReflectionAgentConfig)
class ReflectionAgent(SimpleAgent):
    """An agent with self-reflection capabilities that can improve its responses.

    This agent extends SimpleAgent by adding reflection and improvement steps
    to iteratively refine responses based on self-critique.
    """

    def __init__(self, config: ReflectionAgentConfig):
        """Initialize the reflection agent with the provided configuration."""
        super().__init__(config)
        self.config = config

        # Initialize reflection engine
        if self.config.reflection.reflection_llm:
            self.reflection_engine = (
                self.config.reflection.reflection_llm.create_runnable()
            )
        else:
            # Use the same engine as the main agent
            self.reflection_engine = self.engine

    def setup_workflow(self) -> None:
        """Set up a workflow graph with reflection capabilities."""
        logger.debug(f"Setting up workflow for ReflectionAgent {self.config.name}")

        # Create DynamicGraph with proper component registration
        components = [self.config.engine]
        if (
            self.config.reflection.reflection_llm
            and self.config.reflection.reflection_llm != self.config.engine
        ):
            components.append(self.config.reflection.reflection_llm)

        gb = DynamicGraph(components=components, state_schema=self.config.state_schema)

        # Add the initial response node
        gb.add_node(
            name=self.config.initial_node_name,
            config=self._create_initial_response_function(),
            command_goto=self.config.reflection_node_name,
        )

        # Add reflection node
        gb.add_node(
            name=self.config.reflection_node_name,
            config=self._create_reflection_function(),
            command_goto=None,  # Will use conditional edge
        )

        # Add improvement node
        gb.add_node(
            name=self.config.improvement_node_name,
            config=self._create_improvement_function(),
            command_goto=self.config.evaluation_node_name,
        )

        # Add evaluation node
        gb.add_node(
            name=self.config.evaluation_node_name,
            config=self._create_evaluation_function(),
            command_goto=None,  # Will use conditional edge to either loop or end
        )

        # Add search node if enabled
        if self.config.reflection.use_search:
            gb.add_node(
                name=self.config.search_node_name,
                config=self._create_search_function(),
                command_goto=self.config.improvement_node_name,
            )

        # Add START edge
        gb.add_edge(START, self.config.initial_node_name)

        # Add conditional edge from reflection to either search, improve, or end
        if self.config.reflection.use_search:
            # Route to search if search is enabled
            gb.add_conditional_edges(
                from_node=self.config.reflection_node_name,
                condition_or_branch=self._should_continue_reflection,
                routes={"continue": self.config.search_node_name, "end": END},
            )
        else:
            # Route directly to improvement if search is disabled
            gb.add_conditional_edges(
                from_node=self.config.reflection_node_name,
                condition_or_branch=self._should_continue_reflection,
                routes={"continue": self.config.improvement_node_name, "end": END},
            )

        # Add conditional edge from evaluate to either reflect again or end
        gb.add_conditional_edges(
            from_node=self.config.evaluation_node_name,
            condition_or_branch=self._should_continue_improvement,
            routes={"continue": self.config.reflection_node_name, "end": END},
        )

        # Get the built graph (not compiled yet)
        self.graph = gb.build()
        logger.info(f"Set up reflection workflow for {self.config.name}")

    def _create_initial_response_function(self):
        """Create a function for the initial response node."""

        # This is similar to the simple agent's node
        def initial_response_function(state: ReflectionAgentState) -> dict[str, Any]:
            try:
                # Use the engine to generate an initial response
                result = self.engine.invoke({"messages": state.messages})

                if hasattr(result, "content"):
                    response_content = result.content
                else:
                    response_content = str(result)

                # Extract the original request (last human message)
                original_request = state.last_human_message

                # Store the initial response and request
                response_message = AIMessage(content=response_content)

                return {
                    "messages": state.messages + [response_message],
                    "original_request": original_request,
                    "response": response_content,
                    "reflection_round": 0,
                }
            except Exception as e:
                logger.error(f"Error in initial response: {e}")
                return state

        return initial_response_function

    def _create_reflection_function(self):
        """Create a function for the reflection node."""
        # Create structured output parser for reflection
        reflection_parser = PydanticToolsParser(
            tools=[self.config.reflection_output_model]
        )

        # Create prompt template for reflection
        reflection_prompt = ChatPromptTemplate.from_template(
            self.config.reflection.reflection_prompt_template
        )

        # Create chain with structured output
        reflection_chain = (
            reflection_prompt
            | self.reflection_engine.bind_tools(
                tools=[self.config.reflection_output_model]
            )
            | reflection_parser
        )

        def reflection_function(state: ReflectionAgentState) -> dict[str, Any]:
            try:
                # Extract needed fields
                original_request = state.original_request
                response = state.response

                if not original_request or not response:
                    logger.warning("Missing required fields for reflection")
                    return Command(update=state, goto="end")

                # Construct reflection input
                reflection_input = {
                    "original_request": original_request,
                    "response": response,
                }

                # Generate reflection
                reflection_result = reflection_chain.invoke(reflection_input)

                if not reflection_result:
                    logger.warning("No reflection result generated")
                    return Command(update=state, goto="end")

                # Extract the first reflection result
                reflection = reflection_result[0]

                # Update state with reflection info
                reflection_round = state.reflection_round + 1

                # Add to reflection history
                reflection_history = state.reflection_history.copy()
                reflection_history.append(
                    {
                        "round": reflection_round,
                        "response": response,
                        "reflection": reflection.model_dump(),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                # Update state
                state_update = {
                    **state.model_dump(),
                    "feedback": f"Reflection: {reflection.reflection}\nMissing: {reflection.missing}\nSuperfluous: {reflection.superfluous}\nScore: {reflection.score}",
                    "reflection_round": reflection_round,
                    "reflection_score": reflection.normalized_score,
                    "reflection_history": reflection_history,
                }

                # Check if this is a solution or we've reached max rounds
                if (
                    reflection.found_solution
                    or reflection_round >= self.config.reflection.max_reflection_rounds
                ):
                    return Command(update=state_update, goto="end")

                return Command(update=state_update, goto="continue")

            except Exception as e:
                logger.error(f"Error in reflection: {e}")
                return Command(update=state, goto="end")

        return reflection_function

    def _create_search_function(self):
        """Create a function for the search node."""
        from langchain_core.prompts import ChatPromptTemplate

        # Create prompt template for generating search queries
        search_query_prompt = ChatPromptTemplate.from_template(
            self.config.reflection.search_query_prompt_template
        )

        def search_function(state: ReflectionAgentState) -> dict[str, Any]:
            try:
                # Extract needed fields
                original_request = state.original_request
                response = state.response
                feedback = state.feedback

                if not original_request or not response or not feedback:
                    logger.warning("Missing required fields for search")
                    return state

                # Construct search query input
                search_input = {
                    "original_request": original_request,
                    "response": response,
                    "feedback": feedback,
                }

                # Generate search queries
                search_result = self.engine.invoke(
                    search_query_prompt.format(**search_input)
                )

                if hasattr(search_result, "content"):
                    queries_text = search_result.content
                else:
                    queries_text = str(search_result)

                # Parse queries (simple line splitting)
                queries = [q.strip() for q in queries_text.split("\n") if q.strip()]

                # Limit to 3 queries
                queries = queries[:3]

                # If queries were successfully generated, add them to state
                if queries:
                    # Here you would typically call an actual search tool
                    # For now, we'll just store the queries
                    return {**state.model_dump(), "search_queries": queries}

                return state

            except Exception as e:
                logger.error(f"Error in search: {e}")
                return state

        return search_function

    def _create_improvement_function(self):
        """Create a function for the improvement node."""
        from langchain_core.prompts import ChatPromptTemplate

        # Create prompt template for improvement
        improvement_prompt = ChatPromptTemplate.from_template(
            self.config.reflection.improvement_prompt_template
        )

        def improvement_function(state: ReflectionAgentState) -> dict[str, Any]:
            try:
                # Extract needed fields
                original_request = state.original_request
                response = state.response
                feedback = state.feedback
                search_queries = state.search_queries

                if not original_request or not response or not feedback:
                    logger.warning("Missing required fields for improvement")
                    return state

                # Construct improvement input
                improvement_input = {
                    "original_request": original_request,
                    "response": response,
                    "feedback": feedback,
                }

                # Add search queries if available
                if search_queries:
                    improvement_input["search_queries"] = "\n".join(search_queries)
                    improvement_prompt.template += (
                        "\n\nAdditional search queries to consider:\n{search_queries}"
                    )

                # Generate improved response
                improved_result = self.engine.invoke(
                    improvement_prompt.format(**improvement_input)
                )

                if hasattr(improved_result, "content"):
                    improved_content = improved_result.content
                else:
                    improved_content = str(improved_result)

                # Create a new AI message with the improved content
                messages = state.messages.copy()

                # Replace the last AI message or add a new one
                new_messages = []
                replaced = False
                for msg in messages:
                    if not replaced and (
                        isinstance(msg, AIMessage) or getattr(msg, "type", None) == "ai"
                    ):
                        new_messages.append(AIMessage(content=improved_content))
                        replaced = True
                    else:
                        new_messages.append(msg)

                if not replaced:
                    new_messages.append(AIMessage(content=improved_content))

                # Update state with improved response
                return {
                    **state.model_dump(),
                    "messages": new_messages,
                    "response": improved_content,
                    "improved_response": improved_content,
                }

            except Exception as e:
                logger.error(f"Error in improvement: {e}")
                return state

        return improvement_function

    def _create_evaluation_function(self):
        """Create a function to evaluate if the improved response is good enough."""

        def evaluation_function(state: ReflectionAgentState) -> dict[str, Any]:
            """Simple evaluation based on round count and auto-accept threshold."""
            reflection_round = state.reflection_round
            max_rounds = self.config.reflection.max_reflection_rounds
            reflection_score = state.reflection_score or 0.0
            auto_threshold = self.config.reflection.auto_accept_threshold or 1.0

            # Check if we've reached max rounds
            if reflection_round >= max_rounds:
                logger.info(f"Reached maximum reflection rounds: {reflection_round}")
                return Command(update=state, goto="end")

            # Check if we've reached the acceptance threshold
            if reflection_score >= auto_threshold:
                logger.info(
                    f"Response quality meets auto-accept threshold: {reflection_score} >= {auto_threshold}"
                )
                return Command(update=state, goto="end")

            # Continue for another round
            logger.info(
                f"Continuing reflection: round {reflection_round}, score {reflection_score}"
            )
            return Command(update=state, goto="continue")

        return evaluation_function

    def _should_continue_reflection(self, state: ReflectionAgentState) -> str:
        """Determine if we should continue to the search/improvement step or end."""
        # Check if reflection is disabled
        if not self.config.reflection.enabled:
            return "end"

        # Check if we've reached the max rounds
        if state.reflection_round >= self.config.reflection.max_reflection_rounds:
            return "end"

        # Check if we've reached the auto-accept threshold
        auto_threshold = self.config.reflection.auto_accept_threshold or 1.0
        if state.reflection_score and state.reflection_score >= auto_threshold:
            return "end"

        # Otherwise continue
        return "continue"

    def _should_continue_improvement(self, state: ReflectionAgentState) -> str:
        """Determine if we should continue with another reflection round or end."""
        # Check if we've reached the max rounds
        if state.reflection_round >= self.config.reflection.max_reflection_rounds:
            return "end"

        # Check if we've reached the auto-accept threshold
        auto_threshold = self.config.reflection.auto_accept_threshold or 1.0
        if state.reflection_score and state.reflection_score >= auto_threshold:
            return "end"

        # Otherwise continue
        return "continue"
