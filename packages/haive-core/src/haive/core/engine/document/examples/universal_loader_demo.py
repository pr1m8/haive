"""Universal Document Loader Demo.

This script demonstrates how to use the Universal Document Loader to automatically
detect and load documents from any source with intelligent source detection.
"""

import sys
from pathlib import Path
from typing import Any, Dict

# Add the package root to the path for import
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from haive.core.engine.document import (
    CredentialManager,
    UniversalDocumentLoader,
    analyze_document_source,
    load_document,
)


def demo_universal_loader():
    """Demonstrate the universal loader capabilities."""

    print("🚀 Universal Document Loader Demo")
    print("=" * 50)

    # Create a universal loader
    credential_manager = CredentialManager()

    # Add some example credentials (you would normally load these from config)
    # credential_manager.add_credential("github", Credential(
    #     credential_type=CredentialType.ACCESS_TOKEN,
    #     value="your_github_token_here"
    # ))

    loader = UniversalDocumentLoader(credential_manager)

    # Test paths for demonstration
    test_paths = [
        # Web sources
        "https://github.com/microsoft/vscode",
        "https://reddit.com/r/programming",
        "https://news.ycombinator.com",
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://arxiv.org/abs/2301.00001",
        "https://huggingface.co/datasets/squad",
        # File sources
        "document.pdf",
        "data.csv",
        "code.py",
        "presentation.pptx",
        "README.md",
        "config.yaml",
        "notebook.ipynb",
        # Chat exports
        "whatsapp_chat.txt",
        "discord_export.json",
        # Database sources
        "postgresql://user:pass@localhost/db",
        "mongodb://localhost:27017/mydb",
        # Cloud sources
        "s3://my-bucket/documents/",
        "gs://my-bucket/data.csv",
    ]

    print("\\n📋 Analyzing various document sources...")
    print("-" * 50)

    for path in test_paths:
        print(f"\\n🔍 Analyzing: {path}")

        # Analyze the source
        analysis = loader.analyze_source(path)

        print(f"   📊 Found {len(analysis['candidates'])} potential loaders")
        if analysis["recommended"]:
            print(f"   ⭐ Recommended: {analysis['recommended']}")
        if analysis["supports_auth"]:
            print(f"   🔐 Requires authentication")

        # Show top 3 candidates
        for i, candidate in enumerate(analysis["candidates"][:3]):
            confidence = candidate["confidence"]
            source_type = candidate["source_type"]
            print(f"      {i+1}. {source_type} (confidence: {confidence:.2f})")

    print("\\n\\n🎯 Testing actual loader creation...")
    print("-" * 50)

    # Test actual loader creation for a few examples
    test_loads = [
        ("document.pdf", {"pdf_strategy": "pymupdf", "extract_images": True}),
        ("data.csv", {"csv_args": {"delimiter": ","}}),
        ("https://github.com/microsoft/vscode", {"include_issues": False}),
    ]

    for path, preferences in test_loads:
        print(f"\\n📄 Creating loader for: {path}")
        try:
            doc_loader = loader.load(path, preferences=preferences)
            if doc_loader:
                print(f"   ✅ Successfully created: {type(doc_loader).__name__}")
            else:
                print(f"   ❌ Failed to create loader")
        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    print("\\n\\n📚 Using convenience functions...")
    print("-" * 50)

    # Demonstrate convenience functions
    test_convenience = [
        "README.md",
        "https://en.wikipedia.org/wiki/Python",
    ]

    for path in test_convenience:
        print(f"\\n📖 Loading with convenience function: {path}")
        try:
            # Use the convenience function
            doc_loader = load_document(path)
            if doc_loader:
                print(f"   ✅ Created: {type(doc_loader).__name__}")
            else:
                print(f"   ❌ Failed to create loader")

            # Analyze with convenience function
            analysis = analyze_document_source(path)
            print(f"   📊 Analysis: {analysis['recommended']} recommended")

        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    print("\\n\\n🏁 Demo completed!")
    print("\\nKey Features Demonstrated:")
    print("• ✨ Automatic source detection")
    print("• 🎯 Intelligent loader selection")
    print("• 📊 Confidence scoring")
    print("• 🔐 Authentication support")
    print("• 🛠️ Preference-based selection")
    print("• 🔄 Fallback mechanisms")
    print("• 🎮 Easy-to-use convenience functions")


def show_supported_sources():
    """Show all supported source types."""

    print("\\n📋 Supported Source Types")
    print("=" * 30)

    loader = UniversalDocumentLoader()
    sources = loader.get_supported_sources()

    # Group by category
    categories = {
        "Web & Social": [
            s
            for s in sources
            if any(
                keyword in s.lower()
                for keyword in [
                    "github",
                    "reddit",
                    "twitter",
                    "web",
                    "wiki",
                    "arxiv",
                    "news",
                    "social",
                ]
            )
        ],
        "File Formats": [
            s
            for s in sources
            if any(
                keyword in s.lower()
                for keyword in [
                    "pdf",
                    "csv",
                    "json",
                    "excel",
                    "word",
                    "text",
                    "image",
                    "code",
                ]
            )
        ],
        "Databases": [
            s
            for s in sources
            if any(keyword in s.lower() for keyword in ["sql", "mongo", "database"])
        ],
        "Cloud Storage": [
            s
            for s in sources
            if any(keyword in s.lower() for keyword in ["s3", "gcs", "azure", "cloud"])
        ],
        "Other": [],
    }

    # Put uncategorized sources in "Other"
    categorized = set()
    for cat_sources in categories.values():
        categorized.update(cat_sources)

    categories["Other"] = [s for s in sources if s not in categorized]

    for category, cat_sources in categories.items():
        if cat_sources:
            print(f"\\n{category}:")
            for source in sorted(cat_sources):
                print(f"  • {source}")

    print(f"\\n📊 Total: {len(sources)} source types supported")


if __name__ == "__main__":
    demo_universal_loader()
    show_supported_sources()
