#!/usr/bin/env python3
"""
LLM Provider Discovery Tool for Haive

This script discovers and lists all available LLM providers, their configurations,
and supported models using the haive component discovery system.
"""

import sys
from pathlib import Path

# Add haive packages to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))

from haive.core.utils.haive_discovery.llm_provider_discovery import LLMProviderDiscovery


def main():
    """Main function to discover and document LLM providers."""
    print("🧠 Discovering LLM Providers using Haive Discovery System...\n")
    
    # Initialize discovery system
    discovery = LLMProviderDiscovery()
    
    # Discover all providers
    providers = discovery.discover_providers()
    
    print(f"🎉 Discovered {len(providers)} LLM providers")
    
    # Create summary
    summary = discovery.create_provider_summary(providers)
    
    # Save comprehensive documentation
    output_dir = project_root / "project_docs"
    file_paths = discovery.save_providers_documentation(providers, output_dir)
    
    print(f"\n📊 Summary:")
    print(f"   - Total providers: {summary['total_providers']}")
    print(f"   - With function calling: {summary['with_function_calling']}")
    print(f"   - With vision support: {summary['with_vision']}")
    print(f"   - With embedding support: {summary['with_embedding']}")
    print(f"   - With fine-tuning support: {summary['with_fine_tuning']}")
    
    print(f"\n📄 Generated Files:")
    for file_type, file_path in file_paths.items():
        print(f"   - {file_type.title()}: {file_path}")
    
    # Print top providers by capability
    print(f"\n🔥 Top Providers by Capability:")
    for provider in summary["providers"][:5]:
        caps = [k for k, v in provider["capabilities"].items() if v]
        print(f"   - {provider['name']}: {', '.join(caps)}")


if __name__ == "__main__":
    main()