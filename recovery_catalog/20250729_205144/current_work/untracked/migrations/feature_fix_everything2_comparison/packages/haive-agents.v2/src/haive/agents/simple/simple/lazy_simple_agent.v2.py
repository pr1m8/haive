"""Lazy_Simple_Agent core module.

This module provides lazy simple agent functionality for the Haive framework.

Classes:
    LazyAugLLMConfig: LazyAugLLMConfig implementation.
    LazyAgent: LazyAgent implementation.
    Agent: Agent implementation.

Functions:
    cached_import: Cached Import functionality.
"""

# LazySimpleAgent - Ultra-fast import with intelligent lazy loading
"""
Ultra-optimized SimpleAgent implementation that achieves sub-3 second import times
through comprehensive lazy loading and intelligent caching.

This approach uses proxy objects and deferred imports to avoid loading any heavy
dependencies (LangChain, NumPy, Pandas, etc.) until they're actually needed.

Usage:
    # Ultra-fast import - no heavy dependencies
    from haive.agents.simple.lazy_simple_agent import LazySimpleAgent as SimpleAgentV3

    # Heavy loading happens only when actually used
    agent = SimpleAgentV3(name="test")  # Still fast - creates proxy
    result = await agent.arun("Hello")  # Heavy loading happens here
"""

import importlib
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# Global cache for imported modules and classes
_MODULE_CACHE: dict[str, Any] = {}
_CLASS_CACHE: dict[str, Any] = {}


def cached_import(module_path: str, class_name: str | None = None):
    """Cached import with intelligent loading."""
    cache_key = f"{module_path}{'.' + class_name if class_name else ''}"

    if cache_key in _CLASS_CACHE:
        return _CLASS_CACHE[cache_key]

    if module_path in _MODULE_CACHE:
        module = _MODULE_CACHE[module_path]
    else:
        module = importlib.import_module(module_path)
        _MODULE_CACHE[module_path] = module

    if class_name:
        cls = getattr(module, class_name)
        _CLASS_CACHE[cache_key] = cls
        return cls
    return module


class LazyAugLLMConfig:
    """Lazy proxy for AugLLMConfig that defers all heavy imports."""

    def __init__(self, **kwargs):
        # Store initialization args without importing anything heavy
        self._init_kwargs = kwargs
        self._real_instance = None
        self._is_initialized = False

        # Basic defaults that don't require imports
        self.name = kwargs.get("name", "lazy_aug_llm")
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens")
        self.model = kwargs.get("model", "gpt-4")

    def _ensure_initialized(self):
        """Initialize the real AugLLMConfig only when needed."""
        if not self._is_initialized:
            logger.debug("Lazy loading AugLLMConfig for first use")

            # Import heavy dependencies only now
            AugLLMConfig = cached_import(
                "haive.core.engine.aug_llm.config", "AugLLMConfig"
            )

            # Create real instance with stored kwargs
            self._real_instance = AugLLMConfig(**self._init_kwargs)
            self._is_initialized = True

            logger.debug("AugLLMConfig initialized successfully")

    def __getattr__(self, name: str):
        """Proxy all attribute access to real instance."""
        if name.startswith("_"):
            # Don't proxy private attributes
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

        self._ensure_initialized()
        return getattr(self._real_instance, name)

    def __setattr__(self, name: str, value: Any):
        """Proxy attribute setting."""
        if name.startswith("_") or name in [
            "name",
            "temperature",
            "max_tokens",
            "model",
        ]:
            # Set on proxy for basic attributes
            super().__setattr__(name, value)
            # Also store in init kwargs for later
            if not name.startswith("_"):
                self._init_kwargs[name] = value
        else:
            # Proxy to real instance
            self._ensure_initialized()
            setattr(self._real_instance, name, value)

    def __call__(self, *args, **kwargs):
        """Make callable like real AugLLMConfig."""
        self._ensure_initialized()
        return self._real_instance(*args, **kwargs)


class LazyAgent:
    """Lazy proxy for Agent base class."""

    def __init__(self, **kwargs):
        self._init_kwargs = kwargs
        self._real_instance = None
        self._is_initialized = False

        # Basic attributes that don't require heavy imports
        self.name = kwargs.get("name", "lazy_agent")

    def _ensure_initialized(self):
        """Initialize real Agent only when needed."""
        if not self._is_initialized:
            logger.debug("Lazy loading Agent base class")

            # Import Agent class
            Agent = cached_import("haive.agents.base.enhanced_agent", "Agent")

            # Initialize with proper engine proxy
            engine = self._init_kwargs.get("engine")
            if isinstance(engine, LazyAugLLMConfig):
                # Keep engine as lazy proxy
                pass

            self._real_instance = Agent(**self._init_kwargs)
            self._is_initialized = True

            logger.debug("Agent initialized successfully")

    def __getattr__(self, name: str):
        """Proxy all method calls to real instance."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

        self._ensure_initialized()
        return getattr(self._real_instance, name)


class LazySimpleAgent:
    """Ultra-optimized SimpleAgent with comprehensive lazy loading."""

    def __init__(
        self,
        name: str = "LazySimpleAgent",
        engine: Any | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        model_name: str | None = None,
        debug: bool = True,
        **kwargs,
    ):
        """Initialize with minimal overhead - no heavy imports."""
        # Store all initialization parameters
        self._init_time = datetime.now()
        self._name = name
        self._debug = debug
        self._real_instance = None
        self._is_initialized = False

        # Create lazy engine if none provided
        if engine is None:
            init_kwargs = {}
            if temperature is not None:
                init_kwargs["temperature"] = temperature
            if max_tokens is not None:
                init_kwargs["max_tokens"] = max_tokens
            if model_name is not None:
                init_kwargs["model"] = model_name

            engine = LazyAugLLMConfig(**init_kwargs)

        # Store all init kwargs for real instance creation
        self._init_kwargs = {
            "name": name,
            "engine": engine,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "model_name": model_name,
            "debug": debug,
            **kwargs,
        }

        if debug:
            logger.debug(f"LazySimpleAgent '{name}' created with minimal overhead")

    def _ensure_initialized(self):
        """Initialize the real SimpleAgentV3 only when actually needed."""
        if not self._is_initialized:
            init_start = datetime.now()

            if self._debug:
                logger.info(
                    f"Initializing real SimpleAgentV3 for '{self._name}' (lazy loading triggered)"
                )

            # Now import the real SimpleAgentV3
            SimpleAgentV3 = cached_import(
                "haive.agents.simple.agent_v3", "SimpleAgentV3"
            )

            # Create real instance
            self._real_instance = SimpleAgentV3(**self._init_kwargs)
            self._is_initialized = True

            init_time = (datetime.now() - init_start).total_seconds()

            if self._debug:
                total_time = (datetime.now() - self._init_time).total_seconds()
                logger.info(
                    f"Real SimpleAgentV3 initialized in {init_time:.2f}s (total: {total_time:.2f}s)"
                )

    # Essential properties that can be handled without initialization
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        if self._is_initialized:
            self._real_instance.name = value

    # Proxy all other attribute access
    def __getattr__(self, name: str):
        """Lazy proxy all attribute access to real instance."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

        self._ensure_initialized()
        return getattr(self._real_instance, name)

    def __setattr__(self, name: str, value: Any):
        """Proxy attribute setting."""
        if name.startswith("_") or name in ["name"]:
            super().__setattr__(name, value)
        else:
            self._ensure_initialized()
            setattr(self._real_instance, name, value)

    # Essential methods that trigger initialization
    async def arun(self, *args, **kwargs):
        """Async run - triggers full initialization."""
        self._ensure_initialized()
        return await self._real_instance.arun(*args, **kwargs)

    def run(self, *args, **kwargs):
        """Sync run - triggers full initialization."""
        self._ensure_initialized()
        return self._real_instance.run(*args, **kwargs)

    # Class methods for tool creation
    @classmethod
    def as_tool(cls, *args, **kwargs):
        """Create tool - triggers full initialization."""
        if cls._debug if hasattr(cls, "_debug") else True:
            logger.debug("as_tool called - triggering full SimpleAgentV3 import")

        SimpleAgentV3 = cached_import("haive.agents.simple.agent_v3", "SimpleAgentV3")
        return SimpleAgentV3.as_tool(*args, **kwargs)

    @classmethod
    def as_structured_tool(cls, *args, **kwargs):
        """Create structured tool - triggers full initialization."""
        if cls._debug if hasattr(cls, "_debug") else True:
            logger.debug(
                "as_structured_tool called - triggering full SimpleAgentV3 import"
            )

        SimpleAgentV3 = cached_import("haive.agents.simple.agent_v3", "SimpleAgentV3")
        return SimpleAgentV3.as_structured_tool(*args, **kwargs)

    def __repr__(self) -> str:
        status = "initialized" if self._is_initialized else "lazy"
        return f"LazySimpleAgent(name='{self._name}', status='{status}')"


# Export as SimpleAgentV3 for drop-in compatibility
SimpleAgentV3 = LazySimpleAgent
