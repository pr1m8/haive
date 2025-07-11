import unittest
from typing import Any, Optional

from haive_agents_dep.simple.agent import SimpleAgent

# Import SimpleAgentConfig and SimpleAgent
from haive_agents_dep.simple.config import SimpleAgentConfig
from pydantic import Field, create_model

from haive.core.config.runnable import RunnableConfigManager

# Import agent components
from haive.core.engine.aug_llm import AugLLMConfig

# Import core engine classes
from haive.core.engine.embeddings import EmbeddingsEngineConfig
from haive.core.engine.retriever import BaseRetrieverConfig, RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig

# Import graph building components
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.schema.SchemaComposer import SchemaComposer
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig

# Sample schema model for testing - using create_model to avoid constructor issues
TestStateModel = create_model(
    "TestStateModel",
    query=(str, ""),
    context=(Optional[str], None),
    answer=(Optional[str], None),
    messages=(list[Any], Field(default_factory=list)),
    runnable_config=(dict[str, Any], Field(default_factory=dict)),
    __config__=type("Config", (), {"arbitrary_types_allowed": True}),
)


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        # Create base configurations for engines
        self.llm_config = AugLLMConfig(
            name="test_llm",
            llm_config={"provider": "azure", "model": "gpt-4o"},
            prompt_template=None,  # Set to None to avoid validation errors
        )

        self.embeddings_config = EmbeddingsEngineConfig(
            name="test_embeddings",
            embedding_config=HuggingFaceEmbeddingConfig(
                model="sentence-transformers/all-mpnet-base-v2"
            ),
        )

        self.vectorstore_config = VectorStoreConfig(
            name="test_vectorstore",
            vector_store_provider="FAISS",
            embedding_model=self.embeddings_config.embedding_config,
        )

        self.retriever_config = BaseRetrieverConfig.from_retriever_type(
            RetrieverType.VECTOR_STORE,
            name="test_retriever",
            vector_store_config=self.vectorstore_config,
            k=4,
        )

    def test_schema_derivation(self):
        """Test that schemas can be properly derived from engines."""
        # Test deriving schema from a single engine
        llm_schema = self.llm_config.derive_input_schema()
        self.assertIsNotNone(llm_schema)

        retriever_schema = self.retriever_config.derive_input_schema()
        self.assertIsNotNone(retriever_schema)

        # Test composing schemas from multiple engines
        components = [self.llm_config, self.retriever_config]
        composed_schema = SchemaComposer.compose_schema(
            components, name="TestComposedSchema"
        )

        # Check if the composed schema has expected fields - for Pydantic models, we check their fields
        self.assertTrue(
            hasattr(composed_schema, "model_fields")
            or hasattr(composed_schema, "__fields__")
        )

        # Get the field names based on Pydantic version
        if hasattr(composed_schema, "model_fields"):  # Pydantic v2
            field_names = composed_schema.model_fields.keys()
        else:  # Pydantic v1
            field_names = composed_schema.__fields__.keys()

        # Verify fields exist
        self.assertIn("messages", field_names)
        self.assertIn("query", field_names)

    def test_dynamic_graph_building(self):
        """Test building a graph with different engines."""
        # Create a dynamic graph with component-derived schema
        graph = DynamicGraph(
            name="test_rag_graph", components=[self.retriever_config, self.llm_config]
        )

        # Add retriever node
        graph.add_node(
            name="retrieve", config=self.retriever_config, command_goto="generate"
        )

        # Add LLM node
        graph.add_node(name="generate", config=self.llm_config, command_goto="END")

        # Set entry point
        graph.set_entry_point("retrieve")

        # Build the graph
        built_graph = graph.build()

        # Test the graph structure
        self.assertEqual(len(graph.graph_editor.nodes), 2)
        self.assertEqual(graph.graph_editor.entry_point, "retrieve")

    def test_runnable_config_integration(self):
        """Test that runnable_config is properly propagated."""
        # Create a runnable config
        config = RunnableConfigManager.create(
            thread_id="test_thread",
            user_id="test_user",
            model="gpt-4o-mini",
            temperature=0.7,
        )

        # Set it as the default for a graph
        graph = DynamicGraph(
            name="test_graph_with_config",
            components=[self.llm_config],
            default_runnable_config=config,
        )

        graph.add_node("generate", config=self.llm_config, command_goto="END")
        built_graph = graph.build()

        # Verify the config is set
        self.assertIsNotNone(graph.default_runnable_config)
        self.assertEqual(
            graph.default_runnable_config["configurable"]["thread_id"], "test_thread"
        )

    def test_agent_construction(self):
        """Test creating an agent with the actual SimpleAgent implementation."""
        # Create a prompt template
        from langchain_core.messages import SystemMessage
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        messages = [
            SystemMessage(content="You are a helpful assistant."),
            MessagesPlaceholder(variable_name="messages"),
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Create the LLM config
        llm_config = AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})

        # Create the AugLLM config
        aug_llm = AugLLMConfig(
            name="test_llm", llm_config=llm_config, prompt_template=prompt_template
        )

        # Create the SimpleAgentConfig
        agent_config = SimpleAgentConfig.from_aug_llm(
            aug_llm=aug_llm,
            name="test_simple_agent",
            visualize=False,  # Don't generate visualization for tests
        )

        # Build the agent
        agent = SimpleAgent(config=agent_config)

        # Test that the agent is properly set up
        self.assertEqual(agent.config.name, "test_simple_agent")
        self.assertEqual(agent.config.engine.name, "test_llm")

        # Verify the workflow was set up
        self.assertIsNotNone(agent.graph)

        # Verify the schema includes message field
        schema_fields = agent_config.get_schema_fields()
        self.assertIn("messages", schema_fields)

        # Test that we can create a runnable
        runnable = agent_config.create_runnable()
        self.assertIsNotNone(runnable)


if __name__ == "__main__":
    unittest.main()
