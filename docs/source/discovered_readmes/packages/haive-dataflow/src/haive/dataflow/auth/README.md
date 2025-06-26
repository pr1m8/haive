# Haive Authentication Module

Authentication and authorization functionality for the Haive API, providing secure access to endpoints and resources.

## Overview

The authentication module implements a secure, token-based authentication system for the Haive API. It integrates with Supabase for identity management and provides middleware, dependencies, and utilities for securing API endpoints.

## Module Structure

```
auth/
├── __init__.py           # Package exports
├── dependencies.py       # FastAPI dependencies for authentication
├── middleware.py         # Authentication middleware for FastAPI
├── supabase.py           # Supabase integration for authentication
└── credits.py            # Usage credits management
```

## Key Components

### Authentication Dependencies

The `dependencies.py` module provides FastAPI dependency functions for authentication:

- `get_current_user`: Optional authentication that returns the user ID if present
- `require_auth`: Required authentication that raises an exception if not authenticated
- `get_auth_instance`: Dependency for obtaining the auth service instance

### Supabase Authentication

The `supabase.py` module integrates with Supabase for identity management:

- JWT token validation
- User identity verification
- Role-based access control
- Session management

### Authentication Middleware

The `middleware.py` module provides FastAPI middleware for authentication:

- Automatic token extraction and validation
- Request enrichment with user information
- Authentication bypass for public endpoints

### Credits Management

The `credits.py` module handles usage credits for API users:

- Credit tracking and deduction
- Usage quotas and limits
- Subscription tier management

## Usage Examples

### Securing an Endpoint

```python
from fastapi import APIRouter, Depends
from haive.dataflow.auth.dependencies import require_auth

router = APIRouter()

@router.get("/secure-endpoint")
async def secure_endpoint(user_id: str = Depends(require_auth)):
    """
    This endpoint requires authentication.
    """
    return {"message": f"Hello, authenticated user {user_id}!"}
```

### Optional Authentication

```python
from fastapi import APIRouter, Depends
from typing import Optional
from haive.dataflow.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/partially-secure")
async def partially_secure(user_id: Optional[str] = Depends(get_current_user)):
    """
    This endpoint works with or without authentication.
    """
    if user_id:
        return {"message": f"Hello, authenticated user {user_id}!"}
    else:
        return {"message": "Hello, anonymous user!"}
```

### Adding Authentication Middleware

```python
from fastapi import FastAPI
from haive.dataflow.auth.middleware import SupabaseAuthMiddleware

app = FastAPI()

# Add authentication middleware
app.add_middleware(SupabaseAuthMiddleware)
```

## Authentication Flow

1. Client obtains JWT token from Supabase authentication service
2. Client includes token in Authorization header (`Bearer TOKEN`)
3. Middleware or dependency extracts and validates the token
4. If valid, the request proceeds with the authenticated user's ID
5. If invalid or missing (for protected routes), a 401 error is returned

## Security Considerations

- Tokens are validated cryptographically using Supabase JWT verification
- Tokens have a limited lifetime and must be refreshed
- All authenticated routes use HTTPS to protect token transmission
- Rate limiting is applied to prevent brute force attacks
