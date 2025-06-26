# Haive Tools Documentation Checklist

This checklist tracks the progress of adding Google-style docstrings and Sphinx documentation to all tools and toolkits in the haive-tools package. Each item requires proper docstrings for module, classes, methods, and functions following Google style format.

## Documentation Format Requirements

All documentation should follow these guidelines:

1. **Module-level docstrings**:
   - Brief description of the module
   - Detailed description of purpose and functionality
   - Usage examples
   - Any required environment variables or setup

2. **Class docstrings**:
   - Brief description
   - Detailed explanation of the class purpose
   - Attributes section with all class attributes documented
   - Example usage if applicable

3. **Method/Function docstrings**:
   - Brief description
   - Args section with all parameters documented (type and description)
   - Returns section with return type and description
   - Raises section if applicable
   - Examples if the usage is complex

4. **Pydantic Models**:
   - Each field should have a description using Field(..., description="...")

## Individual Tools

### Search & Knowledge Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/arxiv.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/asknews_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/bing_search_tool_INC.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/brave_search.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/duckduckgo_search.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_scholar.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_search.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_trends.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pubmed.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/stack_exchange.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/youtube_search_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/merriam_webster.py`

### Data & Information Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/agify_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/apify_tools.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/binlist_lookup.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dataforseo_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/domain_search_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/fruityvice_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/genderize_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/open_food_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/openaq_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pokebase_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/yfinance_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/ionic_tool.py`

### Media & Generation Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dalle_image_generator_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/eleven_labs.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/scene_explain_tool.py`

### Messaging & Communication Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/discord_tools.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/translate_tools.py`

### Humor & Entertainment Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/corporate_bs_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/geek_jokes_tool.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py`

### Development Tools

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dev_tools.py`

## Toolkits

### Finance Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/alpha_vantage.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/financialdatasets_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/fred_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/polygon_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/stripe_toolkit.py`

### Data & Analytics Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/azure_ai_services_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dataforseo_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/mongodb_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/nasa_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/nla_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/pandas_toolkits.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/powerbi_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/sql_db_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/weather.py`

### Entertainment & Fun Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/chuck_norris_jokes_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/free_to_game_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/rick_and_morty_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/rps_101_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/steam_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/useless_facts_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/yugiioh_toolkit.py`

### Travel & Location Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/amadues_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/citydsk_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/lcbo_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/trip_advisor_toolkit.py`

### Knowledge & Information Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/openlibrary_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/poetry_db_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/stack_exchange_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/vbible_toolkit.py`

### Productivity & Collaboration Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/clickup_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/github_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/gitlab_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/gmail_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/google_calendar.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/gradio_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/jira_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/office_365.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/slack_toolkit.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/twilio_toolkit.py`

### Utility Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/base.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/request_tools.py`

### Development Toolkits

- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/project_creation/github.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/function_logging_transformer.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/print_to_logging.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/automatic_test_case_generator.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/function_call_analyzer.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/background_process_manager.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/logger.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/permission.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/remote_execution.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/shell.py`
- [x] `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/tools.py`

## Documentation Progress

- Total tools and toolkits: 103
- Documented: 103
- Remaining: 0
- Progress: 100%

## Documentation Templates

### Tool Template

```python
"""
Tool Module Name

Brief description of what this tool does and what API/service it interacts with.
Additional details about functionality, usage scenarios, or any requirements.

Examples:
    >>> from haive.tools.tools.module_name import function_name
    >>> result = function_name()
    >>> print(result)
"""

import requests
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """
    Response model for the tool.

    Attributes:
        field_name (type): Description of the field.
        another_field (type): Description of another field.
    """
    field_name: type = Field(..., description="Description of the field")
    another_field: type = Field(..., description="Description of another field")


def function_name(param1: type, param2: type = default) -> ResponseModel:
    """
    Brief description of what the function does.

    Args:
        param1 (type): Description of first parameter.
        param2 (type, optional): Description of second parameter. Defaults to default.

    Returns:
        ResponseModel: Description of the return value.

    Raises:
        RequestException: If the API request fails.
    """
    # Implementation


# Tool definition
ToolName = [
    StructuredTool.from_function(
        func=function_name,
        name="function_name",
        description="Detailed description of what the tool does and when to use it"
    )
]
```

### Toolkit Template

```python
"""
Toolkit Module Name

Brief description of what this toolkit provides and what APIs/services it interacts with.
Additional details about functionality, usage scenarios, or any requirements.

Examples:
    >>> from haive.tools.toolkits.module_name import ToolkitName
    >>> # Use the toolkit
    >>> result = function_from_toolkit()
"""

import requests
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    """
    Response model for the toolkit.

    Attributes:
        field_name (type): Description of the field.
        another_field (type): Description of another field.
    """
    field_name: type = Field(..., description="Description of the field")
    another_field: type = Field(..., description="Description of another field")


def function_one(param1: type, param2: type = default) -> ResponseModel:
    """
    Brief description of what the function does.

    Args:
        param1 (type): Description of first parameter.
        param2 (type, optional): Description of second parameter. Defaults to default.

    Returns:
        ResponseModel: Description of the return value.

    Raises:
        RequestException: If the API request fails.
    """
    # Implementation


def function_two(param1: type) -> List[ResponseModel]:
    """
    Brief description of what the function does.

    Args:
        param1 (type): Description of first parameter.

    Returns:
        List[ResponseModel]: Description of the return value.

    Raises:
        RequestException: If the API request fails.
    """
    # Implementation


# Toolkit definition
ToolkitName = [
    StructuredTool.from_function(
        func=function_one,
        name="function_one_name",
        description="Detailed description of what the tool does and when to use it"
    ),
    StructuredTool.from_function(
        func=function_two,
        name="function_two_name",
        description="Detailed description of what the tool does and when to use it"
    )
]
```
