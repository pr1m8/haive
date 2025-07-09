"""Simple MRO test without full haive imports."""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))


def test_provider_base_mro():
    """Test MRO without importing full haive stack."""
    from haive.core.models.llm.provider_types import LLMProvider
    from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin

    # Test rate limiting mixin can be created
    mixin = RateLimitingMixin()
    assert hasattr(mixin, "apply_rate_limiting")
    assert hasattr(mixin, "get_rate_limit_info")

    # Test provider enum
    assert LLMProvider.OPENAI.value == "openai"
    assert LLMProvider.ANTHROPIC.value == "anthropic"

    print("Basic imports work correctly")


def test_provider_imports():
    """Test provider module imports."""
    try:
        # Test base provider import
        from haive.core.models.llm.providers.base import (
            BaseLLMProvider,
            ProviderImportError,
        )

        print("✓ Base provider imports correctly")

        # Test provider __init__ imports
        from haive.core.models.llm.providers import get_provider, list_providers

        print("✓ Provider functions import correctly")

        # Test factory imports
        from haive.core.models.llm.factory import LLMFactory, create_llm

        print("✓ Factory imports correctly")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_create_simple_provider():
    """Test creating a simple provider without full dependencies."""
    from pydantic import Field

    from haive.core.models.llm.provider_types import LLMProvider
    from haive.core.models.llm.providers.base import BaseLLMProvider

    class SimpleTestProvider(BaseLLMProvider):
        provider: LLMProvider = Field(default=LLMProvider.OPENAI)

        def _get_chat_class(self):
            # Return a dummy class
            class DummyChat:
                def __init__(self, **kwargs):
                    self.kwargs = kwargs

            return DummyChat

        def _get_default_model(self):
            return "test-model"

        def _get_import_package(self):
            return "test-package"

        def _requires_api_key(self):
            return False

    # Test instantiation
    provider = SimpleTestProvider()
    assert provider.provider == LLMProvider.OPENAI
    assert provider.model == "test-model"

    # Test MRO
    mro = SimpleTestProvider.__mro__
    print(f"MRO chain length: {len(mro)}")
    print(f"MRO: {[cls.__name__ for cls in mro]}")

    # Verify no duplicate classes in MRO
    mro_names = [cls.__name__ for cls in mro]
    assert len(mro_names) == len(set(mro_names)), "Duplicate classes in MRO!"

    # Test instantiation
    llm = provider.instantiate()
    assert llm is not None

    print("✓ Provider creation works correctly")


if __name__ == "__main__":
    print("Testing MRO and imports...")
    test_provider_base_mro()
    test_provider_imports()
    test_create_simple_provider()
    print("\nAll tests passed!")
