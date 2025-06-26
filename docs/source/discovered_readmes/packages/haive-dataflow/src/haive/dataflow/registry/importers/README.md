# Registry Importers

Importers for bringing external component data into the Haive registry system.

## Overview

The importers module provides functionality for importing component data from external sources, such as LiteLLM's model list, embedding model providers, and other component repositories. These importers enable the registry system to be populated with data from various sources, expanding the available components without manual registration.

## Available Importers

### LiteLLM Importer

The `litellm_importer.py` module provides functionality for importing LLM model data from LiteLLM:

- Fetches model information from LiteLLM
- Extracts model metadata (provider, capabilities, etc.)
- Registers models in the registry system
- Creates appropriate configurations

### Embeddings Importer

The `embeddings_importer.py` module handles importing embedding model data:

- Imports embedding models from various providers
- Extracts model capabilities and specifications
- Registers models with appropriate configurations

## Usage Example

```python
from haive.dataflow.registry.importers.litellm_importer import import_litellm_models
from haive.dataflow.registry.importers.embeddings_importer import import_embedding_models

# Import LLM models from LiteLLM
session_id, import_count = import_litellm_models()
print(f"Imported {import_count} LLM models in session {session_id}")

# Import embedding models
embedding_session_id, embedding_count = import_embedding_models()
print(f"Imported {embedding_count} embedding models in session {embedding_session_id}")
```

## Implementing a Custom Importer

To implement a custom importer:

1. Create a new module in the `importers` package
2. Define a main import function that:
   - Fetches data from the external source
   - Transforms it to the registry format
   - Registers components using the registry system
   - Logs import operations
3. Handle errors and edge cases appropriately

Example structure for a custom importer:

```python
def import_custom_components(source_url=None):
    """
    Import components from a custom source.

    Args:
        source_url: Optional URL to fetch components from

    Returns:
        Tuple of (session_id, import_count)
    """
    # Generate session ID
    session_id = str(uuid.uuid4())
    import_count = 0

    try:
        # Fetch data from source
        components = fetch_data(source_url)

        # Process and register components
        for component in components:
            try:
                # Transform data
                registry_data = transform_component(component)

                # Register in registry system
                registry_id = registry_system.register_entity(
                    name=registry_data["name"],
                    type=registry_data["type"],
                    # ... other fields ...
                )

                # Log success
                registry_system.log_import(
                    import_session=session_id,
                    entity_name=registry_data["name"],
                    entity_type=registry_data["type"],
                    status=ImportStatus.SUCCESS
                )

                import_count += 1

            except Exception as e:
                # Log failure
                registry_system.log_import(
                    import_session=session_id,
                    entity_name=component.get("name", "unknown"),
                    entity_type="custom",
                    status=ImportStatus.FAILURE,
                    message=str(e),
                    traceback=traceback.format_exc()
                )

        return session_id, import_count

    except Exception as e:
        logger.error(f"Failed to import custom components: {e}")
        return session_id, import_count
```
