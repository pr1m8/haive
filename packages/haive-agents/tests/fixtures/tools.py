from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers from each other"""
    return a - b
