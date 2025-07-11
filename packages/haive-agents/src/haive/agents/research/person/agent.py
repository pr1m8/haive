"""Person research agent for comprehensive person information gathering.

This module implements a sophisticated person research agent that combines web search,
structured extraction, and iterative refinement to gather comprehensive information
about individuals. The agent is particularly useful for research tasks requiring
detailed personal profiles, biographical information, or professional backgrounds.

The agent workflow includes:
1. Query generation based on the target person and desired information schema
2. Web search execution using multiple search engines (Tavily integration)
3. Information extraction and note-taking from search results
4. Structured data extraction according to user-defined schemas
5. Reflection and completeness assessment
6. Iterative refinement until information quality meets requirements

Key Features:
- Configurable extraction schemas for different research needs
- Multi-source web search with relevance ranking
- Iterative research process with reflection and self-correction
- Structured output generation with validation
- Source attribution and credibility assessment
- Rate limiting and API quota management

Usage:
    ```python
    from haive.agents.research.person import PersonResearchAgent, PersonResearchAgentConfig

    # Configure the agent
    config = PersonResearchAgentConfig(
        name="person_researcher",
        target_person="Dr. Jane Smith",
        extraction_schema={
            "name": "Full name",
            "profession": "Current profession or role",
            "education": "Educational background",
            "achievements": "Notable achievements or awards"
        }
    )

    # Create and run the agent
    agent = PersonResearchAgent(config)
    result = await agent.ainvoke({
        "person": "Dr. Jane Smith, AI researcher",
        "research_depth": "comprehensive"
    })

    print(result.extracted_info)
    ```

The agent integrates with external services (Tavily) for web search and requires
appropriate API keys to function fully. It includes comprehensive error handling
and graceful degradation when external services are unavailable.
"""

import asyncio
import json
import logging
import os
from typing import Any, Literal, Optional, cast

# Import agent base classes
from haive.core.engine.agent.agent import Agent, register_agent
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from pydantic import create_model

# Import agent specific modules
from haive.agents.research.person.config import PersonResearchAgentConfig
from haive.agents.research.person.models import Queries, ReflectionOutput
from haive.agents.research.person.prompts import (
    EXTRACTION_PROMPT,
    INFO_PROMPT,
    QUERY_WRITER_PROMPT,
    REFLECTION_PROMPT,
)
from haive.agents.research.person.state import (
    PersonResearchInputState,
    PersonResearchOutputState,
    PersonResearchState,
)
from haive.agents.research.person.utils import (
    deduplicate_and_format_sources,
    format_all_notes,
    get_config_from_runnable_config,
)

# Set up logging
logger = logging.getLogger(__name__)

# Try to import Tavily client
try:
    from tavily import AsyncTavilyClient

    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    logger.warning("Tavily is not available. Install with 'pip install tavily'")


@register_agent(PersonResearchAgentConfig)
class PersonResearchAgent(Agent[PersonResearchAgentConfig]):
    """Advanced person research agent with iterative information gathering capabilities.

    This agent implements a sophisticated research workflow that systematically
    gathers, processes, and structures information about individuals using web
    search, content extraction, and iterative refinement techniques.

    The agent follows a multi-stage research process:
    1. Query Generation: Creates targeted search queries based on the person
       and desired information schema
    2. Web Search: Executes searches using the Tavily API for high-quality results
    3. Content Extraction: Processes search results and extracts relevant notes
    4. Structured Extraction: Converts notes into structured data following
       user-defined schemas
    5. Reflection: Evaluates information completeness and quality
    6. Iteration: Repeats the process with refined queries until satisfactory
       results are achieved or maximum iterations are reached

    The agent is designed to be highly configurable and can adapt to different
    research requirements by modifying the extraction schema, search parameters,
    and quality thresholds.

    Attributes:
        tavily_client: Optional Tavily API client for web searches.
        state_schema: Pydantic model defining the agent's internal state.
        input_schema: Pydantic model defining expected input format.
        output_schema: Pydantic model defining output format.

    Example:
        >>> config = PersonResearchAgentConfig(
        ...     name="researcher",
        ...     extraction_schema={"name": "Full name", "role": "Current position"}
        ... )
        >>> agent = PersonResearchAgent(config)
        >>> result = await agent.ainvoke({"person": "John Doe"})
    """

    def __init__(self, config: PersonResearchAgentConfig):
        """Initialize the person research agent with configuration and external services.

        Sets up the agent with the provided configuration, initializes the Tavily
        web search client if available, and prepares the agent for research operations.

        Args:
            config: Configuration object containing agent settings, API keys,
                   extraction schemas, and operational parameters.

        Raises:
            ValueError: If required configuration parameters are missing.
            ConnectionError: If external service initialization fails.

        Note:
            The Tavily client is optional - the agent will log a warning and
            continue with limited functionality if the API key is not available.
        """
        # Initialize the tavily client if available
        self.tavily_client = None
        if TAVILY_AVAILABLE:
            # Get API key from config or environment
            tavily_api_key = config.agent_settings.get(
                "tavily_api_key"
            ) or os.environ.get("TAVILY_API_KEY")
            if tavily_api_key:
                self.tavily_client = AsyncTavilyClient(api_key=tavily_api_key)
            else:
                logger.warning(
                    "No Tavily API key found. Web search will not be available."
                )

        # Call parent initializer
        super().__init__(config)

    def setup_workflow(self) -> None:
        """Set up the workflow graph for this agent."""
        logger.debug(f"Setting up workflow for PersonResearchAgent {self.config.name}")

        # Create state schema if not provided
        if not hasattr(self, "state_schema") or self.state_schema is None:
            self.state_schema = PersonResearchState

        # Create input/output schemas if not provided
        if not hasattr(self, "input_schema") or self.input_schema is None:
            self.input_schema = PersonResearchInputState

        if not hasattr(self, "output_schema") or self.output_schema is None:
            self.output_schema = PersonResearchOutputState

        # Create a graph builder with our schema
        builder = StateGraph(
            self.state_schema, input=self.input_schema, output=self.output_schema
        )

        # Add nodes
        builder.add_node("generate_queries", self.generate_queries)
        builder.add_node("research_person", self.research_person)
        builder.add_node(
            "gather_notes_extract_schema", self.gather_notes_extract_schema
        )
        builder.add_node("reflection", self.reflection)

        # Add edges
        builder.add_edge(START, "generate_queries")
        builder.add_edge("generate_queries", "research_person")
        builder.add_edge("research_person", "gather_notes_extract_schema")
        builder.add_edge("gather_notes_extract_schema", "reflection")
        builder.add_conditional_edges("reflection", self.route_from_reflection)

        # Set graph
        self.graph = builder

        logger.info(f"Workflow set up successfully for {self.config.name}")

    def generate_queries(
        self, state: PersonResearchState, config: RunnableConfig
    ) -> dict[str, Any]:
        """Generate search queries based on the user input and extraction schema.

        Args:
            state: Current state
            config: Runnable configuration

        Returns:
            Dict with search_queries field
        """
        # Get configuration
        agent_config = get_config_from_runnable_config(config)
        max_search_queries = agent_config.get(
            "max_search_queries",
            self.config.agent_settings.get("max_search_queries", 3),
        )

        # Get query generator engine
        query_generator = self.engines.get("query_generator", self.engine)

        # Format person string
        person_str = f"Email: {state.person.email}"
        if state.person.name:
            person_str += f" Name: {state.person.name}"
        if state.person.linkedin:
            person_str += f" LinkedIn URL: {state.person.linkedin}"
        if state.person.role:
            person_str += f" Role: {state.person.role}"
        if state.person.company:
            person_str += f" Company: {state.person.company}"

        # Prepare prompt
        query_instructions = QUERY_WRITER_PROMPT.format(
            person=person_str,
            info=json.dumps(state.extraction_schema, indent=2),
            user_notes=state.user_notes or "",
            max_search_queries=max_search_queries,
        )

        # Create structured LLM for queries
        structured_llm = query_generator.with_structured_output(Queries)

        # Generate queries
        results = cast(
            Queries,
            structured_llm.invoke(
                [
                    {"role": "system", "content": query_instructions.template},
                    {
                        "role": "user",
                        "content": "Please generate a list of search queries related to the schema that you want to populate.",
                    },
                ]
            ),
        )

        # Return queries
        query_list = list(results.queries)
        return {"search_queries": query_list}

    async def research_person(
        self, state: PersonResearchState, config: RunnableConfig
    ) -> dict[str, Any]:
        """Execute a multi-step web search and information extraction process.

        Args:
            state: Current state
            config: Runnable configuration

        Returns:
            Dict with completed_notes field
        """
        # Get configuration
        agent_config = get_config_from_runnable_config(config)
        max_search_results = agent_config.get(
            "max_search_results",
            self.config.agent_settings.get("max_search_results", 3),
        )

        # Check if Tavily client is available
        if not self.tavily_client:
            # Mock results if no Tavily client
            logger.warning("No Tavily client available. Using mock results.")
            return {
                "completed_notes": [
                    "No web search results available. Tavily API is not configured."
                ]
            }

        # Get researcher engine
        researcher = self.engines.get("researcher", self.engine)

        # Web search
        search_tasks = []
        for query in state.search_queries:
            search_tasks.append(
                self.tavily_client.search(
                    query,
                    days=360,
                    max_results=max_search_results,
                    include_raw_content=True,
                    topic="general",
                )
            )

        # Execute all searches concurrently
        search_docs = await asyncio.gather(*search_tasks)

        # Deduplicate and format sources
        source_str = deduplicate_and_format_sources(
            search_docs, max_tokens_per_source=1000, include_raw_content=True
        )

        # Format person string for the prompt
        person_str = f"Email: {state.person.email}"
        if state.person.name:
            person_str += f" Name: {state.person.name}"
        if state.person.role:
            person_str += f" Role: {state.person.role}"
        if state.person.company:
            person_str += f" Company: {state.person.company}"

        # Generate structured notes relevant to the extraction schema
        p = INFO_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2),
            content=source_str,
            people=person_str,
            user_notes=state.user_notes or "",
        )

        # Invoke the LLM
        result = await researcher.ainvoke(p)

        # Extract content from result
        if hasattr(result, "content"):
            notes_content = result.content
        elif isinstance(result, dict) and "content" in result:
            notes_content = result["content"]
        else:
            notes_content = str(result)

        return {"completed_notes": [notes_content]}

    def gather_notes_extract_schema(self, state: PersonResearchState) -> dict[str, Any]:
        """Gather notes from the web search and extract the schema fields.

        Args:
            state: Current state

        Returns:
            Dict with info field
        """
        # Get extractor engine
        extractor = self.engines.get("extractor", self.engine)

        # Format all notes
        notes = format_all_notes(state.completed_notes)

        # Create extraction prompt
        system_prompt = EXTRACTION_PROMPT.format(
            info=json.dumps(state.extraction_schema, indent=2), notes=notes
        )

        # Create dynamic schema model from extraction_schema
        dynamic_model = None
        try:
            # Get the schema properties
            properties = state.extraction_schema.get("properties", {})
            fields = {}

            # Convert JSON schema types to Python types
            type_mapping = {
                "string": str,
                "number": float,
                "integer": int,
                "boolean": bool,
                "array": list,
                "object": dict,
            }

            # Build fields dictionary for create_model
            for prop_name, prop_details in properties.items():
                prop_type = prop_details.get("type", "string")
                python_type = type_mapping.get(prop_type, str)

                # Handle arrays
                if prop_type == "array" and "items" in prop_details:
                    item_type = prop_details["items"].get("type", "string")
                    python_item_type = type_mapping.get(item_type, str)
                    python_type = list[python_item_type]

                # Make field optional with default None
                fields[prop_name] = (Optional[python_type], None)

            # Create dynamic model
            dynamic_model = create_model("DynamicExtractionModel", **fields)
        except Exception as e:
            logger.exception(f"Error creating dynamic model: {e}")
            dynamic_model = None

        # Extract schema fields using structured output if possible
        if dynamic_model:
            try:
                # Use structured output with dynamic model
                structured_llm = extractor.with_structured_output(dynamic_model)
                result = structured_llm.invoke(
                    [
                        {"role": "system", "content": system_prompt.template},
                        {
                            "role": "user",
                            "content": "Produce a structured output from these notes.",
                        },
                    ]
                )

                # Convert result to dict
                if hasattr(result, "model_dump"):
                    result_dict = result.model_dump()
                elif hasattr(result, "dict"):
                    result_dict = result.dict()
                else:
                    result_dict = {
                        k: getattr(result, k) for k in result.__annotations__
                    }

                return {"info": result_dict}
            except Exception as e:
                logger.exception(f"Error using structured output: {e}")

        # Fallback: use free-form extraction and parse the result
        try:
            result = extractor.invoke(
                [
                    {"role": "system", "content": system_prompt.template},
                    {
                        "role": "user",
                        "content": "Extract the information from these notes and format it as a JSON object matching the schema.",
                    },
                ]
            )

            # Try to parse JSON from the result
            result_content = None
            if hasattr(result, "content"):
                result_content = result.content
            elif isinstance(result, dict) and "content" in result:
                result_content = result["content"]
            else:
                result_content = str(result)

            # Extract JSON object from the text
            json_str = self._extract_json_from_text(result_content)
            if json_str:
                result_dict = json.loads(json_str)
                return {"info": result_dict}

            # If no JSON found, create a basic structure
            return {"info": {"error": "Could not extract structured data"}}
        except Exception as e:
            logger.exception(f"Error in fallback extraction: {e}")
            return {"info": {"error": f"Extraction failed: {e!s}"}}

    def route_from_reflection(
        self, state: PersonResearchState, config: RunnableConfig
    ) -> Literal[END, "research_person"]:
        """Route the graph based on the reflection output.

        Args:
            state: Current state
            config: Runnable configuration

        Returns:
            Next node to route to
        """
        # Get configuration
        agent_config = get_config_from_runnable_config(config)
        max_reflection_steps = agent_config.get(
            "max_reflection_steps",
            self.config.agent_settings.get("max_reflection_steps", 0),
        )

        # If we have satisfactory results, end the process
        if state.is_satisfactory:
            return END

        # If results aren't satisfactory but we haven't hit max steps, continue research
        if state.reflection_steps_taken <= max_reflection_steps:
            return "research_person"

        # If we've exceeded max steps, end even if not satisfactory
        return END

    def _extract_json_from_text(self, text: str) -> str | None:
        """Extract a JSON object from text.

        Args:
            text: Text to extract JSON from

        Returns:
            JSON string or None if not found
        """
        import re

        # Try to find JSON within code blocks
        json_match = re.search(r"```(?:json)?\s*\n(.*?)\n\s*```", text, re.DOTALL)
        if json_match:
            return json_match.group(1)

        # Try to find JSON with curly braces
        json_match = re.search(r"({.*})", text, re.DOTALL)
        if json_match:
            return json_match.group(1)

        # Try to find the entire text as JSON
        try:
            json.loads(text)
            return text
        except:
            pass

        return None

    def reflection(self, state: PersonResearchState) -> dict[str, Any]:
        """Reflect on the extracted information and generate search queries to find missing information.

        Args:
            state: Current state

        Returns:
            Dict with is_satisfactory field and optionally search_queries
        """
        # Get reflection engine
        reflection_engine = self.engines.get("reflection", self.engine)

        # Create structured LLM with reflection output
        structured_llm = reflection_engine.with_structured_output(ReflectionOutput)

        # Format reflection prompt
        system_prompt = REFLECTION_PROMPT.format(
            schema=json.dumps(state.extraction_schema, indent=2),
            info=json.dumps(state.info, indent=2),
        )

        # Invoke the model
        result = cast(
            ReflectionOutput,
            structured_llm.invoke(
                [
                    {"role": "system", "content": system_prompt.template},
                    {
                        "role": "user",
                        "content": "Produce a structured reflection output.",
                    },
                ]
            ),
        )

        # Return results
        if result.is_satisfactory:
            return {"is_satisfactory": result.is_satisfactory}
        return {
            "is_satisfactory": result.is_satisfactory,
            "search_queries": result.search_queries,
            "reflection_steps_taken": state.reflection_steps_taken + 1,
        }
