# tests/test_llm_metadata.py

import json
import logging
import os
from typing import Any, Dict, List

import pytest
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.traceback import install
from rich.tree import Tree

# Install rich traceback handler for better error visualization
install()

# Import the LLM config classes
from haive.core.models.llm.base import (
    AnthropicLLMConfig,
    AzureLLMConfig,
    MistralLLMConfig,
    OpenAILLMConfig,
)

# Configure rich logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

logger = logging.getLogger("llm_metadata_test")
console = Console()

# Define model configurations to test
MODEL_CONFIGS = [
    # Azure GPT-4o
    {
        "class": AzureLLMConfig,
        "provider": "azure",
        "model": "gpt-4o",
        "name": "Azure GPT-4o",
        "env_var": "AZURE_OPENAI_API_KEY",
    },
    # Azure GPT-4 Turbo
    {
        "class": AzureLLMConfig,
        "provider": "azure",
        "model": "gpt-4-turbo",
        "name": "Azure GPT-4 Turbo",
        "env_var": "AZURE_OPENAI_API_KEY",
    },
    # Claude models
    {
        "class": AnthropicLLMConfig,
        "provider": "anthropic",
        "model": "claude-3-opus-20240229",
        "name": "Claude 3 Opus",
        "env_var": "ANTHROPIC_API_KEY",
    },
    {
        "class": AnthropicLLMConfig,
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "name": "Claude 3 Sonnet",
        "env_var": "ANTHROPIC_API_KEY",
    },
    {
        "class": AnthropicLLMConfig,
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "name": "Claude 3 Haiku",
        "env_var": "ANTHROPIC_API_KEY",
    },
    # Mistral models
    {
        "class": MistralLLMConfig,
        "provider": "mistralai",
        "model": "mistral-large-latest",
        "name": "Mistral Large",
        "env_var": "MISTRAL_API_KEY",
    },
    {
        "class": MistralLLMConfig,
        "provider": "mistralai",
        "model": "mistral-medium-latest",
        "name": "Mistral Medium",
        "env_var": "MISTRAL_API_KEY",
    },
    {
        "class": MistralLLMConfig,
        "provider": "mistralai",
        "model": "mistral-small-latest",
        "name": "Mistral Small",
        "env_var": "MISTRAL_API_KEY",
    },
    # Add OpenAI for comparison
    {
        "class": OpenAILLMConfig,
        "provider": "openai",
        "model": "gpt-4o",
        "name": "OpenAI GPT-4o",
        "env_var": "OPENAI_API_KEY",
    },
]


# Helper functions for testing
def check_env_var(env_var: str) -> bool:
    """Check if an environment variable is set and not empty."""
    return bool(os.getenv(env_var, "").strip())


def format_pricing(price: float) -> str:
    """Format price as a string."""
    if price == 0:
        return "$0"
    elif price < 0.0001:
        return f"${price:.8f}"
    elif price < 0.01:
        return f"${price:.6f}"
    else:
        return f"${price:.4f}"


def display_model_metadata_table(models_data: List[Dict[str, Any]]) -> None:
    """Display a rich table with model metadata."""
    table = Table(title="LLM Model Metadata Comparison")

    # Add columns
    table.add_column("Model", style="cyan")
    table.add_column("Provider", style="magenta")
    table.add_column("Context Window", justify="right", style="green")
    table.add_column("Max Input", justify="right", style="blue")
    table.add_column("Max Output", justify="right", style="blue")
    table.add_column("Input Cost", justify="right", style="yellow")
    table.add_column("Output Cost", justify="right", style="yellow")

    # Add rows
    for data in models_data:
        table.add_row(
            data["name"],
            data["provider"],
            str(data["context_window"]),
            str(data["max_input"]),
            str(data["max_output"]),
            format_pricing(data["input_cost"]),
            format_pricing(data["output_cost"]),
        )

    console.print(table)


def display_model_capabilities(models_data: List[Dict[str, Any]]) -> None:
    """Display a table of model capabilities."""
    capabilities = [
        "vision",
        "function_calling",
        "parallel_function_calling",
        "system_messages",
        "tool_choice",
        "response_schema",
        "web_search",
        "pdf_input",
        "audio_input",
        "audio_output",
        "prompt_caching",
        "native_streaming",
        "reasoning",
    ]

    table = Table(title="LLM Model Capabilities")

    # Add columns
    table.add_column("Model", style="cyan")
    for capability in capabilities:
        table.add_column(capability.replace("_", " ").title(), justify="center")

    # Add rows
    for data in models_data:
        row_data = [data["name"]]
        for capability in capabilities:
            supported = data["capabilities"].get(capability, False)
            row_data.append("✓" if supported else "✗")
        table.add_row(*row_data)

    console.print(table)


def display_metadata_tree(model_name: str, metadata: Dict[str, Any]) -> None:
    """Display the raw metadata as a tree."""
    tree = Tree(f"[bold cyan]{model_name} Raw Metadata[/bold cyan]")

    def _add_dict_to_tree(tree_node, data):
        if isinstance(data, dict):
            for key, value in sorted(data.items()):
                if isinstance(value, dict):
                    branch = tree_node.add(f"[yellow]{key}[/yellow]")
                    _add_dict_to_tree(branch, value)
                elif isinstance(value, list):
                    branch = tree_node.add(
                        f"[yellow]{key}[/yellow] (list, {len(value)} items)"
                    )
                    for i, item in enumerate(value):
                        if isinstance(item, (dict, list)):
                            sub_branch = branch.add(f"[blue]Item {i}[/blue]")
                            _add_dict_to_tree(sub_branch, item)
                        else:
                            branch.add(f"[blue]Item {i}:[/blue] {item}")
                else:
                    tree_node.add(f"[green]{key}[/green]: {value}")

    _add_dict_to_tree(tree, metadata)
    console.print(tree)


# Pytest fixtures
@pytest.fixture(scope="module")
def available_models():
    """Return a list of available models based on environment variables."""
    available = []

    for config in MODEL_CONFIGS:
        if check_env_var(config["env_var"]):
            available.append(config)
        else:
            logger.warning(f"Skipping {config['name']} - {config['env_var']} not set")

    return available


# Tests
@pytest.mark.parametrize(
    "model_config", MODEL_CONFIGS, ids=[m["name"] for m in MODEL_CONFIGS]
)
def test_model_metadata_access(model_config):
    """Test metadata access for each model."""
    env_var = model_config["env_var"]

    # Skip if API key not available
    if not check_env_var(env_var):
        pytest.skip(f"Skipping {model_config['name']} - {env_var} not set")

    # Create the config
    config_class = model_config["class"]
    model = model_config["model"]
    display_name = model_config["name"]  # Get the friendly name from model_config

    logger.info(f"Testing metadata access for {display_name} ({model})")

    # Create the config with progress spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Creating {display_name} config...", total=1)
        # Pass the name parameter when creating the config
        config = config_class(model=model, name=display_name, debug=True)
        progress.update(task, completed=1)

    # Get metadata
    raw_metadata = config._get_model_metadata()

    # Log and assert
    logger.info(f"Retrieved metadata for {model_config['name']}")

    # Display raw metadata tree for debugging
    display_metadata_tree(model_config["name"], raw_metadata)

    # Assert basic data is present
    console.print(Panel(f"[bold]Basic Metadata for {model_config['name']}[/bold]"))

    context_window = config.get_context_window()
    console.print(f"Context Window: [cyan]{context_window}[/cyan] tokens")
    assert context_window > 0, "Context window should be greater than 0"

    max_input = config.get_max_input_tokens()
    console.print(f"Max Input: [cyan]{max_input}[/cyan] tokens")
    assert max_input > 0, "Max input tokens should be greater than 0"

    max_output = config.get_max_output_tokens()
    console.print(f"Max Output: [cyan]{max_output}[/cyan] tokens")
    assert max_output > 0, "Max output tokens should be greater than 0"

    # Check pricing
    input_cost, output_cost = config.get_token_pricing()
    console.print(f"Input cost per token: [green]{format_pricing(input_cost)}[/green]")
    console.print(
        f"Output cost per token: [green]{format_pricing(output_cost)}[/green]"
    )

    # Check capabilities using property access
    console.print("\n[bold]Capabilities:[/bold]")
    capabilities = {
        "vision": config.supports_vision,
        "function_calling": config.supports_function_calling,
        "parallel_function_calling": config.supports_parallel_function_calling,
        "system_messages": config.supports_system_messages,
        "tool_choice": config.supports_tool_choice,
        "response_schema": config.supports_response_schema,
        "web_search": config.supports_web_search,
        "pdf_input": config.supports_pdf_input,
        "audio_input": config.supports_audio_input,
        "audio_output": config.supports_audio_output,
        "prompt_caching": config.supports_prompt_caching,
        "native_streaming": config.supports_native_streaming,
        "reasoning": config.supports_reasoning,
    }

    for capability, supported in capabilities.items():
        icon = "✓" if supported else "✗"
        color = "green" if supported else "red"
        console.print(
            f"  {icon} [bold {color}]{capability.replace('_', ' ').title()}[/bold {color}]"
        )

    # Check for deprecation
    deprecation_date = config.get_deprecation_date()
    if deprecation_date:
        console.print(
            f"\n[bold red]⚠️ Model will be deprecated on: {deprecation_date}[/bold red]"
        )

    # Check additional data if available
    if config.supports_web_search:
        search_costs = config.get_search_context_costs()
        if search_costs:
            console.print("\n[bold]Web Search Context Costs:[/bold]")
            for size, cost in search_costs.items():
                console.print(f"  {size}: [yellow]{format_pricing(cost)}[/yellow]")

    # Instead of returning, collect data for the comparison and assert it's valid
    metadata = config.format_metadata_for_display()

    # Assert key metadata properties
    assert metadata["name"] == model_config["name"], "Name should match"
    assert metadata["provider"] == model_config["provider"], "Provider should match"
    assert metadata["model"] == model, "Model should match"
    assert metadata["context_window"] == context_window, "Context window should match"
    assert metadata["max_input"] == max_input, "Max input should match"
    assert metadata["max_output"] == max_output, "Max output should match"
    assert metadata["input_cost"] == input_cost, "Input cost should match"
    assert metadata["output_cost"] == output_cost, "Output cost should match"
    assert metadata["capabilities"] == capabilities, "Capabilities should match"
    assert (
        metadata["deprecation_date"] == deprecation_date
    ), "Deprecation date should match"


def test_compare_models(available_models):
    """Compare metadata across all available models."""
    if len(available_models) < 2:
        pytest.skip("Need at least 2 models with API keys for comparison")

    # Collect data for all models
    models_data = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            "Collecting model data for comparison...", total=len(available_models)
        )

        for model_config in available_models:
            # Create the config
            config_class = model_config["class"]
            model = model_config["model"]
            config = config_class(model=model)

            # Get metadata formatted for display
            metadata = config.format_metadata_for_display()
            models_data.append(metadata)

            progress.update(task, advance=1)

    # Display comparison tables
    console.print(
        Panel(Text("Model Metadata Comparison", style="bold cyan", justify="center"))
    )
    display_model_metadata_table(models_data)

    console.print("\n")
    console.print(
        Panel(
            Text("Model Capabilities Comparison", style="bold cyan", justify="center")
        )
    )
    display_model_capabilities(models_data)

    # Export comparison to JSON
    try:
        with open("model_comparison.json", "w") as f:
            json.dump(models_data, f, indent=2, default=str)
        console.print(
            "\n[green]Exported comparison data to model_comparison.json[/green]"
        )
    except Exception as e:
        console.print(f"\n[red]Failed to export comparison data: {e}[/red]")

    # Assert we have data from all models
    assert len(models_data) == len(
        available_models
    ), "Should have data for all available models"


if __name__ == "__main__":
    # When run directly, execute specific tests
    console.print(
        Panel(Text("LLM Metadata Test Suite", style="bold cyan", justify="center"))
    )

    # Get available models
    available = []
    for config in MODEL_CONFIGS:
        if check_env_var(config["env_var"]):
            available.append(config)
        else:
            console.print(
                f"[yellow]Skipping {config['name']} - {config['env_var']} not set[/yellow]"
            )

    if not available:
        console.print(
            "[bold red]No API keys found! Set at least one of AZURE_OPENAI_API_KEY, ANTHROPIC_API_KEY, or MISTRAL_API_KEY[/bold red]"
        )
        exit(1)

    # Run individual tests
    model_data = []
    for model in available:
        try:
            test_model_metadata_access(model)  # Just call, don't store result
            console.print("\n" + "-" * 80 + "\n")
        except Exception as e:
            console.print(f"[bold red]Error testing {model['name']}: {e}[/bold red]")

    # Run comparison if we have multiple models
    if len(available) >= 2:
        test_compare_models(available)
