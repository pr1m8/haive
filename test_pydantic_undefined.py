"""
Test for PydanticUndefined issues in SchemaComposer and AugLLMConfig integration.
"""
import pytest
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.tool_state import ToolState
from haive.core.schema.prebuilt.messages_state import MessagesState


class QueryRefinementResponse(BaseModel):
    """Response model for query refinement with metadata tracking."""
    
    refined_query: str = Field(
        description="The refined search query optimized for retrieval"
    )
    original_intent: str = Field(
        description="The original user intent extracted from the query"
    )
    key_concepts: List[str] = Field(
        description="Key concepts and entities identified in the query",
        default_factory=list
    )
    search_strategy: str = Field(
        description="Recommended search strategy (e.g., 'semantic', 'keyword', 'hybrid')",
        default="semantic"
    )
    confidence_score: float = Field(
        description="Confidence score for the refinement quality (0-1)",
        ge=0.0,
        le=1.0,
        default=0.8
    )
    requires_clarification: bool = Field(
        description="Whether the query needs user clarification",
        default=False
    )
    clarification_questions: Optional[List[str]] = Field(
        description="Questions to ask if clarification is needed",
        default=None
    )


RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert query refinement assistant for a RAG (Retrieval-Augmented Generation) system.
    
Your task is to analyze user queries and refine them for optimal document retrieval. Consider:
1. Extract the core intent and information need
2. Identify key concepts, entities, and relationships
3. Optimize for semantic search while preserving meaning
4. Suggest the best search strategy
5. Flag queries that need clarification

Provide structured output with confidence scoring."""),
    
    ("human", "Original query: {query}\n\nContext (if any): {context}\n\nPlease refine this query for optimal retrieval.")
])


@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool  
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


class TestPydanticUndefinedFixes:
    """Test suite for PydanticUndefined issues in SchemaComposer integration."""
    
    def test_basic_augllm_config_schema_composition(self):
        """Test basic AugLLMConfig schema composition without PydanticUndefined."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        
        # Test schema composition
        schema = SchemaComposer.from_components(config)
        
        # Verify no PydanticUndefined values
        assert hasattr(schema, '__fields__'), "Schema should have fields"
        
        for field_name, field_info in schema.__fields__.items():
            assert field_info.default is not ..., f"Field {field_name} has PydanticUndefined default"
            if hasattr(field_info, 'annotation'):
                assert field_info.annotation is not ..., f"Field {field_name} has PydanticUndefined annotation"
        
        # Verify base class hierarchy - should prioritize LLMState
        mro = schema.__mro__
        base_classes = [cls.__name__ for cls in mro]
        print(f"MRO: {base_classes}")
        
        assert 'LLMState' in base_classes, "Schema should inherit from LLMState"
        assert 'ToolState' in base_classes, "Schema should inherit from ToolState"
        assert 'MessagesStateWithTokenUsage' in base_classes, "Schema should inherit from MessagesStateWithTokenUsage"
    
    def test_with_tools_schema_composition(self):
        """Test AugLLMConfig with tools - should still use LLMState base."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2',
            tools=[add, multiply]
        )
        
        schema = SchemaComposer.from_components(config)
        
        # Verify no PydanticUndefined values
        for field_name, field_info in schema.__fields__.items():
            assert field_info.default is not ..., f"Field {field_name} has PydanticUndefined default"
        
        # Should still prioritize LLMState even with tools
        mro = schema.__mro__
        base_classes = [cls.__name__ for cls in mro]
        assert 'LLMState' in base_classes, "Schema with tools should still inherit from LLMState"
    
    def test_without_structured_output(self):
        """Test AugLLMConfig without structured output."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT
        )
        
        schema = SchemaComposer.from_components(config)
        
        # Verify no PydanticUndefined values
        for field_name, field_info in schema.__fields__.items():
            assert field_info.default is not ..., f"Field {field_name} has PydanticUndefined default"
        
        # Should use LLMState as base
        mro = schema.__mro__
        base_classes = [cls.__name__ for cls in mro]
        assert 'LLMState' in base_classes, "Schema should inherit from LLMState"
    
    def test_complex_prompt_template(self):
        """Test with complex prompt template that has multiple input variables."""
        complex_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are processing: {task_type} with context: {context}"),
            ("human", "Query: {query}"),
            ("assistant", "Previous response: {previous_response}"),
            ("human", "Follow-up: {followup}")
        ])
        
        config = AugLLMConfig(
            prompt_template=complex_prompt,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        
        schema = SchemaComposer.from_components(config)
        
        # Verify no PydanticUndefined values
        for field_name, field_info in schema.__fields__.items():
            assert field_info.default is not ..., f"Field {field_name} has PydanticUndefined default"
        
        # Should handle multiple input variables properly
        mro = schema.__mro__
        base_classes = [cls.__name__ for cls in mro]
        assert 'LLMState' in base_classes, "Complex prompt schema should inherit from LLMState"
    
    def test_engine_type_detection(self):
        """Test that engine type is correctly detected as 'llm'."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        
        # Check engine type detection
        assert hasattr(config, 'engine_type'), "Config should have engine_type"
        assert config.engine_type == "llm", f"Expected engine_type 'llm', got '{config.engine_type}'"
    
    def test_schema_composer_base_class_priority(self):
        """Test that SchemaComposer correctly prioritizes LLMState for LLM engines."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        
        # Test the _detect_base_class_requirements method directly
        composer = SchemaComposer()
        base_class = composer._detect_base_class_requirements(config)
        
        assert base_class == LLMState, f"Expected LLMState, got {base_class}"
    
    def test_field_values_not_undefined(self):
        """Test that all field values are properly defined, not PydanticUndefined."""
        config = AugLLMConfig(
            prompt_template=RAG_QUERY_REFINEMENT,
            structured_output_model=QueryRefinementResponse,
            structured_output_version='v2'
        )
        
        schema = SchemaComposer.from_components(config)
        
        # Create an instance to test field values
        instance = schema()
        
        # Check that no field values are PydanticUndefined
        for field_name in schema.__fields__.keys():
            value = getattr(instance, field_name)
            assert value is not ..., f"Field {field_name} has PydanticUndefined value: {value}"
            print(f"Field {field_name}: {value} (type: {type(value)})")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 