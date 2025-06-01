import csv
import sys
from pathlib import Path

# Adjust the path to import base.py from haive-core
sys.path.append(str(Path(__file__).resolve().parent.parent / "packages/haive-core/src/haive/core/models/llm"))

from base import (
    AnthropicLLMConfig,
    OpenAILLMConfig,
    MistralLLMConfig,
    DeepSeekLLMConfig,
)

# List of (class, provider_name, filename)
PROVIDERS = [
    (AnthropicLLMConfig, "anthropic", "anthropic_models.csv"),
    (OpenAILLMConfig, "openai", "openai_models.csv"),
    (MistralLLMConfig, "mistral", "mistral_models.csv"),
    (DeepSeekLLMConfig, "deepseek", "deepseek_models.csv"),
    # Add more here if their get_models() returns a list of model names
]


def save_models_to_csv(model_names, filename):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["model_name"])
        for name in model_names:
            writer.writerow([name])


def main():
    summary = []
    for config_cls, provider, filename in PROVIDERS:
        try:
            print(f"Fetching models for {provider}...")
            models = config_cls.get_models()
            # Some APIs return objects, not just strings
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