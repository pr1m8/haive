"""
LLM Model Export Utility.

This module provides functionality to export lists of available models from
various LLM providers to CSV files. It is used for model discovery, cataloging,
and generating reference lists for use throughout the Haive framework.

The utility handles different API response formats and properly extracts model
identifiers from provider-specific data structures.

Typical usage:
    ```
    python -m haive.core.models.llm.export_llm_models_to_csv
    ```

This will create CSV files in the current directory with model listings
from each configured provider.
"""

import csv
from typing import Any, List, Tuple, Type, Union

from base import (
    AnthropicLLMConfig,
    DeepSeekLLMConfig,
    MistralLLMConfig,
    OpenAILLMConfig,
)

# List of (class, provider_name, filename)
PROVIDERS: List[Tuple[Type, str, str]] = [
    (AnthropicLLMConfig, "anthropic", "anthropic_models.csv"),
    (OpenAILLMConfig, "openai", "openai_models.csv"),
    (MistralLLMConfig, "mistral", "mistral_models.csv"),
    (DeepSeekLLMConfig, "deepseek", "deepseek_models.csv"),
    # Add more here if their get_models() returns a list of model names
]


def save_models_to_csv(model_names: List[str], filename: str) -> None:
    """
    Save a list of model names to a CSV file.

    Args:
        model_names: List of model identifier strings
        filename: Output CSV filename

    The CSV file has a simple structure with a header row
    and one model name per row.
    """
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["model_name"])
        for name in model_names:
            writer.writerow([name])


def main() -> None:
    """
    Main function to fetch models from all providers and save to CSV files.

    This function:
    1. Iterates through the configured providers
    2. Fetches their available models
    3. Normalizes the response data into a list of model names
    4. Saves the model names to a CSV file
    5. Prints a summary of the results

    Error handling ensures that a failure with one provider
    doesn't prevent others from being processed.
    """
    summary = []
    for config_cls, provider, filename in PROVIDERS:
        try:
            print(f"Fetching models for {provider}...")
            models = config_cls.get_models()

            # Handle different API response formats
            if hasattr(models, "data"):
                # Try to extract .id from each model in .data
                model_names = [getattr(m, "id", str(m)) for m in models.data]
            elif isinstance(models, list):
                # List of strings or objects
                if all(isinstance(m, str) for m in models):
                    model_names = models
                else:
                    model_names = [getattr(m, "id", str(m)) for m in models]
            else:
                model_names = [str(models)]

            save_models_to_csv(model_names, filename)
            summary.append(f"{provider}: {len(model_names)} models saved to {filename}")
        except Exception as e:
            summary.append(f"{provider}: ERROR - {e}")

    print("\nSummary:")
    for line in summary:
        print(line)


if __name__ == "__main__":
    main()
