#!/usr/bin/env python3
"""Find where LangChain validator gets triggered."""

import traceback

from pydantic import BaseModel


class SimpleModel(BaseModel):
    value: int = 1

    def __call__(self, x: int) -> int:
        return x * self.value


# Monkey patch the problematic function to get the call stack
def debug_raise_deprecation(cls, values):
    print("🚨 LangChain raise_deprecation called!")
    print(f"  cls: {cls}")
    print(f"  values type: {type(values)}")
    print(f"  values: {values}")
    print("\nCall stack:")
    traceback.print_stack()

    # This will fail with our BaseModel, but we'll see the stack trace
    raise AttributeError(f"DEBUG: {type(values).__name__} has no .get() method")


# Patch the function before importing AugLLMConfig
import langchain_core.tools.base

original_func = None

# Find the class with raise_deprecation
for name in dir(langchain_core.tools.base):
    obj = getattr(langchain_core.tools.base, name)
    if hasattr(obj, "__dict__") and "raise_deprecation" in obj.__dict__:
        print(f"Found raise_deprecation in {name}")
        original_func = getattr(obj, "raise_deprecation")
        setattr(obj, "raise_deprecation", classmethod(debug_raise_deprecation))
        break

if not original_func:
    # Try to patch BaseTool directly
    if hasattr(langchain_core.tools.base.BaseTool, "raise_deprecation"):
        print("Patching BaseTool.raise_deprecation")
        original_func = langchain_core.tools.base.BaseTool.raise_deprecation
        langchain_core.tools.base.BaseTool.raise_deprecation = classmethod(
            debug_raise_deprecation
        )

print("=" * 60)
print("FINDING LANGCHAIN VALIDATOR")
print("=" * 60)

instance = SimpleModel(value=5)

try:
    from haive.core.engine.aug_llm.config import AugLLMConfig

    config = AugLLMConfig(tools=[instance])
    print("✅ Success!")
except Exception as e:
    print(f"❌ Expected failure: {e}")

print("\nDone!")
