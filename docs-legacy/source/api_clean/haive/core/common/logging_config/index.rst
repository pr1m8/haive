
haive.core.common.logging_config
================================

.. py:module:: haive.core.common.logging_config

.. autoapi-nested-parse::

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
       logger.setLevel(logging.DEBUG)
       ```






Functions
---------

   get_game_logger
.. autofunction:: get_game_logger

Classes
-------

* :py:class:`LogLevel` - Logging level enumeration.* :py:class:`LogFormat` - Log output format enumeration.* :py:class:`GameLogger` - Enhanced logger for game agents with rich formatting and game-specific methods.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/logging_config/LogLevel   /api_clean/haive/core/common/logging_config/LogFormat   /api_clean/haive/core/common/logging_config/GameLogger

Package Contents
----------------

