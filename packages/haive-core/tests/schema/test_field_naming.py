#!/usr/bin/env python3
"""
Test field naming utilities.
"""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from pydantic import BaseModel, Field

from haive.core.schema.field_utils import (
    camel_to_snake_case,
    create_field_name_from_model,
    field_name,
    get_field_info_from_model,
)


# Test models
class QueryRefinementResponse(BaseModel):
    """Test model for field naming."""

    pass


@field_name("custom_query_result")
class CustomQueryResult(BaseModel):
    """Test model with custom field name."""

    pass


def test_field_naming():
    """Test field naming utilities."""
    print("=== Testing Field Naming Utilities ===")

    # Test camel_to_snake_case
    print(
        f"camel_to_snake_case('QueryRefinementResponse'): {camel_to_snake_case('QueryRefinementResponse')}"
    )
    print(f"camel_to_snake_case('UserProfile'): {camel_to_snake_case('UserProfile')}")
    print(f"camel_to_snake_case('APIKey'): {camel_to_snake_case('APIKey')}")

    # Test create_field_name_from_model
    print(
        f"create_field_name_from_model(QueryRefinementResponse): {create_field_name_from_model(QueryRefinementResponse)}"
    )
    print(
        f"create_field_name_from_model(QueryRefinementResponse, remove_suffixes=False): {create_field_name_from_model(QueryRefinementResponse, remove_suffixes=False)}"
    )

    # Test get_field_info_from_model
    print(
        f"get_field_info_from_model(QueryRefinementResponse): {get_field_info_from_model(QueryRefinementResponse)}"
    )
    print(
        f"get_field_info_from_model(CustomQueryResult): {get_field_info_from_model(CustomQueryResult)}"
    )

    return get_field_info_from_model(QueryRefinementResponse)


if __name__ == "__main__":
    field_info = test_field_naming()
    print(
        f"\nExpected field name for QueryRefinementResponse: {field_info['field_name']}"
    )
