"""Rich logging mixin for enhanced console output.

This module provides a mixin for adding rich console logging capabilities to
Pydantic models. It leverages the Rich library to enable colorized, formatted
console output with features like syntax highlighting and rich traceback display.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins import RichLoggerMixin

    class MyProcessor(RichLoggerMixin, BaseModel):
        name: str

        def process(self, data):
            self._info(f"Processing data with {self.name}")
            try:
                # Processing logic
                result = self._process_data(data)
                self._debug(f"Processed result: {result}")
                return result
            except Exception as e:
                self._error(f"Failed to process data: {e}")
                raise

    # Create with debug enabled
    processor = MyProcessor(name="TestProcessor", debug=True)
    processor.process({"test": "data"})
    ```
"""

import logging

from pydantic import BaseModel, PrivateAttr
from rich.console import Console
from rich.logging import RichHandler


class RichLoggerMixin(BaseModel):
    """Mixin that provides rich console logging capabilities.

    This mixin adds a configurable logger with rich formatting to any
    Pydantic model. It creates a logger named after the class, configures
    it with Rich's handler for pretty console output, and provides convenience
    methods for different log levels with appropriate styling.

    Attributes:
        debug: Boolean flag to control debug output visibility.
    """

    # Debug flag to control debug output
    debug: bool = False

    # Private logger instance
    _logger: logging.Logger | None = PrivateAttr(default=None)
    _logger_setup: bool = PrivateAttr(default=False)

    @property
    def logger(self) -> logging.Logger:
        """Get or create logger with rich handler.

        This property lazily initializes a logger with a Rich handler,
        creating it only when first accessed. The logger is named
        using the module and class name for proper log categorization.

        Returns:
            Configured logging.Logger instance with Rich formatting.
        """
        if self._logger is None or not self._logger_setup:
            # Create logger with module.class name
            logger_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
            self._logger = logging.getLogger(logger_name)

            # Only add handler if not already present
            if not self._logger.handlers:
                # Create rich handler with clean format
                handler = RichHandler(
                    console=Console(stderr=True),
                    show_time=True,
                    show_path=False,  # Keep it clean
                    rich_tracebacks=True,
                )
                handler.setFormatter(logging.Formatter("%(message)s"))
                self._logger.addHandler(handler)
                self._logger.setLevel(logging.INFO)

            self._logger_setup = True

        return self._logger

    def _debug(self, msg: str, *args, **kwargs) -> None:
        """Debug logging - only shows if debug=True.

        Args:
            msg: The message to log.
            *args: Additional positional arguments for the logger.
            **kwargs: Additional keyword arguments for the logger.
        """
        if self.debug:
            self.logger.debug(
                f"[dim cyan]{self.__class__.__name__}:[/] {msg}", *args, **kwargs
            )

    def _info(self, msg: str, *args, **kwargs) -> None:
        """Info logging with standard formatting.

        Args:
            msg: The message to log.
            *args: Additional positional arguments for the logger.
            **kwargs: Additional keyword arguments for the logger.
        """
        self.logger.info(msg, *args, **kwargs)

    def _warning(self, msg: str, *args, **kwargs) -> None:
        """Warning logging with yellow highlighting.

        Args:
            msg: The message to log.
            *args: Additional positional arguments for the logger.
            **kwargs: Additional keyword arguments for the logger.
        """
        self.logger.warning(f"[yellow]{msg}[/]", *args, **kwargs)

    def _error(self, msg: str, *args, **kwargs) -> None:
        """Error logging with red highlighting.

        Args:
            msg: The message to log.
            *args: Additional positional arguments for the logger.
            **kwargs: Additional keyword arguments for the logger.
        """
        self.logger.error(f"[red]{msg}[/]", *args, **kwargs)
