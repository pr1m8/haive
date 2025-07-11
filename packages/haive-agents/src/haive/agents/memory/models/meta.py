import re
import threading
from abc import ABC, ABCMeta
from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Type, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class MemoryValidationMeta(ABCMeta):
    """Advanced metaclass for memory models with automatic validation registration
    and cross-model consistency checking.
    """

    _memory_registry: dict[str, type] = {}
    _validation_rules: dict[str, list[callable]] = defaultdict(list)
    _lock = threading.Lock()

    def __new__(mcs, name: str, bases: tuple, namespace: dict, **kwargs):
        # Extract validation metadata
        memory_type = namespace.get("__memory_type__")
        validation_level = namespace.get("__validation_level__", "standard")

        # Enforce memory type classification
        if memory_type and memory_type not in [
            "semantic",
            "episodic",
            "procedural",
            "working",
        ]:
            raise TypeError(
                f"Invalid memory type: {memory_type}. Must be one of: semantic, episodic, procedural, working"
            )

        # Register global validation rules
        if hasattr(mcs, "_apply_global_validations"):
            namespace = mcs._apply_global_validations(namespace, validation_level)

        cls = super().__new__(mcs, name, bases, namespace)

        # Register the class in our memory registry
        with mcs._lock:
            if memory_type:
                mcs._memory_registry[name] = cls
                cls._memory_siblings = [
                    registered_cls
                    for registered_cls in mcs._memory_registry.values()
                    if getattr(registered_cls, "__memory_type__", None) == memory_type
                ]

        return cls

    @classmethod
    def _apply_global_validations(cls, namespace: dict, level: str) -> dict:
        """Apply validation rules based on validation level."""
        if level == "enterprise":
            # Add enterprise-grade validation methods
            namespace["_validate_security_constraints"] = cls._security_validator
            namespace["_validate_data_integrity"] = cls._integrity_validator

        return namespace

    @staticmethod
    def _security_validator(obj) -> bool:
        """Enterprise security validation."""
        # Implement security rules like PII detection, etc.
        return True

    @staticmethod
    def _integrity_validator(obj) -> bool:
        """Data integrity validation."""
        # Implement cross-field integrity checks
        return True
