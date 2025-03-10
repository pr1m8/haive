# tests/test_schema_manager.py

import sys
import os
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the SchemaManager
from src.haive.core.graph.StateSchemaManager import StateSchemaManager as SchemaManager

# Import dependencies for testing
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import add_messages
from typing import Annotated, Sequence

# Test models
class SimpleModel(BaseModel):
    name: str
    age: int = 0
    is_active: bool = True

class NestedModel(BaseModel):
    info: SimpleModel
    tags: List[str] = []

# Test with AugLLMConfig (mocked version to avoid dependencies)
class MockAugLLMConfig:
    def __init__(self, name="mock_llm", prompt_template=None, tools=None, 
                 structured_output_model=None, output_parser=None):
        self.name = name
        self.prompt_template = prompt_template
        self.tools = tools
        self.structured_output_model = structured_output_model
        self.output_parser = output_parser

class MockPromptTemplate:
    def __init__(self, input_variables=None, messages=None):
        self.input_variables = input_variables or []
        self.messages = messages or []

class PlaceholderMessage:
    def __init__(self, variable_name):
        self.variable_name = variable_name
class MockBaseModel(BaseModel):
    name: str
    age: int = 0
    is_active: bool = True

def test_create_from_dict():
    """Test creating a schema from a dictionary."""
    print("\n=== Testing creation from dict ===")
    
    # Simple dictionary
    data = {
        "name": "Test User",
        "age": 30,
        "scores": [95, 87, 92]
    }
    
    schema = SchemaManager(data, name="UserSchema")
    print("Schema from dict:")
    schema.pretty_print()
    
    # Get the model
    Model = schema.get_model()
    
    # Create an instance
    instance = Model(name="John Doe", age=25, scores=[80, 85, 90])
    print("\nInstance values:")
    print(f"Name: {instance.name}")
    print(f"Age: {instance.age}")
    print(f"Scores: {instance.scores}")
    
    # Test field inspection
    assert schema.has_field("name")
    assert schema.get_field_type("age") == int
    assert schema.get_field_default("scores") == [95, 87, 92]
    
    return schema

def test_create_from_model():
    """Test creating a schema from a Pydantic model."""
    print("\n=== Testing creation from Pydantic model ===")
    
    schema = SchemaManager(SimpleModel, name="SimpleSchema")
    print("Schema from model:")
    schema.pretty_print()
    
    # Get the model
    Model = schema.get_model()
    
    # Create an instance
    instance = Model(name="Alice", age=35, is_active=False)
    print("\nInstance values:")
    print(f"Name: {instance.name}")
    print(f"Age: {instance.age}")
    print(f"Is Active: {instance.is_active}")
    
    return schema

def test_create_from_aug_llm():
    """Test creating a schema from an AugLLMConfig."""
    print("\n=== Testing creation from AugLLMConfig ===")
    
    # Create a mock prompt template with input variables
    prompt = MockPromptTemplate(
        input_variables=["messages", "context", "query"],
        messages=[PlaceholderMessage(variable_name="messages")]
    )
    model = MockBaseModel
    # Create a mock AugLLMConfig
    llm_config = MockAugLLMConfig(
        name="test_llm",
        prompt_template=prompt,
        tools=[{"name": "calculator"}],
        output_parser=JsonOutputParser(pydantic_object=model),
        structured_output_model=model,
    )
    
    # Create schema from AugLLMConfig
    schema = SchemaManager.from_aug_llm(llm_config, name="test_schema")
    print("Schema from AugLLMConfig:")
    print(schema)
    schema.pretty_print()
    
    return schema

