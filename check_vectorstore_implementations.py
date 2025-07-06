#!/usr/bin/env python3
"""Check all vector store implementations in the providers directory."""

import os
import re
from pathlib import Path


def check_vector_stores():
    """Check all vector store implementations."""

    # Path to providers directory
    providers_path = Path(
        "packages/haive-core/src/haive/core/engine/vectorstore/providers"
    )

    # Get all config files
    config_files = sorted(
        [
            f
            for f in providers_path.glob("*VectorStoreConfig.py")
            if f.name != "__init__.py"
        ]
    )


    # Categories for organization
    categories = {
        "Core Open Source": ["Chroma", "FAISS", "Qdrant", "Weaviate", "Milvus"],
        "Cloud/Managed": [
            "Pinecone",
            "Zilliz",
            "MongoDBAtlas",
            "AzureSearch",
            "Vectara",
            "Marqo",
        ],
        "Database Extensions": ["PGVector", "Supabase", "ClickHouse", "Cassandra"],
        "Search Engines": [
            "Elasticsearch",
            "Typesense",
            "OpenSearch",
            "AmazonOpenSearch",
        ],
        "In-Memory/Cache": ["Redis", "InMemory"],
        "Specialized Stores": ["LanceDB", "DocArray", "Annoy", "USearch", "SKLearn"],
        "Graph Databases": ["Neo4j"],
    }

    # Create reverse mapping
    store_to_category = {}
    for category, stores in categories.items():
        for store in stores:
            store_to_category[store.lower()] = category

    # Track implementations
    implemented = {}

    # Check each config file
    for config_file in config_files:
        # Extract store name from filename
        store_name = config_file.stem.replace("VectorStoreConfig", "")

        # Read the file to get details
        with open(config_file) as f:
            content = f.read()

        # Check for registration
        register_match = re.search(
            r"@BaseVectorStoreConfig\.register\(VectorStoreType\.(\w+)\)", content
        )
        registered_type = register_match.group(1) if register_match else "NOT REGISTERED"

        # Check for SecureConfigMixin
        uses_secure = "SecureConfigMixin" in content

        # Check for custom validate_embedding
        has_custom_validate = "def validate_embedding(self)" in content

        # Get category
        category = store_to_category.get(store_name.lower(), "Uncategorized")

        implemented[store_name] = {
            "file": config_file.name,
            "registered_type": registered_type,
            "uses_secure": uses_secure,
            "custom_validate": has_custom_validate,
            "category": category,
        }

    # Print by category
    for category in categories:
        stores_in_category = [
            s for s, info in implemented.items() if info["category"] == category
        ]
        if stores_in_category:
            for store in sorted(stores_in_category):
                info = implemented[store]
                details = []
                if info["uses_secure"]:
                    details.append("SecureConfig")
                if info["custom_validate"]:
                    details.append("CustomValidation")
                detail_str = f" ({', '.join(details)})" if details else ""

    # Check for uncategorized
    uncategorized = [
        s for s, info in implemented.items() if info["category"] == "Uncategorized"
    ]
    if uncategorized:
        for store in sorted(uncategorized):
            info = implemented[store]

    # Check __init__.py imports

    init_file = providers_path / "__init__.py"
    with open(init_file) as f:
        init_content = f.read()

    # Check imports
    missing_imports = []
    missing_exports = []

    for store in implemented:
        config_class = f"{store}VectorStoreConfig"

        # Check import
        if f"from .{config_class} import {config_class}" not in init_content:
            missing_imports.append(config_class)

        # Check export
        if f'"{config_class}"' not in init_content:
            missing_exports.append(config_class)

    if missing_imports:
        pass)}")
    else:
        pass")

    if missing_exports:
        pass)}")
    else:
        pass")

    # Summary

    # List all store names for documentation
    all_stores = sorted(implemented.keys())
    for i in range(0, len(all_stores), 5):
        pass


if __name__ == "__main__":
    check_vector_stores()
