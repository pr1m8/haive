# src/haive/core/logging/mixins.py

"""
Logging mixins that integrate with the Rich logging system.
"""

import functools
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar

from pydantic import BaseModel, PrivateAttr, computed_field, model_validator

from haive.core.logging.manager import get_logging_manager

T = TypeVar("T")


class LoggingMixin(BaseModel):
    """
    Basic logging mixin for Pydantic models.

    Provides structured logging with context information.
    """

    # Private attributes for logging
    _logger: Optional[logging.Logger] = PrivateAttr(default=None)
    _log_context: Optional[Dict[str, Any]] = PrivateAttr(default=None)

    @model_validator(mode="after")
    def initialize_logger(self) -> "LoggingMixin":
        """Initialize logger after model validation."""
        logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        component = self._infer_component_from_class()

        logging_manager = get_logging_manager()
        self._logger = logging_manager.get_logger(logger_name, component=component)

        return self

    @computed_field
    @property
    def logger_name(self) -> str:
        """Get the logger name for this object."""
        return f"{self.__class__.__module__}.{self.__class__.__name__}"

    @property
    def logger(self) -> logging.Logger:
        """Get the logger for this object."""
        if self._logger is None:
            self.initialize_logger()
        return self._logger

    def _infer_component_from_class(self) -> str:
        """Infer component type from class name and module."""
        class_name = self.__class__.__name__.lower()
        module_name = self.__class__.__module__.lower()

        if "agent" in class_name or "agent" in module_name:
            return "agent"
        elif "engine" in class_name or "engine" in module_name:
            return "engine"
        elif "graph" in class_name or "graph" in module_name:
            return "graph"
        elif "tool" in class_name or "tool" in module_name:
            return "tool"
        elif "game" in class_name or "game" in module_name:
            return "game"
        elif "core" in module_name:
            return "core"
        else:
            return "general"

    def _get_log_context(self) -> Dict[str, Any]:
        """Get context information for logging."""
        if self._log_context is not None:
            return self._log_context.copy()

        context = {
            "class": self.__class__.__name__,
        }

        # Add ID if available (from IdentifierMixin)
        if hasattr(self, "id"):
            context["object_id"] = getattr(self, "short_id", self.id)

        # Add name if available
        if hasattr(self, "name") and self.name:
            context["object_name"] = self.name

        # Add engine_type if available
        if hasattr(self, "engine_type"):
            context["engine_type"] = str(self.engine_type)

        # Cache context
        self._log_context = context
        return context

    def log_debug(self, message: str, **kwargs) -> None:
        """Log debug message with context."""
        context = self._get_log_context()
        context.update(kwargs)

        record = self.logger.makeRecord(
            self.logger.name, logging.DEBUG, __file__, 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)

    def log_info(self, message: str, **kwargs) -> None:
        """Log info message with context."""
        context = self._get_log_context()
        context.update(kwargs)

        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)

    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message with context."""
        context = self._get_log_context()
        context.update(kwargs)

        record = self.logger.makeRecord(
            self.logger.name, logging.WARNING, __file__, 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)

    def log_error(
        self, message: str, exception: Optional[Exception] = None, **kwargs
    ) -> None:
        """Log error message with context and optional exception."""
        context = self._get_log_context()
        context.update(kwargs)

        if exception:
            context["exception_type"] = type(exception).__name__
            context["exception_message"] = str(exception)

        record = self.logger.makeRecord(
            self.logger.name,
            logging.ERROR,
            __file__,
            0,
            message,
            (),
            exc_info=exception if exception else None,
        )
        record.context = context
        self.logger.handle(record)


class RichLoggerMixin(LoggingMixin):
    """
    Enhanced logging mixin with Rich-specific features.

    Provides beautiful console output with Rich formatting.
    """

    def log_banner(
        self, message: str, title: str = "Information", style: str = "bright_blue"
    ) -> None:
        """Log a banner-style message."""
        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, message, (), None
        )
        record.haive_type = "banner"
        record.banner_title = title
        record.banner_style = style
        record.context = self._get_log_context()
        self.logger.handle(record)

    def log_performance(
        self, operation: str, duration: float, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log performance information with Rich formatting."""
        message = f"{operation} completed in {duration:.3f}s"

        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, message, (), None
        )
        record.haive_type = "performance"
        record.operation = operation
        record.duration = duration
        record.component = self._infer_component_from_class()
        record.context = self._get_log_context()

        if details:
            record.context.update(details)

        self.logger.handle(record)

    def log_error_with_context(self, message: str, error: Exception, **context) -> None:
        """Log error with rich context information."""
        error_context = self._get_log_context()
        error_context.update(context)
        error_context.update(
            {"error_type": type(error).__name__, "error_message": str(error)}
        )

        record = self.logger.makeRecord(
            self.logger.name, logging.ERROR, __file__, 0, message, (), exc_info=error
        )
        record.haive_type = "error_context"
        record.error_context = error_context
        self.logger.handle(record)

    def log_success(self, message: str, **kwargs) -> None:
        """Log success message with special formatting."""
        context = self._get_log_context()
        context.update(kwargs)

        # Create Rich-formatted message
        success_message = f"✅ {message}"

        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, success_message, (), None
        )
        record.context = context
        self.logger.handle(record)

    def log_operation_start(self, operation: str, **kwargs) -> float:
        """Log the start of an operation and return start time."""
        start_time = time.time()

        context = self._get_log_context()
        context.update(kwargs)
        context["operation"] = operation
        context["start_time"] = start_time

        message = f"🚀 Starting {operation}"

        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)

        return start_time

    def log_operation_end(self, operation: str, start_time: float, **kwargs) -> float:
        """Log the end of an operation and return duration."""
        end_time = time.time()
        duration = end_time - start_time

        self.log_performance(operation, duration, kwargs)
        return duration

    def log_step(self, step: str, step_number: Optional[int] = None, **kwargs) -> None:
        """Log a step in a process."""
        context = self._get_log_context()
        context.update(kwargs)

        if step_number is not None:
            message = f"📋 Step {step_number}: {step}"
        else:
            message = f"📋 {step}"

        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, __file__, 0, message, (), None
        )
        record.context = context
        self.logger.handle(record)

    def log_component_init(self) -> None:
        """Log component initialization."""
        component_type = self._infer_component_from_class().title()
        component_name = getattr(self, "name", self.__class__.__name__)

        logging_manager = get_logging_manager()
        logging_manager.print_component_banner(component_name, component_type)

        self.log_banner(
            f"Initialized {component_name}",
            title=f"{component_type} Ready",
            style="bright_green",
        )


class PerformanceLoggerMixin(RichLoggerMixin):
    """
    Specialized mixin for performance logging with timing utilities.
    """

    # Private attribute for timing operations
    _operation_timers: Dict[str, float] = PrivateAttr(default_factory=dict)

    def start_timer(self, operation: str) -> None:
        """Start timing an operation."""
        self._operation_timers[operation] = time.time()
        self.log_operation_start(operation)

    def end_timer(self, operation: str, **details) -> float:
        """End timing an operation and log the duration."""
        if operation not in self._operation_timers:
            self.log_warning(f"Timer for operation '{operation}' was not started")
            return 0.0

        start_time = self._operation_timers.pop(operation)
        duration = time.time() - start_time

        self.log_performance(operation, duration, details)
        return duration

    def time_operation(self, operation_name: str):
        """Decorator to time a method or function."""

        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                self.start_timer(operation_name)
                try:
                    result = func(*args, **kwargs)
                    self.end_timer(operation_name, success=True)
                    return result
                except Exception as e:
                    self.end_timer(operation_name, success=False, error=str(e))
                    raise

            return wrapper

        return decorator
