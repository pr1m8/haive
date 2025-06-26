# Authentication Handling for Document Loaders

## Overview

Many document loaders require authentication to access their data sources. This document outlines our approach to managing authentication for different loader types while maintaining security and flexibility.

## Authentication Requirements

Different loader types have different authentication requirements:

### API Keys

- GitHub API (`GITHUB_TOKEN`)
- YouTube API (`GOOGLE_API_KEY`)
- OpenAI API (`OPENAI_API_KEY`)
- Notion API (`NOTION_TOKEN`)
- Many others

### OAuth Credentials

- Google Drive/Docs
- Microsoft OneDrive/SharePoint
- Dropbox
- Slack

### Database Credentials

- Username/password
- Connection strings
- Access tokens

### Cloud Storage Credentials

- AWS credentials (access key, secret key)
- GCP service account keys
- Azure connection strings

### Special Requirements

- SSH keys for Git repositories
- Signed URLs for cloud storage
- Session cookies for web services

## Authentication Strategy

We'll implement a multi-layered authentication strategy:

### 1. Credential Provider Interface

```python
class CredentialProvider(Protocol):
    """Protocol for credential providers."""

    def get_credential(self, credential_name: str) -> Optional[Dict[str, Any]]:
        """Get a credential by name."""
        ...

    def store_credential(self, credential_name: str, credential: Dict[str, Any]) -> bool:
        """Store a credential."""
        ...

    def list_available_credentials(self) -> List[str]:
        """List available credential names."""
        ...
```

### 2. Environment-based Provider

```python
class EnvironmentCredentialProvider(BaseModel):
    """Provides credentials from environment variables."""

    prefix: str = "HAIVE_"
    env_map: Dict[str, str] = Field(default_factory=dict)

    def get_credential(self, credential_name: str) -> Optional[Dict[str, Any]]:
        """Get credentials from environment variables."""
        # Check direct environment variable
        env_var = f"{self.prefix}{credential_name.upper()}"
        if env_var in os.environ:
            return {"value": os.environ[env_var]}

        # Check mapped variables
        if credential_name in self.env_map:
            mapped_var = self.env_map[credential_name]
            if mapped_var in os.environ:
                return {"value": os.environ[mapped_var]}

        # Check JSON-encoded credentials
        json_var = f"{self.prefix}{credential_name.upper()}_JSON"
        if json_var in os.environ:
            try:
                return json.loads(os.environ[json_var])
            except:
                pass

        return None
```

### 3. File-based Provider

```python
class FileCredentialProvider(BaseModel):
    """Provides credentials from a file."""

    credential_file: Path = Field(default_factory=lambda: Path.home() / ".haive" / "credentials.json")
    credentials: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)
        self._load_credentials()

    def _load_credentials(self):
        """Load credentials from file."""
        if self.credential_file.exists():
            try:
                with open(self.credential_file, "r") as f:
                    self.credentials = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load credentials: {e}")

    def get_credential(self, credential_name: str) -> Optional[Dict[str, Any]]:
        """Get a credential by name."""
        return self.credentials.get(credential_name)
```

### 4. Secret Manager Provider

```python
class SecretManagerCredentialProvider(BaseModel):
    """Provides credentials from a secret manager."""

    # Implementation depends on the secret manager (AWS Secrets Manager, GCP Secret Manager, etc.)
    # This is a simplified version

    def get_credential(self, credential_name: str) -> Optional[Dict[str, Any]]:
        """Get a credential from the secret manager."""
        try:
            # Implementation for specific secret manager
            secret = self._get_secret(credential_name)
            return json.loads(secret)
        except:
            return None
```

### 5. Credential Manager

```python
class CredentialManager(BaseModel):
    """Manages credentials from multiple providers."""

    providers: List[CredentialProvider] = Field(default_factory=list)

    def get_credential(self, credential_name: str) -> Optional[Dict[str, Any]]:
        """Get a credential from any provider."""
        for provider in self.providers:
            credential = provider.get_credential(credential_name)
            if credential:
                return credential
        return None
```

## Integration with Source Types

Each source type that requires authentication will specify:

```python
class GitHubSource(RemoteSource):
    """GitHub repository source."""

    repo_url: HttpUrl
    include_issues: bool = True
    include_code: bool = True

    class Config:
        # Authentication requirements
        required_credentials = ["github_token"]
        optional_credentials = []

    def authenticate(self, credential_manager: CredentialManager) -> bool:
        """Authenticate the source."""
        credential = credential_manager.get_credential("github_token")
        if not credential:
            return False

        self.github_token = credential.get("value")
        return bool(self.github_token)
```

## Integration with Loader Strategies

Loader strategies will specify authentication requirements:

```python
@dataclass
class LoaderStrategy:
    # ... other fields ...

    # Authentication
    required_credentials: List[str] = field(default_factory=list)
    optional_credentials: List[str] = field(default_factory=list)

    def check_authentication(self, credential_manager: CredentialManager) -> bool:
        """Check if all required credentials are available."""
        for cred_name in self.required_credentials:
            if not credential_manager.get_credential(cred_name):
                return False
        return True
```

## Secure Handling of Credentials

### Storage Security

1. Environment variables
   - Never logged or exposed in error messages
   - No persistence between sessions

2. Credential files
   - Stored with restricted permissions (600)
   - Optionally encrypted at rest
   - Located in user home directory

3. Secret managers
   - AWS Secrets Manager, GCP Secret Manager, Azure Key Vault
   - Industry-standard encryption and access controls

### Runtime Security

1. Never log credentials
2. Redact credentials in error messages
3. Clear credentials from memory when no longer needed
4. No serialization of credential objects

### OAuth Flow

For OAuth-based authentication:

```python
class OAuthHelper(BaseModel):
    """Helper for OAuth authentication."""

    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str]

    def get_authorization_url(self) -> str:
        """Get the authorization URL."""
        # Implementation depends on the service

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange an authorization code for a token."""
        # Implementation depends on the service

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh an OAuth token."""
        # Implementation depends on the service
```

## Credential Format Standardization

All credentials will follow a standard format:

```python
# Simple API key
{
    "type": "api_key",
    "value": "sk-1234567890abcdef"
}

# Username/password
{
    "type": "basic",
    "username": "user",
    "password": "pass"
}

# OAuth token
{
    "type": "oauth",
    "access_token": "token",
    "refresh_token": "refresh",
    "expires_at": 1234567890,
    "scopes": ["read", "write"]
}

# Service account
{
    "type": "service_account",
    "client_email": "service@project.iam.gserviceaccount.com",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...",
    "project_id": "project-id"
}
```

## Source Credential Requirements Registry

We'll maintain a registry of credential requirements for each source type:

```python
CREDENTIAL_REQUIREMENTS = {
    "github": {
        "required": ["github_token"],
        "optional": [],
        "environment_vars": ["GITHUB_TOKEN"]
    },
    "google_drive": {
        "required": ["google_credentials"],
        "optional": [],
        "environment_vars": [
            "GOOGLE_APPLICATION_CREDENTIALS",
            "GOOGLE_CREDENTIALS"
        ]
    },
    "s3": {
        "required": ["aws_credentials"],
        "optional": [],
        "environment_vars": [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY"
        ]
    }
    # ... other sources
}
```

## Error Handling

For authentication failures:

```python
class AuthenticationError(Exception):
    """Error raised when authentication fails."""

    source_type: str
    missing_credentials: List[str]

    def __init__(self, source_type: str, missing_credentials: List[str]):
        self.source_type = source_type
        self.missing_credentials = missing_credentials
        message = f"Authentication failed for {source_type}. Missing credentials: {', '.join(missing_credentials)}"
        super().__init__(message)
```

## Next Steps

1. Implement the credential provider interface
2. Create basic environment and file providers
3. Build the credential manager
4. Integrate with source types
5. Develop OAuth helpers for common services
6. Add support for secret managers
