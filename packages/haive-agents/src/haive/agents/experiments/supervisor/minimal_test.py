"""Minimal test to verify imports and basic setup."""

print("Testing imports...")

try:
    from haive.agents.simple.agent import SimpleAgent

    print("✓ SimpleAgent imported")
except Exception as e:
    print(f"✗ SimpleAgent import failed: {e}")

try:
    from haive.agents.react.agent import ReactAgent

    print("✓ ReactAgent imported")
except Exception as e:
    print(f"✗ ReactAgent import failed: {e}")

try:
    from haive.core.engine.aug_llm import AugLLMConfig

    print("✓ AugLLMConfig imported")
except Exception as e:
    print(f"✗ AugLLMConfig import failed: {e}")

try:
    from langchain_core.tools import tool

    print("✓ tool decorator imported")
except Exception as e:
    print(f"✗ tool import failed: {e}")

try:
    from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel

    print("✓ DynamicChoiceModel imported")
except Exception as e:
    print(f"✗ DynamicChoiceModel import failed: {e}")

print("\nAll imports successful! The pattern should work.")
