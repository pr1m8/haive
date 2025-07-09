"""
Logging Configuration Module.

This module provides utilities for configuring and managing logging throughout the Haive
framework. It includes customizable log levels, formatters, and specialized logging
for games and agents with rich console output support.

The module is designed to create a consistent logging experience across different
components while allowing for flexibility in output formats and verbosity levels.

Typical usage example:
    ```python
    from haive.core.common.logging_config import get_game_logger, LogLevel

    # Create a logger with default settings
    logger = get_game_logger("my_game")

    # Log messages at different levels
    logger.info("Game starting")
    logger.debug("Detailed state information")

    # Log game-specific events
    logger.turn_start("Player 1", turn_number=1)
    logger.dice_roll("Player 1", die1=3, die2=4, total=7)
    logger.player_move("Player 1", from_pos=0, to_pos=7)

    # Change log level dynamically
    logger.set_level(LogLevel.DEBUG)
    ```
"""

import logging
import os
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

# Try to import rich for enhanced console output
try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


class LogLevel(str, Enum):
    """
    Logging level enumeration.

    This enum defines standard logging levels plus a SILENT level
    for suppressing most log output. Since it inherits from str,
    it can be used directly in string contexts.

    Attributes:
        DEBUG: Detailed information, typically of interest only when diagnosing problems
        INFO: Confirmation that things are working as expected
        WARNING: Indication that something unexpected happened, or may happen
        ERROR: Due to a more serious problem, the software has not been able to perform a function
        CRITICAL: A serious error, indicating that the program itself may be unable to continue running
        SILENT: No logging except critical errors
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SILENT = "SILENT"  # No logging except critical errors


class LogFormat(str, Enum):
    """
    Log output format enumeration.

    This enum defines available formatting options for log output.
    It inherits from str for easy use in string contexts.

    Attributes:
        SIMPLE: Basic text output with just the message
        DETAILED: Include timestamps, logger name, and level with the message
        JSON: JSON formatted logs for machine parsing
        RICH: Enhanced console output with colors and formatting (requires rich library)
    """

    SIMPLE = "simple"  # Basic text output
    DETAILED = "detailed"  # Include timestamps and module info
    JSON = "json"  # JSON formatted logs
    RICH = "rich"  # Rich console output (if available)


class GameLogger:
    """
    Enhanced logger for game agents with rich formatting and game-specific methods.

    This logger extends standard Python logging with game-specific logging methods
    and support for rich console output. It provides specialized methods for logging
    game events like turns, dice rolls, player moves, and property actions with
    appropriate formatting and icons.

    It also includes performance tracking capabilities for monitoring operation durations
    and configurable verbosity levels that can be changed at runtime.

    Attributes:
        name: Logger name (usually module or game name)
        level: Current logging level
        format: Output format being used
        enable_file_logging: Whether logging to file is enabled
        log_file: Path to the log file if file logging is enabled
        logger: The underlying Python logger instance
    """

    def __init__(
        self,
        name: str,
        level: LogLevel = LogLevel.INFO,
        format: LogFormat = LogFormat.RICH if RICH_AVAILABLE else LogFormat.SIMPLE,
        enable_file_logging: bool = False,
        log_file: Optional[str] = None,
    ):
        """
        Initialize the game logger with the specified configuration.

        Args:
            name: Logger name (usually module or game name)
            level: Logging level to control verbosity
            format: Output format for log messages
            enable_file_logging: Whether to log to a file in addition to console
            log_file: Path to log file (auto-generated with timestamp if not provided)
        """
        self.name = name
        self.level = level
        self.format = format
        self.enable_file_logging = enable_file_logging
        self.log_file = (
            log_file or f"game_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # Performance tracking
        self._operation_starts: Dict[str, float] = {}

        # Set up the logger
        self._setup_logger()

    def _setup_logger(self) -> None:
        """
        Set up the logging configuration based on the current settings.

        This method configures the underlying Python logger with appropriate
        handlers and formatters based on the format and level settings.
        It is called automatically during initialization but can also be
        called to reconfigure the logger after changing settings.
        """
        self.logger = logging.getLogger(self.name)

        # Clear existing handlers
        self.logger.handlers = []

        # Set level
        if self.level == LogLevel.SILENT:
            self.logger.setLevel(logging.CRITICAL + 1)
        else:
            self.logger.setLevel(getattr(logging, self.level.value))

        # Console handler
        if self.format == LogFormat.RICH and RICH_AVAILABLE:
            console_handler = RichHandler(
                console=console, show_time=False, show_path=False, markup=True
            )
        else:
            console_handler = logging.StreamHandler(sys.stdout)

        # Set formatter based on format type
        if self.format == LogFormat.SIMPLE:
            formatter = logging.Formatter("%(message)s")
        elif self.format == LogFormat.DETAILED:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        elif self.format == LogFormat.JSON:
            # JSON formatter would go here
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "name": "%(name)s", '
                '"level": "%(levelname)s", "message": "%(message)s"}',
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        else:
            formatter = logging.Formatter("%(message)s")

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if enabled
        if self.enable_file_logging:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            self.logger.addHandler(file_handler)

    def set_level(self, level: LogLevel) -> None:
        """
        Change the logging level at runtime.

        Args:
            level: New logging level to use
        """
        self.level = level
        if level == LogLevel.SILENT:
            self.logger.setLevel(logging.CRITICAL + 1)
        else:
            self.logger.setLevel(getattr(logging, level.value))

    # Game-specific logging methods

    def turn_start(self, player_name: str, turn_number: int, **kwargs) -> None:
        """
        Log the start of a player's turn.

        Args:
            player_name: Name of the player whose turn is starting
            turn_number: Current turn number
            **kwargs: Additional turn information to log
        """
        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            console.print(
                f"\n[bold cyan]🎲 Turn {turn_number}:[/bold cyan] [yellow]{player_name}[/yellow]"
            )
            if kwargs:
                for key, value in kwargs.items():
                    console.print(f"  {key}: {value}")
        else:
            self.logger.info(f"Turn {turn_number}: {player_name}'s turn")
            if kwargs:
                for key, value in kwargs.items():
                    self.logger.info(f"  {key}: {value}")

    def dice_roll(self, player_name: str, die1: int, die2: int, total: int) -> None:
        """
        Log a dice roll event.

        Args:
            player_name: Name of the player who rolled
            die1: Value of the first die
            die2: Value of the second die
            total: Sum of both dice
        """
        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            console.print(
                f"  🎲 [blue]{player_name}[/blue] rolled: {die1} + {die2} = [bold]{total}[/bold]"
            )
        else:
            self.logger.info(f"{player_name} rolled: {die1} + {die2} = {total}")

    def player_move(
        self, player_name: str, from_pos: int, to_pos: int, passed_go: bool = False
    ) -> None:
        """
        Log player movement on the game board.

        Args:
            player_name: Name of the player who moved
            from_pos: Starting position
            to_pos: Ending position
            passed_go: Whether the player passed GO during the move
        """
        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            move_text = (
                f"  🚶 [blue]{player_name}[/blue] moves from {from_pos} to {to_pos}"
            )
            if passed_go:
                move_text += " [bold green](Passed GO! +$200)[/bold green]"
            console.print(move_text)
        else:
            msg = f"{player_name} moves from {from_pos} to {to_pos}"
            if passed_go:
                msg += " (Passed GO! +$200)"
            self.logger.info(msg)

    def property_action(
        self,
        action: str,
        player_name: str,
        property_name: str,
        amount: Optional[int] = None,
        **kwargs,
    ) -> None:
        """
        Log property-related actions.

        Args:
            action: Type of action (e.g., "buy", "rent", "mortgage")
            player_name: Name of the player performing the action
            property_name: Name of the property involved
            amount: Amount of money involved (if applicable)
            **kwargs: Additional action details
        """
        icons = {
            "landed": "🎯",
            "buy": "✅",
            "pass": "🚫",
            "rent": "💸",
            "mortgage": "🏦",
            "unmortgage": "🏠",
            "build": "🏗️",
        }

        icon = icons.get(action, "📍")

        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            if action == "buy":
                console.print(
                    f"  {icon} [green]{player_name} purchased {property_name} for ${amount}[/green]"
                )
            elif action == "rent":
                recipient = kwargs.get("recipient", "unknown")
                console.print(
                    f"  {icon} [red]{player_name} paid ${amount} rent to {recipient}[/red]"
                )
            else:
                msg = f"  {icon} {player_name} {action} {property_name}"
                if amount:
                    msg += f" (${amount})"
                console.print(msg)
        else:
            msg = f"{player_name} {action} {property_name}"
            if amount:
                msg += f" (${amount})"
            self.logger.info(msg)

    def game_event(self, event_type: str, description: str, **kwargs) -> None:
        """
        Log a general game event.

        Args:
            event_type: Type of event
            description: Description of what happened
            **kwargs: Additional event details (logged at debug level)
        """
        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            console.print(f"  📌 [magenta]{event_type}:[/magenta] {description}")
            if kwargs and self.logger.level <= logging.DEBUG:
                for key, value in kwargs.items():
                    console.print(f"    • {key}: {value}")
        else:
            self.logger.info(f"{event_type}: {description}")
            if kwargs and self.logger.level <= logging.DEBUG:
                for key, value in kwargs.items():
                    self.logger.debug(f"  {key}: {value}")

    def decision(
        self, player_name: str, decision_type: str, choice: str, reasoning: str = ""
    ) -> None:
        """
        Log a player decision.

        Args:
            player_name: Name of the player making the decision
            decision_type: Type of decision being made
            choice: The decision that was made
            reasoning: Optional explanation for the decision (logged at debug level)
        """
        if RICH_AVAILABLE and self.format == LogFormat.RICH:
            console.print(
                f"  🤔 [yellow]{player_name}[/yellow] decides to [bold]{choice}[/bold]"
            )
            if reasoning and self.logger.level <= logging.DEBUG:
                console.print(f"     [dim]{reasoning}[/dim]")
        else:
            self.logger.info(f"{player_name} decides to {choice}")
            if reasoning and self.logger.level <= logging.DEBUG:
                self.logger.debug(f"  Reasoning: {reasoning}")

    def game_state_summary(self, state: Dict[str, Any]) -> None:
        """
        Display a summary of the current game state.

        This method produces a rich table or formatted log output
        showing the current state of all players.

        Args:
            state: Dictionary containing the game state with at least a "players" key
        """
        if (
            RICH_AVAILABLE
            and self.format == LogFormat.RICH
            and self.logger.level <= logging.DEBUG
        ):
            table = Table(title="Game State Summary")
            table.add_column("Player", style="cyan")
            table.add_column("Money", style="green")
            table.add_column("Properties", style="yellow")
            table.add_column("Status", style="magenta")

            players = state.get("players", [])
            for player in players:
                status = "Bankrupt" if player.get("bankrupt", False) else "Active"
                if player.get("in_jail", False):
                    status = "In Jail"

                table.add_row(
                    player.get("name", "Unknown"),
                    f"${player.get('money', 0)}",
                    str(len(player.get("properties", []))),
                    status,
                )

            console.print(table)
        elif self.logger.level <= logging.DEBUG:
            self.logger.debug("Game State Summary:")
            players = state.get("players", [])
            for player in players:
                self.logger.debug(
                    f"  {player.get('name')}: ${player.get('money')} | "
                    f"Properties: {len(player.get('properties', []))}"
                )

    def performance_start(self, operation: str) -> None:
        """
        Start timing an operation for performance tracking.

        Call this at the beginning of an operation you want to time.

        Args:
            operation: Name of the operation to time
        """
        import time

        self._operation_starts[operation] = time.time()

    def performance_end(self, operation: str) -> None:
        """
        End timing an operation and log the duration.

        Call this at the end of an operation you started timing with
        performance_start(). The duration is only logged at DEBUG level.

        Args:
            operation: Name of the operation to end timing
        """
        import time

        if operation in self._operation_starts:
            duration = time.time() - self._operation_starts[operation]
            del self._operation_starts[operation]

            if self.logger.level <= logging.DEBUG:
                if RICH_AVAILABLE and self.format == LogFormat.RICH:
                    console.print(f"  ⏱️  [dim]{operation} took {duration:.3f}s[/dim]")
                else:
                    self.logger.debug(f"{operation} took {duration:.3f}s")

    # Standard logging methods that delegate to the underlying logger
    def debug(self, msg: str, **kwargs) -> None:
        """
        Log a debug message.

        Args:
            msg: Message to log
            **kwargs: Additional logging parameters
        """
        self.logger.debug(msg, **kwargs)

    def info(self, msg: str, **kwargs) -> None:
        """
        Log an info message.

        Args:
            msg: Message to log
            **kwargs: Additional logging parameters
        """
        self.logger.info(msg, **kwargs)

    def warning(self, msg: str, **kwargs) -> None:
        """
        Log a warning message.

        Args:
            msg: Message to log
            **kwargs: Additional logging parameters
        """
        self.logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        """
        Log an error message.

        Args:
            msg: Message to log
            **kwargs: Additional logging parameters
        """
        self.logger.error(msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> None:
        """
        Log a critical message.

        Args:
            msg: Message to log
            **kwargs: Additional logging parameters
        """
        self.logger.critical(msg, **kwargs)


def get_game_logger(
    name: str, level: Optional[str] = None, format: Optional[str] = None
) -> GameLogger:
    """
    Get a configured game logger instance.

    This function creates a GameLogger with settings from environment variables
    or the provided parameters. Environment variables take precedence over
    the function parameters if both are provided.

    Environment variables:
        - GAME_LOG_LEVEL: Logging level (DEBUG, INFO, etc.)
        - GAME_LOG_FORMAT: Logging format (simple, detailed, json, rich)
        - GAME_LOG_TO_FILE: Whether to log to file ("true" or "false")

    Args:
        name: Logger name (usually module or game name)
        level: Override log level (environment variable takes precedence)
        format: Override format (environment variable takes precedence)

    Returns:
        Configured GameLogger instance ready for use
    """
    # Check environment variables for configuration
    env_level = level or os.getenv("GAME_LOG_LEVEL", "INFO")
    env_format = format or os.getenv(
        "GAME_LOG_FORMAT", "rich" if RICH_AVAILABLE else "simple"
    )
    enable_file = os.getenv("GAME_LOG_TO_FILE", "false").lower() == "true"

    # Convert to enums
    try:
        log_level = LogLevel[env_level.upper()]
    except KeyError:
        log_level = LogLevel.INFO

    try:
        log_format = (
            LogFormat[env_format.upper()]
            if env_format.upper() in LogFormat.__members__
            else LogFormat(env_format.lower())
        )
    except (KeyError, ValueError):
        log_format = LogFormat.RICH if RICH_AVAILABLE else LogFormat.SIMPLE

    return GameLogger(
        name=name, level=log_level, format=log_format, enable_file_logging=enable_file
    )
