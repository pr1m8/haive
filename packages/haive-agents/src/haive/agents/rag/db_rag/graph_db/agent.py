"""Graph Database RAG Agent implementation.

This module implements the main Graph Database RAG Agent that provides natural
language querying capabilities for Neo4j databases. The agent uses a multi-step
workflow to convert questions to Cypher queries, validate them, execute them,
and generate natural language responses.

The agent workflow consists of the following steps:
    1. **Domain Relevance Check**: Validates if the query is within the configured domain
    2. **Query Generation**: Converts natural language to Cypher using few-shot learning
    3. **Query Validation**: Checks the Cypher query against the database schema
    4. **Query Correction**: Fixes any errors found during validation
    5. **Query Execution**: Runs the validated query against Neo4j
    6. **Answer Generation**: Converts database results to natural language

Example:
    Basic usage of the Graph DB RAG Agent::

        >>> from haive.agents.rag.db_rag.graph_db import GraphDBRAGAgent, GraphDBRAGConfig
        >>>
        >>> # Configure the agent for a movie domain
        >>> config = GraphDBRAGConfig(
        ...     domain_name="movies",
        ...     domain_categories=["movie", "actor", "director"],
        ...     graph_db_config=GraphDBConfig(
        ...         graph_db_uri="bolt://localhost:7687",
        ...         graph_db_user="neo4j",
        ...         graph_db_password="password"
        ...     )
        ... )
        >>>
        >>> # Create and use the agent
        >>> agent = GraphDBRAGAgent(config)
        >>> result = agent.invoke({"question": "Who directed The Matrix?"})
        >>> print(result["answer"])
        The Wachowskis directed The Matrix.

    Using the agent with streaming::

        >>> # Stream the workflow execution
        >>> for chunk in agent.stream({"question": "What are the top 5 rated movies?"}):
        ...     if "answer" in chunk:
        ...         print(chunk["answer"])

Note:
    The agent requires a connection to a Neo4j database and uses environment
    variables for configuration if not explicitly provided.

See Also:
    - :class:`GraphDBRAGConfig`: Configuration options for the agent
    - :class:`OverallState`: State management during workflow execution
    - :mod:`haive.agents.rag.db_rag.graph_db.engines`: LLM engines used by the agent
"""

import json
import logging
import os

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.branches import Branch
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_neo4j.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.rag.db_rag.graph_db.config import GraphDBRAGConfig
from haive.agents.rag.db_rag.graph_db.state import OverallState

logger = logging.getLogger(__name__)


@register_agent(GraphDBRAGConfig)
class GraphDBRAGAgent(Agent[GraphDBRAGConfig]):
    """Graph Database RAG Agent for natural language querying of Neo4j databases.

    This agent implements a sophisticated workflow for converting natural language
    questions into Cypher queries, executing them against a Neo4j database, and
    generating human-readable responses. It includes domain validation, query
    validation, error correction, and result formatting.

    The agent uses few-shot learning with domain-specific examples to improve
    query generation accuracy and includes robust error handling for common
    Cypher mistakes.

    Attributes:
        config (GraphDBRAGConfig): Configuration object containing all settings.
        graph_db (Neo4jGraph): Connected Neo4j database instance.
        graph_db_enhanced_schema: Enhanced schema information from the database.
        graph_db_structured_schema: Structured schema for relationship validation.
        corrector_schema: Schema used for correcting relationship directions.
        cypher_query_corrector: Utility for fixing common Cypher errors.
        example_selector: Semantic similarity selector for few-shot examples.
        no_results (str): Default message when no results are found.

    Example:
        Creating and using the agent::

            >>> # Create agent with minimal config
            >>> agent = GraphDBRAGAgent()
            >>>
            >>> # Query the database
            >>> result = agent.invoke({
            ...     "question": "What movies has Tom Hanks acted in?"
            ... })
            >>> print(f"Answer: {result['answer']}")
            >>> print(f"Cypher used: {result['cypher_statement']}")

            >>> # Use with custom domain
            >>> config = GraphDBRAGConfig(
            ...     domain_name="healthcare",
            ...     domain_categories=["patient", "doctor", "medication"]
            ... )
            >>> healthcare_agent = GraphDBRAGAgent(config)

    Note:
        The agent automatically sets up the workflow graph upon initialization.
        All node functions return Command objects for state updates and routing.
    """

    def __init__(self, config: GraphDBRAGConfig = GraphDBRAGConfig()):
        """Initialize the Graph DB RAG Agent.

        Sets up the Neo4j connection, schema information, example selector,
        and workflow graph. Handles initialization errors gracefully with
        appropriate logging.

        Args:
            config: Configuration object. Defaults to GraphDBRAGConfig() which
                uses environment variables for Neo4j connection.

        Raises:
            ValueError: If Neo4j connection cannot be established.
            Exception: For other initialization errors.

        Example:
            >>> # Using default config (from environment)
            >>> agent = GraphDBRAGAgent()

            >>> # Using custom config
            >>> custom_config = GraphDBRAGConfig(
            ...     domain_name="movies",
            ...     graph_db_config=GraphDBConfig(
            ...         graph_db_uri="bolt://localhost:7687"
            ...     )
            ... )
            >>> agent = GraphDBRAGAgent(custom_config)
        """
        self._initialize_config(config)
        super().__init__(config)

    def _initialize_config(self, config: GraphDBRAGConfig) -> None:
        """Initialize configuration and core components.

        Sets up the Neo4j connection, retrieves schema information, configures
        the Cypher query corrector, and initializes the example selector for
        few-shot learning.

        Args:
            config: The configuration object containing all settings.

        Raises:
            ValueError: If Neo4j connection fails.
            Exception: For other initialization errors.

        Note:
            This method is called automatically during __init__ and should not
            be called directly.
        """
        try:
            # Initialize graph database connection
            self.graph_db = config.graph_db_config.get_graph_db()
            if not self.graph_db:
                raise ValueError("Failed to connect to Neo4j database")

            # Get schema information
            self.graph_db_enhanced_schema = self.graph_db.schema
            self.graph_db_structured_schema = self.graph_db.structured_schema

            # Set up corrector schema for relationship direction correction
            self.corrector_schema = [
                Schema(el["start"], el["type"], el["end"])
                for el in self.graph_db_structured_schema.get("relationships", [])
            ]

            self.cypher_query_corrector = CypherQueryCorrector(self.corrector_schema)
            self.no_results = "No results found"

            # Initialize example selector
            self._initialize_example_selector(config)

        except Exception as e:
            logger.error(f"Error initializing GraphDBRAGAgent: {e}")
            raise

    def _initialize_example_selector(self, config: GraphDBRAGConfig) -> None:
        """Initialize the semantic example selector for few-shot learning.

        Creates an example selector that retrieves relevant query examples based
        on semantic similarity. Falls back to simpler selection methods if
        vector-based selection fails.

        Args:
            config: Configuration containing example settings and domain info.

        Note:
            The selector prioritizes examples in this order:
            1. Domain-specific examples from config
            2. Examples loaded from file (if specified)
            3. Default examples for the domain
            4. General fallback examples
        """
        try:
            # Check if we have domain-specific examples
            domain_examples = []

            # Try to get examples for the configured domain
            if (
                hasattr(config, "domain_examples")
                and config.domain_name in config.domain_examples
            ):
                domain_examples = config.domain_examples[config.domain_name]

            # Try to load examples from a file if specified
            if hasattr(config, "example_config") and config.example_config:
                examples_path = config.example_config.examples_path
                if examples_path and os.path.exists(examples_path):
                    with open(examples_path) as f:
                        domain_examples = json.load(f)
                elif config.example_config.examples:
                    domain_examples = config.example_config.examples

            # Default examples if none are provided
            if not domain_examples:
                # Get default examples for the domain
                domain_examples = self._get_default_examples(config.domain_name)

            # Create documents for embedding
            documents = [
                Document(
                    page_content=ex["query"], metadata={"question": ex["question"]}
                )
                for ex in domain_examples
            ]

            # Try to use OpenAI embeddings, falling back to default if not available
            try:
                embedding = OpenAIEmbeddings()
                vectorstore = Chroma.from_documents(
                    documents, embedding, collection_name="cypher_examples"
                )
                self.example_selector = SemanticSimilarityExampleSelector(
                    vectorstore=vectorstore,
                    k=(
                        getattr(config, "example_config", {}).get("k", 2)
                        if hasattr(config, "example_config")
                        else 2
                    ),
                    input_keys=["question"],
                )
            except Exception as e:
                logger.warning(f"Failed to initialize semantic example selector: {e}")
                # Simple fallback - just use all examples
                self.example_selector = type(
                    "SimpleSelector",
                    (),
                    {"select_examples": lambda self, query: domain_examples},
                )()

        except Exception as e:
            logger.error(f"Error initializing example selector: {e}")
            # Create a dummy selector that returns empty examples if all else fails
            self.example_selector = type(
                "DummySelector", (), {"select_examples": lambda self, query: []}
            )()

    def _get_default_examples(self, domain_name: str) -> list[dict[str, str]]:
        """Get default examples for the specified domain.

        Provides pre-defined examples for common domains to help with few-shot
        learning when custom examples are not provided.

        Args:
            domain_name: The name of the domain (e.g., "movies", "healthcare").

        Returns:
            List of example dictionaries, each containing:
                - question: Natural language question
                - query: Corresponding Cypher query

        Example:
            >>> agent = GraphDBRAGAgent()
            >>> examples = agent._get_default_examples("movies")
            >>> print(examples[0])
            {
                "question": "Which movie has the highest rating?",
                "query": "MATCH (m:Movie) RETURN m.title, m.rating ORDER BY m.rating DESC LIMIT 1"
            }
        """
        # Default examples by domain
        default_examples = {
            "movies": [
                {
                    "question": "Which movie has the highest rating?",
                    "query": "MATCH (m:Movie) RETURN m.title, m.rating ORDER BY m.rating DESC LIMIT 1",
                },
                {
                    "question": "Who directed The Matrix?",
                    "query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'The Matrix'}) RETURN p.name",
                },
                {
                    "question": "What are the top 5 highest-rated movies?",
                    "query": "MATCH (m:Movie) RETURN m.title, m.rating ORDER BY m.rating DESC LIMIT 5",
                },
            ],
            "healthcare": [
                {
                    "question": "Which patients have diabetes?",
                    "query": "MATCH (p:Patient)-[:HAS_CONDITION]->(c:Condition {name: 'Diabetes'}) RETURN p.name",
                },
                {
                    "question": "What medications are prescribed for hypertension?",
                    "query": "MATCH (m:Medication)<-[:PRESCRIBED]-(c:Condition {name: 'Hypertension'}) RETURN m.name",
                },
                {
                    "question": "Who are the doctors specializing in cardiology?",
                    "query": "MATCH (d:Doctor {specialty: 'Cardiology'}) RETURN d.name",
                },
            ],
            # Add more domains as needed
            "general": [
                {
                    "question": "What are the connections between A and B?",
                    "query": "MATCH (a)-[r]-(b) RETURN a, r, b LIMIT 10",
                },
                {
                    "question": "What properties does node type X have?",
                    "query": "MATCH (x:X) RETURN x LIMIT 1",
                },
                {
                    "question": "How many relationships exist in the database?",
                    "query": "MATCH ()-[r]->() RETURN count(r)",
                },
            ],
        }

        return default_examples.get(domain_name, default_examples["general"])

    def check_domain_relevance(self, state: OverallState) -> Command:
        """Check if the user's question is relevant to the configured domain.

        This is the first step in the workflow. It uses the guardrails engine
        to determine if the question should be processed or rejected as
        out-of-domain.

        Args:
            state: Current workflow state containing the user's question.

        Returns:
            Command object with updates:
                - next_action: "end" if out-of-domain, otherwise continue
                - database_records: Error message if out-of-domain
                - steps: Updated with "check_domain_relevance"

        Example:
            >>> state = OverallState(question="What's the weather like?")
            >>> command = agent.check_domain_relevance(state)
            >>> # For a movie domain agent, this would return:
            >>> # Command(update={"next_action": "end", ...})

        Note:
            This node acts as a guardrail to prevent processing of irrelevant
            queries, saving computational resources and improving accuracy.
        """
        try:
            # Get domain information
            domain_name = self.config.domain_name
            domain_categories = self.config.domain_categories

            # If no categories defined, default to domain name
            if not domain_categories:
                domain_categories = [domain_name]

            # Default category to use
            category = domain_categories[0] if domain_categories else domain_name

            # Invoke the guardrails engine
            guardrails_output = self.engines["guardrails"].invoke(
                {
                    "question": state.question,
                    "domain_name": domain_name,
                    "category": category,
                }
            )

            database_records = None

            # Handle the output - it might be an AIMessage or a structured output
            if hasattr(guardrails_output, "decision"):
                # It's a structured GuardrailsOutput
                decision = guardrails_output.decision
            elif hasattr(guardrails_output, "content"):
                # It's an AIMessage - try to parse the content
                try:
                    import json

                    content = guardrails_output.content
                    if isinstance(content, str):
                        parsed = json.loads(content)
                        decision = parsed.get("decision", "continue")
                    else:
                        decision = "continue"  # Default if we can't parse
                except:
                    # If parsing fails, default to continue
                    decision = "continue"
            else:
                # Unknown output type, default to continue
                decision = "continue"

            if decision == "end":
                database_records = f"This question is not about {domain_name}. Therefore I cannot answer this question."

            return Command(
                update={
                    "next_action": decision,
                    "database_records": database_records,
                    "steps": ["check_domain_relevance"],
                }
            )
        except Exception as e:
            logger.error(f"Error in check_domain_relevance: {e}")
            return Command(
                update={
                    "error": f"Error checking domain relevance: {e!s}",
                    "next_action": "end",
                }
            )

    def generate_query(self, state: OverallState) -> Command:
        """Generate a Cypher query from the natural language question.

        Uses the text2cypher engine with few-shot examples to convert the
        user's question into a valid Cypher query for the database schema.

        Args:
            state: Current state containing the user's question.

        Returns:
            Command object with updates:
                - cypher_statement: The generated Cypher query
                - steps: Updated with "generate_query"

        Example:
            >>> state = OverallState(question="Who directed Inception?")
            >>> command = agent.generate_query(state)
            >>> print(command.update["cypher_statement"])
            MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: 'Inception'}) RETURN p.name

        Note:
            The quality of generation depends heavily on the provided examples
            and their similarity to the user's question.
        """
        try:
            if "text2cypher" not in self.engines:
                raise ValueError("Missing 'text2cypher' engine in configuration")

            # Get examples for few-shot learning
            examples = self.example_selector.select_examples(
                {"question": state.question}
            )

            fewshot_examples = "\n".join(
                [
                    f"Question: {example['question']}\nCypher query: {example['query']}"
                    for example in examples
                ]
            )

            cypher_statement = self.engines["text2cypher"].invoke(
                {"question": state.question, "fewshot_examples": fewshot_examples}
            )

            logger.info(f"Generated Cypher query: {cypher_statement}")

            return Command(
                update={
                    "cypher_statement": cypher_statement,
                    "steps": state.steps + ["generate_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in generate_query: {e}")
            return Command(
                update={
                    "error": f"Error generating Cypher query: {e!s}",
                    "next_action": "end",
                }
            )

    def validate_query(self, state: OverallState) -> Command:
        """Validate the generated Cypher query against the database schema.

        Checks for syntax errors, schema mismatches, and logical issues in
        the generated query. Routes to correction if errors are found.

        Args:
            state: Current state containing the Cypher statement to validate.

        Returns:
            Command object with updates:
                - next_action: "correct_cypher" if errors, "execute_query" if valid
                - cypher_errors: List of validation errors (if any)
                - steps: Updated with "validate_query"

        Example:
            >>> state = OverallState(
            ...     cypher_statement="MATCH (p:Actor)-[:DIRECTED]->(m:Film) RETURN p.name"
            ... )
            >>> command = agent.validate_query(state)
            >>> # Would return errors about "Film" label and "Actor" directing

        Note:
            Validation checks include label existence, property names,
            relationship types, and query completeness.
        """
        try:
            if "validate_cypher" not in self.engines:
                raise ValueError("Missing 'validate_cypher' engine in configuration")

            validation_result = self.engines["validate_cypher"].invoke(
                {
                    "question": state.question,
                    "cypher": state.cypher_statement,
                    "schema": self.graph_db_enhanced_schema.schema,
                }
            )

            if validation_result.is_valid == False:
                return Command(
                    update={
                        "next_action": "correct_cypher",
                        "cypher_errors": validation_result.errors,
                        "steps": state.steps + ["validate_query"],
                    }
                )
            return Command(
                update={
                    "next_action": "execute_query",
                    "steps": state.steps + ["validate_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in validate_query: {e}")
            return Command(
                update={
                    "error": f"Error validating Cypher query: {e!s}",
                    "next_action": "end",
                }
            )

    def correct_query(self, state: OverallState) -> Command:
        """Correct errors in the Cypher query based on validation feedback.

        Uses the correct_cypher engine to fix identified errors and produce
        a valid query that matches the database schema.

        Args:
            state: Current state containing the invalid query and errors.

        Returns:
            Command object with updates:
                - next_action: "validate_query" (to re-validate)
                - cypher_statement: The corrected Cypher query
                - steps: Updated with "correct_query"

        Example:
            >>> state = OverallState(
            ...     cypher_statement="MATCH (p:Actor)-[:DIRECTED]->(m:Film) RETURN p.name",
            ...     cypher_errors=["Label 'Film' does not exist, use 'Movie'"]
            ... )
            >>> command = agent.correct_query(state)
            >>> print(command.update["cypher_statement"])
            MATCH (p:Person)-[:DIRECTED]->(m:Movie) RETURN p.name

        Note:
            The corrected query is sent back to validation to ensure
            all errors are resolved.
        """
        try:
            if "correct_cypher" not in self.engines:
                raise ValueError("Missing 'correct_cypher' engine in configuration")

            corrected_cypher = self.engines["correct_cypher"].invoke(
                {
                    "question": state.question,
                    "errors": state.cypher_errors,
                    "cypher": state.cypher_statement,
                    "schema": self.graph_db_enhanced_schema.schema,
                }
            )

            return Command(
                update={
                    "next_action": "validate_query",
                    "cypher_statement": corrected_cypher,
                    "steps": state.steps + ["correct_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in correct_query: {e}")
            return Command(
                update={
                    "error": f"Error correcting Cypher query: {e!s}",
                    "next_action": "end",
                }
            )

    def execute_query(self, state: OverallState) -> Command:
        """Execute the validated Cypher query against the Neo4j database.

        Runs the query and captures the results for answer generation.
        Handles empty results gracefully.

        Args:
            state: Current state containing the validated Cypher statement.

        Returns:
            Command object with updates:
                - database_records: Query results or "No results found"
                - next_action: "generate_answer"
                - steps: Updated with "execute_query"

        Example:
            >>> state = OverallState(
            ...     cypher_statement="MATCH (m:Movie) RETURN m.title LIMIT 3"
            ... )
            >>> command = agent.execute_query(state)
            >>> print(command.update["database_records"])
            [{"m.title": "The Matrix"}, {"m.title": "Inception"}, ...]

        Note:
            The query is executed with proper sanitization and timeout
            settings configured in the Neo4j connection.
        """
        try:
            records = self.graph_db.query(state.cypher_statement)

            return Command(
                update={
                    "database_records": records if records else self.no_results,
                    "next_action": "generate_answer",
                    "steps": state.steps + ["execute_query"],
                }
            )
        except Exception as e:
            logger.error(f"Error in execute_query: {e}")
            return Command(
                update={
                    "error": f"Error executing Cypher query: {e!s}",
                    "next_action": "end",
                }
            )

    def generate_answer(self, state: OverallState) -> Command:
        """Generate a natural language answer from the query results.

        Uses the generate_final_answer engine to convert database records
        into a human-friendly response that directly answers the question.

        Args:
            state: Current state containing question and database results.

        Returns:
            Command object with updates:
                - answer: The natural language response
                - next_action: "end"
                - steps: Updated with "generate_answer"

        Example:
            >>> state = OverallState(
            ...     question="Who directed The Matrix?",
            ...     database_records=[{"p.name": "Lana Wachowski"}, {"p.name": "Lilly Wachowski"}]
            ... )
            >>> command = agent.generate_answer(state)
            >>> print(command.update["answer"])
            The Matrix was directed by Lana Wachowski and Lilly Wachowski.

        Note:
            The engine is prompted to provide direct, conversational answers
            without mentioning the database or technical details.
        """
        try:
            if "generate_final_answer" not in self.engines:
                raise ValueError(
                    "Missing 'generate_final_answer' engine in configuration"
                )

            if state.database_records == self.no_results:
                answer = f"I couldn't find any information about your question: {state.question}"
            else:
                answer = self.engines["generate_final_answer"].invoke(
                    {"question": state.question, "results": state.database_records}
                )

            return Command(
                update={
                    "answer": answer,
                    "next_action": "end",
                    "steps": state.steps + ["generate_answer"],
                }
            )
        except Exception as e:
            logger.error(f"Error in generate_answer: {e}")
            return Command(
                update={
                    "error": f"Error generating answer: {e!s}",
                    "answer": f"An error occurred while generating the answer: {e!s}",
                    "next_action": "end",
                }
            )

    def domain_router(self, state: OverallState) -> str:
        """Route based on domain relevance check result.

        Args:
            state: Current state with next_action field.

        Returns:
            str: Next node name - END if out-of-domain, "generate_query" otherwise.

        Note:
            This is used as a conditional edge function in the workflow graph.
        """
        if state.next_action == "end":
            return END
        return "generate_query"

    def validation_router(self, state: OverallState) -> str:
        """Route based on query validation result.

        Args:
            state: Current state with next_action field.

        Returns:
            str: Next node name - "correct_query", "execute_query", or END.

        Note:
            This is used as a conditional edge function in the workflow graph.
        """
        if state.next_action == "end":
            return END
        if state.next_action == "correct_cypher":
            return "correct_query"
        return "execute_query"

    def setup_workflow(self) -> None:
        """Set up the complete Graph DB RAG workflow.

        Configures the workflow graph with all nodes and edges, including
        conditional routing based on validation results. This method is
        called automatically during agent initialization.

        The workflow structure::

            START
              ↓
            check_domain_relevance
              ↓ (conditional)
            generate_query ← ─ ─ ─ ┐
              ↓                    │
            validate_query         │
              ↓ (conditional)     │
            correct_query ─ ─ ─ ─ ─┘
              ↓
            execute_query
              ↓
            generate_answer
              ↓
            END

        Note:
            The workflow includes loops for query correction and multiple
            exit points for error handling.
        """
        # Add nodes for the workflow
        self.graph.add_node("check_domain_relevance", self.check_domain_relevance)
        self.graph.add_node("generate_query", self.generate_query)
        self.graph.add_node("validate_query", self.validate_query)
        self.graph.add_node("correct_query", self.correct_query)
        self.graph.add_node("execute_query", self.execute_query)
        self.graph.add_node("generate_answer", self.generate_answer)

        # Connect nodes
        self.graph.add_edge(START, "check_domain_relevance")

        # Add conditional edges using Branch directly
        domain_branch = Branch(
            key="next_action",
            destinations={"end": END, "generate_query": "generate_query"},
            default="generate_query",
        )

        self.graph.add_conditional_edges(
            "check_domain_relevance",
            domain_branch,  # Branch object can be called directly
            domain_branch.destinations,  # Pass the destinations mapping
        )

        self.graph.add_edge("generate_query", "validate_query")

        # Validation branch
        validation_branch = Branch(
            key="next_action",
            destinations={
                "correct_cypher": "correct_query",
                "execute_query": "execute_query",
                "end": END,
            },
            default="execute_query",
        )

        self.graph.add_conditional_edges(
            "validate_query", validation_branch, validation_branch.destinations
        )

        self.graph.add_edge("correct_query", "validate_query")
        self.graph.add_edge("execute_query", "generate_answer")
        self.graph.add_edge("generate_answer", END)

        logger.info("Graph DB RAG workflow setup complete")
