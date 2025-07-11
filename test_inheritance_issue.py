#!/usr/bin/env python3
"""Test if create_model properly inherits fields from base classes."""

import logging
from typing import Optional

from pydantic import BaseModel, Field, create_model

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Test 1: Simple inheritance
class BaseSchema(BaseModel):
    required_field: str = Field(..., description="Required field from base")
    optional_field: str | None = Field(default=None, description="Optional field")


# Create a schema using create_model with BaseSchema as base
DerivedSchema = create_model(
    "DerivedSchema",
    __base__=BaseSchema,
    extra_field=(str, Field(default="extra", description="Extra field")),
)

logger.info("=== Test 1: Simple Inheritance ===")
logger.info(f"BaseSchema fields: {list(BaseSchema.model_fields.keys())}")
logger.info(f"DerivedSchema fields: {list(DerivedSchema.model_fields.keys())}")
logger.info(
    f"Is DerivedSchema subclass of BaseSchema: {issubclass(DerivedSchema, BaseSchema)}"
)

# Try to create instance
try:
    instance = DerivedSchema(required_field="test")
    logger.info(
        f"✓ Created instance: required_field={instance.required_field}, extra_field={instance.extra_field}"
    )
except Exception as e:
    logger.exception(f"✗ Failed to create instance: {e}")

# Test 2: With LLMState
try:
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.schema.prebuilt.llm_state import LLMState

    logger.info("\n=== Test 2: LLMState Inheritance ===")
    logger.info(f"LLMState fields: {list(LLMState.model_fields.keys())}")

    # Check if engine is required in LLMState
    engine_field = LLMState.model_fields.get("engine")
    if engine_field:
        logger.info(f"Engine field required: {engine_field.is_required()}")
        logger.info(f"Engine field type: {engine_field.annotation}")

    # Create a derived schema
    TestState = create_model(
        "TestState",
        __base__=LLMState,
        query=(str, Field(default="", description="Query field")),
    )

    logger.info(f"\nTestState fields: {list(TestState.model_fields.keys())}")
    logger.info(f"Is TestState subclass of LLMState: {issubclass(TestState, LLMState)}")

    # Check if engine field exists in TestState
    if "engine" in TestState.model_fields:
        engine_field = TestState.model_fields["engine"]
        logger.info(
            f"TestState has engine field, required: {engine_field.is_required()}"
        )
    else:
        logger.error("TestState is missing engine field!")

    # Try to create instance
    try:
        # This should fail because engine is required
        instance1 = TestState(query="test")
        logger.error("✗ Created instance without engine - this shouldn't happen!")
    except Exception as e:
        logger.info(f"✓ Correctly failed without engine: {e}")

    # Try with engine
    try:
        engine = AugLLMConfig()
        instance2 = TestState(engine=engine, query="test")
        logger.info("✓ Created instance with engine"e")
    except Exception as e:
        logger.exception(f"✗ Failed with engine: {e}")

except ImportError as e:
    logger.exception(f"Could not import LLMState: {e}")

# Test 3: Field skipping issue
logger.info("\n=== Test 3: Field Skipping Simulation ===")


class BaseWithEngine(BaseModel):
    engine: str = Field(..., description="Required engine field")
    other_field: str = Field(default="default", description="Other field")


# Simulate what SchemaComposer does - it skips base class fields
base_class_fields = set(BaseWithEngine.model_fields.keys())
logger.info(f"Base class fields to skip: {base_class_fields}")

# Create schema without passing base fields (like SchemaComposer does)
field_defs = {"new_field": (str, Field(default="new", description="New field"))}
# Note: NOT including 'engine' or 'other_field' in field_defs

SimulatedSchema = create_model("SimulatedSchema", __base__=BaseWithEngine, **field_defs)

logger.info(f"\nSimulatedSchema fields: {list(SimulatedSchema.model_fields.keys())}")

# Check if engine is still there
if "engine" in SimulatedSchema.model_fields:
    logger.info("✓ Engine field properly inherited even when not in field_defs")
else:
    logger.error("✗ Engine field missing when not in field_defs!")

# Try to create instance
try:
    instance = SimulatedSchema(engine="test_engine")
    logger.info("✓ Created instance with inherited engine field"d")
except Exception as e:
    logger.exception(f"✗ Failed to create instance: {e}")
