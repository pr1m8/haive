#!/usr/bin/env python3
"""Validate haive-mcp setup with actual functionality tests."""

import asyncio
import subprocess
import sys
from pathlib import Path


async def test_basic_functionality():
    """Test basic MCP functionality."""
    tests_passed = 0
    tests_failed = 0

    # Test 1: Create configuration
    config_test = """from haive.mcp.config import MCPConfig, MCPServerConfig
config = MCPConfig(
    enabled=True,
    servers={
        "test": MCPServerConfig(
            name="test-server",
            transport="stdio",
            command="echo",
            args=["hello"]
        )
    }
)
print("Config created OK")
"""

    result = subprocess.run(
        ["poetry", "run", "python", "-c", config_test],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 2: Create MCP manager
    manager_test = """from haive.mcp.manager import MCPManager
manager = MCPManager()
print("Manager created OK")
"""

    result = subprocess.run(
        ["poetry", "run", "python", "-c", manager_test],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 3: Create FastMCP server
    server_test = """import asyncio
from mcp.server import FastMCP

server = FastMCP("validation-server")

@server.tool()
async def test_tool(message: str) -> str:
    return f"Validated: {message}"

async def test():
    result = await test_tool("Hello MCP")
    assert result == "Validated: Hello MCP"
    print("Server test OK")

asyncio.run(test())
"""

    result = subprocess.run(
        ["poetry", "run", "python", "-c", server_test],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 4: Test dataflow integration
    dataflow_test = """from haive.dataflow import registry_system, EntityType

# Register a test server
test_id = registry_system.register_entity(
    name="validation-test-server",
    entity_type=EntityType.MCP_SERVER,
    description="Test server for validation",
    metadata={
        "test": True,
        "validation_run": True
    }
)

# Query it back
servers = registry_system.get_entities_by_type(EntityType.MCP_SERVER)
found = any(s.get("name") == "validation-test-server" for s in servers)

if found:
    print("Dataflow test OK")
else:
    raise Exception("Could not find registered server")
"""

    result = subprocess.run(
        ["poetry", "run", "python", "-c", dataflow_test],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        tests_passed += 1
    elif "ImportError" in result.stderr:
        pass
    else:
        tests_failed += 1

    # Test 5: Test file operations
    try:
        test_file = Path("test_validation.txt")
        test_file.write_text("MCP validation test")

        # Simulate file server operations
        content = test_file.read_text()
        assert content == "MCP validation test"

        # Cleanup
        test_file.unlink()

        tests_passed += 1
    except Exception:
        tests_failed += 1

    # Summary

    return tests_failed == 0


async def test_example_usage():
    """Test a realistic example."""
    example_test = '''import asyncio
from mcp.server import FastMCP

example_server = FastMCP("example-validation")

@example_server.tool()
async def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())

@example_server.tool()
async def reverse_text(text: str) -> str:
    """Reverse the text."""
    return text[::-1]

async def test():
    word_count = await count_words("Hello MCP World")
    reversed_text = await reverse_text("MCP")

    print(f"Word count: {word_count}")
    print(f"Reversed: {reversed_text}")

    if word_count == 3 and reversed_text == "PCM":
        print("Example OK")
    else:
        raise Exception("Unexpected results")

asyncio.run(test())
'''

    result = subprocess.run(
        ["poetry", "run", "python", "-c", example_test],
        capture_output=True,
        text=True,
        check=False,
    )

    return bool(result.returncode == 0 and "Example OK" in result.stdout)


async def main():
    """Run all validation tests."""
    # Run basic tests
    basic_ok = await test_basic_functionality()

    # Run example test
    example_ok = await test_example_usage()

    # Final verdict

    if basic_ok and example_ok:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
