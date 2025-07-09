# Codebase Documentation Template for Haive

## Overview
This template provides the structure for documenting the Haive codebase. Use this as a guide for creating comprehensive documentation for modules, classes, and functions.

## Module Documentation Structure

### 1. Module Overview File (`{module_name}/README.md`)

```markdown
# Module: haive.{module_name}

## Purpose
Brief description of what this module does and why it exists.

## Architecture
- Key components and their relationships
- Design patterns used
- Integration points with other modules

## Quick Start
```python
# Minimal working example
from haive.{module_name} import MainClass
instance = MainClass()
result = instance.main_method()
```

## API Summary
| Class/Function | Description | Status |
|----------------|-------------|---------|
| `MainClass` | Primary interface for X | Stable |
| `HelperClass` | Utilities for Y | Beta |
| `experimental_feature()` | New feature Z | Experimental |

## Dependencies
- Internal: `haive.core`, `haive.utils`
- External: `pydantic>=2.0`, `aiohttp>=3.8`

## Configuration
```yaml
module_name:
  setting_a: default_value
  setting_b: 123
```

## Testing
```bash
pytest tests/test_{module_name}/
```

## Known Issues
- Issue #123: Description
- Issue #456: Description

## Changelog
- v0.2.0: Added feature X
- v0.1.0: Initial release
```

### 2. Python File Documentation Template

```python
"""Module: haive.{package}.{module}

This module provides {brief description of functionality}.

Architecture Notes:
    - Design decision 1: Why we chose approach X over Y
    - Design decision 2: Trade-offs considered
    - Integration: How this connects to other modules

Example:
    Basic usage::
    
        from haive.{package}.{module} import {MainClass}
        
        instance = {MainClass}(config={"key": "value"})
        result = await instance.process(data)
        
    Advanced usage::
    
        # With custom configuration
        config = {
            "option1": True,
            "option2": "custom_value"
        }
        instance = {MainClass}(**config)
        
        # Process with callbacks
        async def callback(event):
            print(f"Event: {event}")
            
        result = await instance.process(
            data,
            callback=callback
        )

Module Attributes:
    DEFAULT_CONFIG (Dict[str, Any]): Default configuration values
    SUPPORTED_MODELS (List[str]): List of supported model types
    VERSION (str): Current module version

Environment Variables:
    HAIVE_{MODULE}_TIMEOUT: Operation timeout in seconds (default: 30)
    HAIVE_{MODULE}_DEBUG: Enable debug logging (default: false)

See Also:
    - :doc:`/guides/{module}_guide`: User guide
    - :mod:`haive.{related_module}`: Related functionality
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union, Protocol, TypeVar
from typing_extensions import Annotated, Self

from pydantic import BaseModel, Field, validator, root_validator

# Module-level logger
logger = logging.getLogger(__name__)

# Type definitions
T = TypeVar('T')
ConfigType = Dict[str, Any]


class {ClassName}Protocol(Protocol):
    """{ClassName} protocol definition.
    
    This protocol defines the interface that all {ClassName}
    implementations must follow.
    """
    
    async def process(self, data: Any) -> Any:
        """Process data according to implementation."""
        ...


class {ClassName}Config(BaseModel):
    """Configuration for {ClassName}.
    
    This configuration model validates and provides defaults for all
    {ClassName} settings. It uses Pydantic for validation and 
    serialization.
    
    Attributes:
        setting_a (str): Description of setting A. Used for X.
        setting_b (int): Description of setting B. Must be positive.
        advanced_option (Optional[Dict]): Advanced configuration options.
            Only needed for custom implementations.
    
    Example:
        >>> config = {ClassName}Config(
        ...     setting_a="value",
        ...     setting_b=42
        ... )
        >>> print(config.json(indent=2))
        {
          "setting_a": "value",
          "setting_b": 42,
          "advanced_option": null
        }
    """
    
    setting_a: str = Field(
        default="default_value",
        description="Main configuration setting",
        regex="^[a-zA-Z0-9_]+$"
    )
    
    setting_b: int = Field(
        default=100,
        description="Numeric setting with constraints",
        ge=1,
        le=1000
    )
    
    advanced_option: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Advanced options for power users"
    )
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"
        
    @validator('setting_b')
    def validate_setting_b(cls, v: int) -> int:
        """Ensure setting_b is even for internal reasons."""
        if v % 2 != 0:
            raise ValueError("setting_b must be even")
        return v
        
    @root_validator
    def validate_config(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-field validation."""
        if values.get('advanced_option') and values.get('setting_a') == 'default_value':
            raise ValueError(
                "Cannot use advanced_option with default setting_a"
            )
        return values


class {ClassName}:
    """Main class implementation.
    
    This class provides the primary interface for {functionality}.
    It handles {what it handles} and integrates with {what it integrates with}.
    
    Design Notes:
        - Thread-safe: All methods are thread-safe
        - Async-first: All I/O operations are async
        - Lazy loading: Resources loaded on first use
        
    Attributes:
        config ({ClassName}Config): Configuration instance
        is_initialized (bool): Whether the instance is initialized
        _internal_state (Dict): Internal state (private)
    
    Example:
        Simple usage::
        
            async with {ClassName}() as instance:
                result = await instance.process("input")
                
        Manual lifecycle::
        
            instance = {ClassName}(config)
            await instance.initialize()
            try:
                result = await instance.process("input")
            finally:
                await instance.cleanup()
                
    Raises:
        ConfigurationError: If configuration is invalid
        InitializationError: If initialization fails
    """
    
    def __init__(
        self,
        config: Optional[Union[{ClassName}Config, Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize {ClassName}.
        
        Args:
            config: Configuration object or dict. If None, uses defaults.
                Can be either a {ClassName}Config instance or a dict that
                will be converted to {ClassName}Config.
            **kwargs: Additional keyword arguments that override config values.
                These are applied after config initialization.
                
        Raises:
            ValidationError: If config validation fails
            TypeError: If config is neither dict nor {ClassName}Config
            
        Example:
            >>> # Using config object
            >>> config = {ClassName}Config(setting_a="custom")
            >>> instance = {ClassName}(config)
            
            >>> # Using dict
            >>> instance = {ClassName}({"setting_a": "custom"})
            
            >>> # Using kwargs
            >>> instance = {ClassName}(setting_a="custom", setting_b=200)
        """
        # Implementation with detailed comments
        
    async def initialize(self) -> None:
        """Initialize resources and connections.
        
        This method must be called before using the instance. It sets up
        all necessary resources, connections, and internal state.
        
        The initialization process:
        1. Validates configuration
        2. Establishes connections
        3. Loads required resources
        4. Sets up internal state
        
        Raises:
            InitializationError: If any step fails
            TimeoutError: If initialization takes too long
            
        Note:
            This is automatically called when using async context manager.
            
        Example:
            >>> instance = {ClassName}()
            >>> await instance.initialize()
            >>> # Now ready to use
        """
        
    async def process(
        self,
        data: Any,
        *,
        options: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable[[str], Awaitable[None]]] = None,
        timeout: Optional[float] = None
    ) -> ProcessResult:
        """Process input data.
        
        This is the main processing method. It takes input data,
        applies transformations according to configuration, and
        returns the result.
        
        Args:
            data: Input data to process. Can be:
                - str: Text input
                - Dict: Structured data
                - List: Batch of items
                - Custom type: Must implement __str__
                
            options: Processing options that override defaults:
                - "strict": bool, whether to enforce strict validation
                - "format": str, output format ("json", "text", "binary")
                - "chunk_size": int, processing chunk size
                
            callback: Optional async callback for progress updates.
                Called with status messages during processing.
                
            timeout: Override default timeout in seconds.
                If None, uses config.timeout.
                
        Returns:
            ProcessResult: Object containing:
                - data: Processed output
                - metadata: Processing metadata
                - errors: List of non-fatal errors
                - stats: Performance statistics
                
        Raises:
            ProcessingError: If processing fails
            ValidationError: If input validation fails  
            TimeoutError: If processing exceeds timeout
            
        Example:
            Basic usage::
            
                result = await instance.process("Hello world")
                print(result.data)
                
            With options::
            
                result = await instance.process(
                    {"key": "value"},
                    options={"format": "json", "strict": True}
                )
                
            With callback::
            
                async def progress(msg: str):
                    print(f"Progress: {msg}")
                    
                result = await instance.process(
                    large_data,
                    callback=progress,
                    timeout=60.0
                )
                
        Warning:
            Large inputs may require increased timeout values.
            
        See Also:
            - :meth:`process_batch`: For batch processing
            - :meth:`process_stream`: For streaming processing
        """
        
    @property  
    def statistics(self) -> Statistics:
        """Get processing statistics.
        
        Returns current statistics including:
        - Total items processed
        - Success/failure rates  
        - Average processing time
        - Resource usage
        
        Returns:
            Statistics: Current statistics object
            
        Example:
            >>> stats = instance.statistics
            >>> print(f"Processed: {stats.total_processed}")
            >>> print(f"Success rate: {stats.success_rate:.2%}")
        """
        
    @classmethod
    def from_config_file(cls, path: str) -> Self:
        """Create instance from configuration file.
        
        Supports YAML, JSON, and TOML formats.
        
        Args:
            path: Path to configuration file
            
        Returns:
            New configured instance
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ParseError: If config file is malformed
            
        Example:
            >>> instance = {ClassName}.from_config_file("config.yaml")
        """


# Specialized exceptions
class {ClassName}Error(Exception):
    """Base exception for {ClassName} errors.
    
    All {ClassName}-specific exceptions inherit from this.
    
    Attributes:
        message: Error message
        code: Error code for programmatic handling
        details: Additional error details
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Initialize exception.
        
        Args:
            message: Human-readable error message
            code: Machine-readable error code (e.g., "CONFIG_INVALID")
            details: Additional context about the error
        """
        super().__init__(message)
        self.message = message
        self.code = code or "UNKNOWN_ERROR"
        self.details = details or {}


# Module-level functions
async def create_{classname}(
    config: Optional[ConfigType] = None,
    **kwargs: Any
) -> {ClassName}:
    """Factory function to create and initialize {ClassName}.
    
    This is the recommended way to create instances as it handles
    initialization automatically.
    
    Args:
        config: Configuration dict or None for defaults
        **kwargs: Override configuration values
        
    Returns:
        Initialized {ClassName} instance
        
    Example:
        >>> instance = await create_{classname}(
        ...     setting_a="custom",
        ...     setting_b=200
        ... )
    """
    # Create instance
    if config:
        instance = {ClassName}(config, **kwargs)
    else:
        instance = {ClassName}(**kwargs)
        
    # Initialize
    await instance.initialize()
    
    return instance


# Constants and module-level configuration
DEFAULT_TIMEOUT = 30.0
"""Default timeout for operations in seconds."""

SUPPORTED_FORMATS = ["json", "yaml", "text", "binary"]
"""List of supported output formats."""

# Version information
__version__ = "0.1.0"
__all__ = [
    "{ClassName}",
    "{ClassName}Config", 
    "{ClassName}Error",
    "create_{classname}",
]
```

### 3. Test Documentation Template

```python
"""Tests for haive.{module_name}.

Test Categories:
    - Unit tests: Test individual components
    - Integration tests: Test component interactions
    - Performance tests: Test performance characteristics
    - Edge cases: Test boundary conditions

Test Data:
    Test fixtures are located in tests/fixtures/{module_name}/
    Generated test data uses factories in tests/factories/{module_name}.py
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import Any, Dict

from haive.{module_name} import {ClassName}, {ClassName}Config


class Test{ClassName}:
    """Test suite for {ClassName}.
    
    Tests are organized by functionality:
    - Initialization and configuration
    - Core processing methods
    - Error handling
    - Edge cases
    - Performance characteristics
    """
    
    @pytest.fixture
    def default_config(self) -> {ClassName}Config:
        """Provide default test configuration.
        
        Returns:
            Configuration suitable for most tests
        """
        return {ClassName}Config(
            setting_a="test_value",
            setting_b=100
        )
        
    @pytest.fixture
    async def initialized_instance(
        self,
        default_config: {ClassName}Config
    ) -> {ClassName}:
        """Provide initialized instance for testing.
        
        Args:
            default_config: Configuration fixture
            
        Returns:
            Ready-to-use instance
        """
        instance = {ClassName}(default_config)
        await instance.initialize()
        yield instance
        await instance.cleanup()
        
    class TestInitialization:
        """Test initialization and configuration."""
        
        def test_init_with_defaults(self):
            """Test initialization with default values.
            
            Verifies:
            - Instance created successfully
            - Default values applied
            - State is correct
            """
            instance = {ClassName}()
            assert instance.config.setting_a == "default_value"
            assert instance.config.setting_b == 100
            assert not instance.is_initialized
            
        def test_init_with_config_object(self, default_config):
            """Test initialization with config object.
            
            Verifies:
            - Config object accepted
            - Values preserved
            - No mutations to input
            """
            original_dict = default_config.dict()
            instance = {ClassName}(default_config)
            
            assert instance.config.setting_a == "test_value"
            assert default_config.dict() == original_dict
            
        @pytest.mark.parametrize("invalid_config", [
            {"setting_b": -1},  # Negative value
            {"setting_b": 1001},  # Exceeds maximum
            {"setting_a": ""},  # Empty string
            {"extra_field": "value"},  # Unknown field
        ])
        def test_init_with_invalid_config(self, invalid_config):
            """Test initialization with invalid configurations.
            
            Verifies proper validation and error messages.
            """
            with pytest.raises(ValidationError) as exc_info:
                {ClassName}(invalid_config)
                
            assert "validation error" in str(exc_info.value).lower()
            
    class TestProcessing:
        """Test core processing functionality."""
        
        @pytest.mark.asyncio
        async def test_process_simple_input(self, initialized_instance):
            """Test processing with simple string input.
            
            Verifies:
            - Basic processing works
            - Result structure is correct
            - Metadata is populated
            """
            result = await initialized_instance.process("test input")
            
            assert result.data is not None
            assert result.metadata["input_type"] == "str"
            assert result.errors == []
            assert result.stats.duration > 0
            
        @pytest.mark.asyncio
        @pytest.mark.parametrize("data,expected_type", [
            ("string", "str"),
            ({"key": "value"}, "dict"),
            ([1, 2, 3], "list"),
            (123, "int"),
        ])
        async def test_process_different_types(
            self,
            initialized_instance,
            data: Any,
            expected_type: str
        ):
            """Test processing with different input types.
            
            Verifies type handling and polymorphic behavior.
            """
            result = await initialized_instance.process(data)
            assert result.metadata["input_type"] == expected_type
            
    class TestErrorHandling:
        """Test error handling and edge cases."""
        
        @pytest.mark.asyncio
        async def test_process_timeout(self, initialized_instance):
            """Test timeout handling.
            
            Verifies:
            - Timeout is respected
            - Proper error is raised
            - State is cleaned up
            """
            with patch.object(
                initialized_instance,
                '_do_process',
                new=AsyncMock(side_effect=asyncio.sleep(10))
            ):
                with pytest.raises(TimeoutError):
                    await initialized_instance.process(
                        "data",
                        timeout=0.1
                    )
                    
        @pytest.mark.asyncio
        async def test_process_with_callback_error(self, initialized_instance):
            """Test handling of callback errors.
            
            Verifies that callback errors don't break processing.
            """
            async def failing_callback(msg: str):
                raise Exception("Callback failed")
                
            # Should complete despite callback error
            result = await initialized_instance.process(
                "data",
                callback=failing_callback
            )
            assert result.data is not None
            
    class TestPerformance:
        """Test performance characteristics."""
        
        @pytest.mark.asyncio
        @pytest.mark.performance
        async def test_process_large_input_performance(
            self,
            initialized_instance,
            benchmark
        ):
            """Benchmark processing of large inputs.
            
            Verifies:
            - Performance scales linearly
            - Memory usage is bounded
            - No performance regressions
            """
            large_data = "x" * 1_000_000  # 1MB of data
            
            result = await benchmark(
                initialized_instance.process,
                large_data
            )
            
            assert result.stats.duration < 1.0  # Should complete in < 1s
            
    class TestIntegration:
        """Integration tests with other components."""
        
        @pytest.mark.asyncio
        @pytest.mark.integration
        async def test_with_real_engine(self):
            """Test with real engine integration.
            
            Note: Requires API keys to be set.
            """
            instance = {ClassName}(
                config={
                    "engine": "real_engine",
                    "api_key": os.getenv("TEST_API_KEY")
                }
            )
            await instance.initialize()
            
            result = await instance.process("real data")
            assert result.data is not None
```

### 4. Issues and Troubleshooting Documentation

```markdown
# Troubleshooting: haive.{module_name}

## Common Issues

### Import Errors

#### Issue: `ModuleNotFoundError: No module named 'haive.{module_name}'`

**Cause**: Module not installed or dependencies missing

**Solutions**:
1. Install with correct extras:
   ```bash
   pip install haive[{module_name}]
   ```

2. Check Python path:
   ```python
   import sys
   print(sys.path)
   ```

3. Verify installation:
   ```bash
   pip show haive
   pip list | grep haive
   ```

#### Issue: `AttributeError: module 'haive.{module_name}' has no attribute '{ClassName}'`

**Cause**: Class not imported correctly or version mismatch

**Solutions**:
1. Check import statement:
   ```python
   # Correct
   from haive.{module_name} import {ClassName}
   
   # Incorrect
   import haive.{module_name}.{ClassName}
   ```

2. Verify version compatibility:
   ```python
   import haive
   print(haive.__version__)
   ```

### Configuration Errors

#### Issue: `ValidationError` when creating instance

**Common Causes and Solutions**:

1. **Invalid type**:
   ```python
   # Wrong
   instance = {ClassName}(setting_b="100")  # Should be int
   
   # Correct
   instance = {ClassName}(setting_b=100)
   ```

2. **Missing required fields**:
   ```python
   # Check required fields
   print({ClassName}Config.schema()["required"])
   ```

3. **Value out of range**:
   ```python
   # Check constraints
   print({ClassName}Config.schema()["properties"]["setting_b"])
   ```

### Runtime Errors

#### Issue: `TimeoutError` during processing

**Solutions**:
1. Increase timeout:
   ```python
   result = await instance.process(data, timeout=60.0)
   ```

2. Process in smaller chunks:
   ```python
   for chunk in chunks(data, size=100):
       result = await instance.process(chunk)
   ```

3. Use streaming mode:
   ```python
   async for partial in instance.process_stream(data):
       handle_partial(partial)
   ```

### Performance Issues

#### Issue: Slow processing

**Diagnostic Steps**:
1. Enable profiling:
   ```python
   instance = {ClassName}(debug=True, profile=True)
   result = await instance.process(data)
   print(result.stats.profile)
   ```

2. Check resource usage:
   ```python
   import psutil
   process = psutil.Process()
   print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
   print(f"CPU: {process.cpu_percent()}%")
   ```

3. Use batching:
   ```python
   results = await instance.process_batch(
       items,
       batch_size=50,
       max_concurrency=5
   )
   ```

## Debugging

### Enable Debug Logging

```python
import logging

# Set module-specific logging
logging.getLogger("haive.{module_name}").setLevel(logging.DEBUG)

# Or enable all haive logging
logging.getLogger("haive").setLevel(logging.DEBUG)

# With detailed formatter
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logging.getLogger("haive").addHandler(handler)
```

### Debug Mode

```python
# Enable debug mode for detailed errors
instance = {ClassName}(debug=True)

# Or via environment variable
os.environ["HAIVE_DEBUG"] = "true"
```

### Introspection

```python
# Check configuration
print(instance.config.json(indent=2))

# Check state
print(instance._internal_state)

# Check statistics
print(instance.statistics.dict())

# Validate configuration
try:
    {ClassName}Config(**your_config)
except ValidationError as e:
    print(e.json(indent=2))
```

## Error Messages Reference

| Error Code | Message | Cause | Solution |
|------------|---------|-------|----------|
| `CONFIG_INVALID` | "Invalid configuration: {details}" | Validation failed | Check config against schema |
| `INIT_FAILED` | "Initialization failed: {reason}" | Resource unavailable | Check connections/permissions |
| `PROCESS_TIMEOUT` | "Processing exceeded timeout" | Long operation | Increase timeout or optimize |
| `INVALID_INPUT` | "Input validation failed" | Bad input format | Validate input before processing |

## Getting Help

1. **Check logs** - Most issues are logged with context
2. **Read stack trace** - Error location often hints at cause  
3. **Search issues** - GitHub issues may have solutions
4. **Ask community** - Discord/Slack for quick help
5. **File bug report** - Include minimal reproduction

### Bug Report Template

```markdown
**Environment**:
- Haive version: X.Y.Z
- Python version: 3.x
- OS: Linux/Mac/Windows

**Code to reproduce**:
```python
# Minimal code that shows the issue
```

**Expected behavior**:
What should happen

**Actual behavior**:
What actually happens

**Logs**:
```
Relevant log output
```
```

## Documentation Checklist

When documenting a module, ensure you have:

- [ ] Module README.md with overview and quick start
- [ ] Docstrings for all public classes and functions
- [ ] Type hints for all parameters and returns  
- [ ] Examples in docstrings showing common usage
- [ ] Error documentation with causes and solutions
- [ ] Test documentation explaining test structure
- [ ] Integration guide for connecting with other modules
- [ ] Performance considerations and optimization tips
- [ ] Troubleshooting section with common issues
- [ ] API reference with all public interfaces
- [ ] Configuration schema documentation
- [ ] Environment variables documentation
- [ ] Changelog with version history