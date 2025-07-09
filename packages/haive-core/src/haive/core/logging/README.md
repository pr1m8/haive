# Haive Logging System

A comprehensive logging management system for the haive framework with rich UI, interactive CLI, and advanced debugging features.

## Features

- 🎨 **Rich UI Integration** - Beautiful colored output with rich formatting
- 🖥️ **Interactive CLI** - Prompt-toolkit powered CLI with auto-completion
- 🐛 **Debug Toggle** - Quick debug mode switching
- 📊 **Real-time Monitoring** - Live log monitoring with statistics
- 🎯 **Module-specific Control** - Fine-grained control per module
- 🔇 **Smart Suppression** - Auto-suppress noisy third-party libraries
- 💾 **Persistent Configuration** - Save and load settings
- 🚀 **Auto-configuration** - Pre-configured for common scenarios
- 📍 **Source Tracking** - See exactly where logs and prints come from

## Installation

```bash
# Basic installation (included with haive-core)
pip install haive-core

# With optional UI dependencies
pip install haive-core[logging]

# Or install dependencies separately
pip install rich prompt-toolkit readchar
```

## Quick Start - See Where Everything Comes From! 🔍

### The Fastest Way

```python
# See EVERYTHING with source info (logs + prints)
from haive.core.logging.quick_setup import i_want_to_see_everything
i_want_to_see_everything()
```

### Recommended for Development

```python
# Perfect development setup - shows sources, hides library noise
from haive.core.logging.quick_setup import setup_development_logging
setup_development_logging()
```

### What You'll See

```
[14:32:15] INFO     haive.core.engine | execute() in executor.py:123
    Processing request 456

[PRINT from mymodule.do_work():45] Starting process...

[14:32:16] WARNING  myapp.service | validate() in service.py:67
    Invalid configuration detected
```

### Other Quick Options

```python
# Just see your code (hide all libraries)
from haive.core.logging.quick_setup import just_show_my_code
just_show_my_code()

# Track specific modules only
from haive.core.logging.quick_setup import track_specific_modules
track_specific_modules(['haive.core.engine', 'myapp'])

# Find where a specific message is coming from
from haive.core.logging.quick_setup import where_is_this_coming_from
where_is_this_coming_from('error message text')

# Quick debug toggle with source info
from haive.core.logging.quick_setup import debug_on, debug_off
debug_on()   # Enable debug + sources
debug_off()  # Back to normal
```

### Command Line Source Tracking

```bash
# Enable source tracking from command line
python -m haive.core.logging source

# Then run your script - all logs will show sources!
```

## Quick Start (Original)

### Debug Toggle

```bash
# Toggle debug mode on/off
python -m haive.core.logging.debug_toggle

# Enable debug
python -m haive.core.logging debug on

# Disable debug
python -m haive.core.logging debug off

# Debug specific modules
python -m haive.core.logging debug on haive.core.engine haive.agents
```

### Interactive CLI

```bash
# Launch interactive CLI with auto-completion
python -m haive.core.logging interactive

# Or use the shorter alias
python -m haive.core.logging i
```

Features:

- Tab auto-completion for commands and module names
- Command history (Up/Down arrows)
- Fuzzy matching
- Real-time log monitoring
- Module statistics

### Basic Commands

```bash
# Set global log level
python -m haive.core.logging level DEBUG

# Set module-specific level
python -m haive.core.logging module haive.core.engine DEBUG

# Apply preset
python -m haive.core.logging preset development

# Show status
python -m haive.core.logging status

# Generate test logs
python -m haive.core.logging test
```

### UI and Monitoring

```bash
# Launch rich UI
python -m haive.core.logging ui

# Launch advanced dashboard
python -m haive.core.logging dashboard

# Monitor logs in real-time
python -m haive.core.logging monitor

# Monitor with filter
python -m haive.core.logging monitor -f haive.core haive.agents
```

## Python API

### Basic Usage

```python
from haive.core.logging import logging_control, get_logger

# Get a logger
logger = get_logger("myapp.module")

# Set global level
logging_control.set_level("DEBUG")

# Quick presets
logging_control.debug_mode()  # Debug with third-party suppressed
logging_control.quiet_mode()  # Only warnings and above
logging_control.haive_only()  # Only show haive logs
```

### Module Control

```python
# Set module-specific level
logging_control.set_module_level("haive.core.engine", "DEBUG")

# Suppress modules
logging_control.suppress("langchain", "urllib3")

# Filter to specific modules
logging_control.only_show(["haive.core", "haive.agents"])

# Clear filters
logging_control.show_all()
```

### Auto-configuration

```python
from haive.core.logging.auto_config import (
    auto_configure_logging,
    configure_for_game_development,
    configure_for_agent_development,
    enable_source_tracking,
)

# Apply preset
auto_configure_logging(preset="development")

# Enable source tracking
enable_source_tracking()

# Specialized configurations
configure_for_game_development()
configure_for_agent_development()
```

### Environment Variables

```bash
# Enable verbose logging
export HAIVE_LOG_VERBOSE=1

# Enable quiet mode
export HAIVE_LOG_QUIET=1

# Show only haive logs
export HAIVE_ONLY=1

# Set specific level
export HAIVE_LOG_LEVEL=DEBUG

# Set modules to show
export HAIVE_LOG_MODULES=haive.core,haive.agents

# Set filter
export HAIVE_LOG_FILTER=haive
```

## Interactive CLI Commands

When in the interactive CLI (`python -m haive.core.logging interactive`):

### Basic Commands

- `help` - Show help message
- `status` - Show current configuration
- `quit`/`exit` - Exit the CLI

### Level Control

- `level <LEVEL>` - Set global log level
- `module <name> <LEVEL>` - Set module-specific level
- `debug [modules...]` - Enable debug mode

### Filtering

- `suppress <module>` - Suppress logs from module
- `unsuppress <module>` - Stop suppressing module
- `filter <modules...>` - Only show specified modules
- `clear-filter` - Show all modules

### Presets

- `preset <name>` - Apply preset (debug, normal, quiet, silent, haive-only)

### Monitoring

- `monitor` - Start real-time log monitoring
- `ui` - Launch interactive UI
- `dashboard` - Launch advanced dashboard
- `stats` - Show module statistics

### Advanced

- `trace <module>` - Enable detailed tracing
- `breakpoint <module> <message>` - Set log breakpoint
- `export <file>` - Export logs to file
- `test` - Generate test logs

## Presets

### Default

- Global level: INFO
- Suppresses noisy third-party libraries
- Shows all haive modules

### Development

- Global level: INFO
- haive modules at DEBUG
- Third-party libraries suppressed

### Minimal

- Global level: ERROR
- Maximum suppression

### Verbose

- Global level: DEBUG
- Minimal suppression

## Examples

### Game Development

```python
from haive.core.logging.auto_config import configure_for_game_development

# Automatically configured for game dev:
# - haive.games at DEBUG
# - Game engine internals suppressed
# - Agent decisions visible
configure_for_game_development()
```

### Agent Development

```python
from haive.core.logging.auto_config import configure_for_agent_development

# Automatically configured for agent dev:
# - haive.agents at DEBUG
# - Graph building noise suppressed
# - Agent decisions highlighted
configure_for_agent_development()
```

### Production

```python
# Quiet production logging
from haive.core.logging import logging_control

logging_control.quiet_mode()
# Or
logging_control.apply_preset("production")
```

## Tips

1. **Auto-import**: When you import `haive.core`, logging is automatically configured with sensible defaults

2. **Persistent Config**: Settings are saved to `~/.haive/logging_config.json`

3. **Thread-safe**: All operations are thread-safe for concurrent applications

4. **Performance**: Suppressed modules have minimal overhead

5. **Integration**: Works seamlessly with existing Python logging

## Troubleshooting

### Missing Dependencies

```bash
# Install all optional dependencies
pip install rich prompt-toolkit readchar

# Or install haive with logging extras
pip install haive-core[logging]
```

### Too Many Logs

```python
# Quick fixes:
logging_control.quiet_mode()  # Only warnings+
logging_control.haive_only()  # Only haive logs
logging_control.suppress("noisy.module")  # Suppress specific
```

### Can't See Debug Logs

```python
# Enable debug mode
logging_control.debug_mode()

# Or for specific module
logging_control.set_module_level("mymodule", "DEBUG")
```

### Reset Everything

```python
# Reset to defaults
from haive.core.logging.auto_config import auto_configure_logging
auto_configure_logging(preset="default")

# Or clear all settings
logging_control.show_all()
logging_control.set_level("INFO")
```
