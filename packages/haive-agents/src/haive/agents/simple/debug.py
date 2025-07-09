# Create a debug script to test input/output schema derivation

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import PromptTemplate

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create a simple prompt template
prompt = PromptTemplate.from_template(
    """
    Context information: {context}
    
    User query: {input}
    
    Please provide a helpful response based on the context and query.
    """
)

# Print the prompt's input variables
print(f"Prompt input variables: {prompt.input_variables}")

# Create AugLLMConfig
aug_llm = AugLLMConfig(
    name="debug_llm",
    llm_config=AzureLLMConfig(model="gpt-4o"),
    prompt_template=prompt,
    system_prompt="You are a helpful assistant.",
)

# Get variables from _get_input_variables
input_vars = aug_llm._get_input_variables()
print(f"AugLLMConfig input variables: {input_vars}")

# Derive the input schema
input_schema = aug_llm.derive_input_schema()
print(f"Input schema fields: {list(input_schema.model_fields.keys())}")

# Try to process different types of input
test_inputs = [
    "Just a string",
    {"input": "What is X?", "context": "X is Y."},
    {"messages": [], "input": "What is X?", "context": "X is Y."},
]

# Process each input and print results
for idx, test_input in enumerate(test_inputs):
    print(f"\nTest {idx+1}: {type(test_input)}")
    result = aug_llm._process_input(test_input)
    print(f"Processed result: {result}")

    # Check if all required variables are present
    missing = [var for var in input_vars if var not in result]
    if missing:
        print(f"WARNING: Missing variables: {missing}")
    else:
        print("All required variables present")
