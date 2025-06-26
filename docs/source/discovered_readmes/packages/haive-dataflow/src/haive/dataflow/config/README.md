# Haive Configuration Module

Configuration management for the Haive framework, providing environment-specific settings and environment variable handling.

## Overview

The configuration module centralizes all application settings, allowing for consistent and type-safe configuration across the Haive framework. It uses Pydantic models for settings validation and provides mechanisms for loading settings from environment variables.

## Module Structure

```
config/
├── __init__.py         # Package exports
├── settings.py         # Application settings models
└── environment.py      # Environment variable handling
```

## Key Components

### Settings Models

The `settings.py` module defines Pydantic models for application settings:

- `AppSettings`: Top-level application settings
- `APISettings`: API-specific settings
- `AgentSettings`: Agent-specific settings

These models include default values, validation, and automatic loading from environment variables.

### Environment Variable Handling

The `environment.py` module provides utilities for working with environment variables:

- Loading environment variables from `.env` files
- Resolving sensitive configuration like API keys
- Providing access to service configurations (Supabase, etc.)

## Usage Examples

### Accessing Settings

```python
from haive.dataflow.config.settings import get_settings

# Get application settings
settings = get_settings()

# Access specific settings
api_prefix = settings.api.prefix
is_prod = settings.is_production
agent_timeout = settings.agent.default_timeout

# Use in application logic
if settings.is_development:
    print(f"Running in development mode with prefix {api_prefix}")
```

### Environment-Specific Configuration

The settings system automatically adapts to the current environment based on the `ENVIRONMENT` variable:

- `development`: Default development settings
- `staging`: Staging environment settings
- `production`: Production environment settings

## Configuration Reference

### API Settings

| Environment Variable | Description                             | Default     |
| -------------------- | --------------------------------------- | ----------- |
| `API_DEBUG`          | Enable debug mode                       | `false`     |
| `API_TITLE`          | API title for OpenAPI docs              | `Haive API` |
| `API_PREFIX`         | URL prefix for all endpoints            | `/api`      |
| `CORS_ORIGINS`       | Comma-separated list of allowed origins | `*`         |
| `RATE_LIMIT`         | Requests per minute rate limit          | `60`        |

### Agent Settings

| Environment Variable | Description                | Default |
| -------------------- | -------------------------- | ------- |
| `AGENT_TIMEOUT`      | Default timeout in seconds | `60`    |
| `AGENT_STREAMING`    | Enable response streaming  | `true`  |
| `AGENT_COST_PER_1K`  | Credit cost per 1K tokens  | `0.01`  |

### Application Settings

| Environment Variable | Description             | Default       |
| -------------------- | ----------------------- | ------------- |
| `ENVIRONMENT`        | Application environment | `development` |

## Extending Configuration

To add new settings:

1. Define a new Pydantic model in `settings.py`
2. Add default values and environment variable loading
3. Include the new model in the appropriate parent model

Example:

```python
class DatabaseSettings(BaseModel):
    """Database-specific settings."""
    url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///app.db"))
    pool_size: int = Field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "5")))

# Update AppSettings to include the new settings
class AppSettings(BaseModel):
    # Existing fields...
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
```
