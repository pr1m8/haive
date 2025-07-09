# src/haive/core/logging/decorators.py

"""
Decorators for automatic logging with Rich formatting.
"""

import functools
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar, Union

from haive.core.logging.utils import get_logger

T = TypeVar("T")


def log_calls(
    logger: Optional[Union[str, logging.Logger]] = None,
    level: int = logging.INFO,
    include_args: bool = False,
    include_result: bool = False,
    component: Optional[str] = None,
):
    """
    Decorator to log function/method calls.

    Args:
        logger: Logger instance or name
        level: Logging level
        include_args: Whether to include function arguments in log
        include_result: Whether to include return value in log
        component: Component name for logger inference
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Get logger
        if isinstance(logger, str):
            log = get_logger(logger, component)
        elif logger is not None:
            log = logger
        else:
            # Infer logger from function
            module_name = func.__module__
            func_name = func.__name__
            log = get_logger(f"{module_name}.{func_name}", component)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Prepare log message
            call_info = f"Calling {func.__name__}"

            # Add arguments if requested
            if include_args and (args or kwargs):
                arg_parts = []
                if args:
                    arg_parts.append(f"args={args}")
                if kwargs:
                    arg_parts.append(f"kwargs={kwargs}")
                call_info += f" with {', '.join(arg_parts)}"

            # Log the call
            log.log(level, call_info)

            try:
                result = func(*args, **kwargs)

                # Log result if requested
                if include_result:
                    log.log(level, f"{func.__name__} returned: {result}")
                else:
                    log.log(level, f"{func.__name__} completed successfully")

                return result

            except Exception as e:
                log.error(f"{func.__name__} failed: {type(e).__name__}: {e}")
                raise

        return wrapper

    return decorator


def log_performance(
    logger: Optional[Union[str, logging.Logger]] = None,
    threshold_seconds: float = 1.0,
    component: Optional[str] = None,
    include_args: bool = False,
):
    """
    Decorator to log function performance with Rich formatting.

    Args:
        logger: Logger instance or name
        threshold_seconds: Only log if execution time exceeds this threshold
        component: Component name for logger inference
        include_args: Whether to include function arguments in performance log
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Get logger
        if isinstance(logger, str):
            log = get_logger(logger, component)
        elif logger is not None:
            log = logger
        else:
            module_name = func.__module__
            func_name = func.__name__
            log = get_logger(f"{module_name}.{func_name}", component)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # Only log if above threshold
                if duration >= threshold_seconds:
                    # Create performance log record
                    message = f"{func.__name__} performance: {duration:.3f}s"

                    record = log.makeRecord(
                        log.name, logging.INFO, __file__, 0, message, (), None
                    )
                    record.haive_type = "performance"
                    record.operation = func.__name__
                    record.duration = duration
                    record.component = component or "performance"

                    context = {
                        "function": func.__name__,
                        "module": func.__module__,
                        "duration_seconds": duration,
                        "threshold_seconds": threshold_seconds,
                    }

                    if include_args and (args or kwargs):
                        context["args"] = args
                        context["kwargs"] = kwargs

                    record.context = context
                    log.handle(record)

                return result

            except Exception as e:
                duration = time.time() - start_time
                log.error(
                    f"{func.__name__} failed after {duration:.3f}s: {type(e).__name__}: {e}"
                )
                raise

        return wrapper

    return decorator


def log_errors(
    logger: Optional[Union[str, logging.Logger]] = None,
    reraise: bool = True,
    component: Optional[str] = None,
    include_context: bool = True,
):
    """
    Decorator to log errors with Rich formatting and context.

    Args:
        logger: Logger instance or name
        reraise: Whether to reraise the exception after logging
        component: Component name for logger inference
        include_context: Whether to include function context in error log
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Get logger
        if isinstance(logger, str):
            log = get_logger(logger, component)
        elif logger is not None:
            log = logger
        else:
            module_name = func.__module__
            func_name = func.__name__
            log = get_logger(f"{module_name}.{func_name}", component)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Prepare context
                context = {
                    "function": func.__name__,
                    "module": func.__module__,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                }

                if include_context and (args or kwargs):
                    context["function_args"] = args
                    context["function_kwargs"] = kwargs

                # Create error log record
                message = f"Error in {func.__name__}: {type(e).__name__}: {e}"

                record = log.makeRecord(
                    log.name, logging.ERROR, __file__, 0, message, (), exc_info=e
                )
                record.haive_type = "error_context"
                record.error_context = context
                log.handle(record)

                if reraise:
                    raise

                return None

        return wrapper

    return decorator


def log_method_calls(
    level: int = logging.DEBUG, include_args: bool = False, include_result: bool = False
):
    """
    Class decorator to log all method calls.

    Args:
        level: Logging level
        include_args: Whether to include method arguments
        include_result: Whether to include return values
    """

    def class_decorator(cls):
        # Get all methods
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith("_"):
                # Apply log_calls decorator
                decorated_method = log_calls(
                    level=level,
                    include_args=include_args,
                    include_result=include_result,
                    component=cls.__name__.lower(),
                )(attr)
                setattr(cls, attr_name, decorated_method)

        return cls

    return class_decorator


class TimedOperation:
    """
    Context manager for timing operations with Rich logging.
    """

    def __init__(
        self,
        operation_name: str,
        logger: Optional[logging.Logger] = None,
        component: str = "System",
        context: Optional[Dict[str, Any]] = None,
    ):
        self.operation_name = operation_name
        self.component = component
        self.context = context or {}
        self.logger = logger or get_logger(f"{component}.performance")
        self.start_time: Optional[float] = None

    def __enter__(self) -> "TimedOperation":
        self.start_time = time.time()

        # Log operation start
        record = self.logger.makeRecord(
            self.logger.name,
            logging.INFO,
            __file__,
            0,
            f"🚀 Starting {self.operation_name}",
            (),
            None,
        )
        record.context = {
            "operation": self.operation_name,
            "component": self.component,
            "start_time": self.start_time,
            **self.context,
        }
        self.logger.handle(record)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return

        duration = time.time() - self.start_time

        if exc_type is None:
            # Success
            message = f"✅ {self.operation_name} completed in {duration:.3f}s"
            level = logging.INFO
        else:
            # Error
            message = f"❌ {self.operation_name} failed after {duration:.3f}s"
            level = logging.ERROR

        # Log performance
        record = self.logger.makeRecord(
            self.logger.name,
            level,
            __file__,
            0,
            message,
            (),
            exc_info=(exc_type, exc_val, exc_tb) if exc_type else None,
        )
        record.haive_type = "performance"
        record.operation = self.operation_name
        record.duration = duration
        record.component = self.component
        record.context = {
            "operation": self.operation_name,
            "duration_seconds": duration,
            "success": exc_type is None,
            **self.context,
        }

        self.logger.handle(record)
