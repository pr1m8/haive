#!/usr/bin/env python3
"""
Tools and Schema Discovery Tool for Haive

This script uses the haive component discovery system to find all available
tools, toolkits, and their schemas across the haive packages.
"""

import sys
from pathlib import Path

# Add haive packages to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))
sys.path.insert(0, str(project_root / "packages" / "haive-tools" / "src"))

from haive.core.utils.haive_discovery.enhanced_tool_discovery import EnhancedToolDiscovery


def main():
    """Main function to discover and document tools."""
    print("🔍 Discovering Tools and Schemas using Enhanced Haive Discovery...\n")
    
    # Initialize enhanced discovery system
    discovery = EnhancedToolDiscovery(str(project_root))
    
    # Discover all tools with enhanced schema analysis
    results = discovery.discover_tools_with_enhanced_schemas()
    
    print(f"\n🎉 Enhanced Discovery Complete!")
    print(f"   - Individual Tools: {results['summary']['individual_tools']}")
    print(f"   - Toolkits: {results['summary']['toolkits']}")
    print(f"   - Retrievers: {results['summary']['retrievers']}")
    print(f"   - Vector Stores: {results['summary']['vector_stores']}")
    print(f"   - Document Loaders: {results['summary']['document_loaders']}")
    print(f"   - Engines: {results['summary']['engines']}")
    print(f"   - Total Tools Found: {results['summary']['total_tools']}")
    
    # Create comprehensive documentation
    output_dir = project_root / "project_docs"
    file_paths = discovery.create_comprehensive_documentation(results, output_dir)
    
    print(f"\n📄 Generated Files:")
    for file_type, file_path in file_paths.items():
        print(f"   - {file_type.replace('_', ' ').title()}: {file_path}")
    
    # Print some interesting stats
    categories_with_tools = [cat for cat, data in results["categories"].items() 
                           if sum(item["tool_count"] for item in data["items"]) > 0]
    
    print(f"\n🔥 Categories with Tools: {len(categories_with_tools)}")
    for category in categories_with_tools:
        tool_count = sum(item["tool_count"] for item in results["categories"][category]["items"])
        print(f"   - {category.replace('_', ' ').title()}: {tool_count} tools")


if __name__ == "__main__":
    main()