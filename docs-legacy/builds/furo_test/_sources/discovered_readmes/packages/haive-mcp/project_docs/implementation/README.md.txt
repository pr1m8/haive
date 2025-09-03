# Implementation Patterns

**Production-ready patterns for implementing dynamic MCP integration**

## 🎯 Overview

This guide provides battle-tested implementation patterns for deploying Haive-MCP in production environments, covering everything from basic setups to enterprise-scale deployments.

## 🏗️ Implementation Architecture

### Production Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Application Layer                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │    Web API      │ │   Background    │ │     Admin       ││
│  │   (FastAPI)     │ │    Workers      │ │   Dashboard     ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Agent Layer                                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   MCPAgent      │ │ IntelligentMCP  │ │ TransferableMCP ││
│  │   (Static)      │ │   (Dynamic)     │ │   (Sharing)     ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                Infrastructure Layer                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │     Redis       │ │   PostgreSQL    │ │   Monitoring    ││
│  │   (Caching)     │ │   (Metadata)    │ │   (Observ.)     ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Basic Implementation

### Simple Production Setup

```python
# production_mcp_agent.py
import asyncio
import logging
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRequest(BaseModel):
    messages: list[dict]
    agent_id: str = "default"

class AgentResponse(BaseModel):
    response: str
    agent_id: str
    tools_used: list[str]

# Global agent storage
agents: Dict[str, MCPAgent] = {}

async def create_production_agent(agent_id: str) -> MCPAgent:
    """Create production-ready MCP agent."""

    # Production configuration
    config = MCPConfig(
        servers={
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "/app/workspace"],
                timeout=30.0,
                retry_attempts=3
            ),
            "postgres": MCPServerConfig(
                name="postgres",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-postgres"],
                env={"DATABASE_URL": "postgresql://user:pass@localhost/prod"},
                timeout=60.0,
                retry_attempts=5
            )
        },
        auto_health_check=True,
        health_check_interval=30.0,
        max_concurrent_connections=10
    )

    # Create agent with production settings
    agent = MCPAgent(
        name=agent_id,
        engine=AugLLMConfig(
            model="gpt-4",
            temperature=0.3,
            max_tokens=2000,
            timeout=120.0
        ),
        mcp_config=config
    )

    await agent.setup()
    logger.info(f"Created production agent: {agent_id}")
    return agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting production MCP service...")

    # Create default agent
    agents["default"] = await create_production_agent("default")

    yield

    # Shutdown
    logger.info("Shutting down production MCP service...")
    for agent in agents.values():
        await agent.cleanup()

# FastAPI application
app = FastAPI(
    title="Production MCP Service",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/chat", response_model=AgentResponse)
async def chat_endpoint(request: AgentRequest):
    """Chat with MCP-enabled agent."""
    try:
        agent = agents.get(request.agent_id)
        if not agent:
            raise HTTPException(status_code=404, f"Agent {request.agent_id} not found")

        # Execute agent
        result = await agent.arun({"messages": request.messages})

        # Extract tools used (implementation dependent)
        tools_used = getattr(agent, 'last_tools_used', [])

        return AgentResponse(
            response=result,
            agent_id=request.agent_id,
            tools_used=tools_used
        )

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    agent_status = {}
    for agent_id, agent in agents.items():
        try:
            status = await agent.mcp_manager.get_all_server_status()
            agent_status[agent_id] = {
                "status": "healthy",
                "servers": status['summary']
            }
        except Exception as e:
            agent_status[agent_id] = {
                "status": "unhealthy",
                "error": str(e)
            }

    return {"agents": agent_status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Install Node.js for MCP servers
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install common MCP servers
RUN npm install -g \
    @modelcontextprotocol/server-filesystem \
    @modelcontextprotocol/server-postgres \
    @modelcontextprotocol/server-brave-search

# Copy application
COPY . .

# Create workspace directory
RUN mkdir -p /app/workspace

EXPOSE 8000

CMD ["python", "production_mcp_agent.py"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  mcp-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/mcp_db
      - REDIS_URL=redis://redis:6379
      - BRAVE_API_KEY=${BRAVE_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./workspace:/app/workspace
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=mcp_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

## 🏢 Enterprise Implementation

### Scalable Multi-Agent System

```python
# enterprise_mcp_system.py
import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from haive.mcp.agents import IntelligentMCPAgent, MCPAgent
from haive.mcp.manager import MCPManager
from haive.core.engine.aug_llm import AugLLMConfig

class AgentType(Enum):
    STATIC = "static"
    INTELLIGENT = "intelligent"
    SPECIALIZED = "specialized"

@dataclass
class AgentConfig:
    agent_id: str
    agent_type: AgentType
    capabilities: List[str]
    max_concurrent_requests: int = 5
    auto_scale: bool = True

class EnterpriseAgentManager:
    """Enterprise-grade agent management with scaling and monitoring."""

    def __init__(self, redis_url: str, db_url: str):
        self.redis_pool = redis.from_url(redis_url)
        self.db_engine = create_async_engine(db_url)
        self.Session = sessionmaker(self.db_engine, class_=AsyncSession)

        self.agents: Dict[str, MCPAgent] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.request_queues: Dict[str, asyncio.Queue] = {}

    async def initialize(self):
        """Initialize the enterprise system."""
        await self._setup_database()
        await self._load_agent_configs()
        await self._start_monitoring()

    async def create_agent(self, config: AgentConfig) -> MCPAgent:
        """Create agent based on configuration."""

        if config.agent_type == AgentType.STATIC:
            agent = await self._create_static_agent(config)
        elif config.agent_type == AgentType.INTELLIGENT:
            agent = await self._create_intelligent_agent(config)
        else:
            agent = await self._create_specialized_agent(config)

        # Setup monitoring
        await self._setup_agent_monitoring(agent, config)

        # Create request queue
        self.request_queues[config.agent_id] = asyncio.Queue(
            maxsize=config.max_concurrent_requests * 2
        )

        # Start agent worker
        asyncio.create_task(self._agent_worker(config.agent_id))

        self.agents[config.agent_id] = agent
        self.agent_configs[config.agent_id] = config

        return agent

    async def _create_intelligent_agent(self, config: AgentConfig) -> IntelligentMCPAgent:
        """Create intelligent agent with dynamic discovery."""

        # Custom approval handler for enterprise
        async def enterprise_approval_handler(request):
            # Log approval request
            await self._log_approval_request(request)

            # Check security policies
            if await self._check_security_policy(request):
                return True

            # Require human approval for high-risk servers
            return await self._request_human_approval(request)

        agent = IntelligentMCPAgent(
            name=config.agent_id,
            engine=AugLLMConfig(
                model="gpt-4-turbo",
                temperature=0.2,
                max_tokens=4000
            ),
            auto_discover=True,
            require_approval=True,
            approval_callback=enterprise_approval_handler,
            approval_timeout=300.0  # 5 minutes
        )

        await agent.setup()
        return agent

    async def _create_specialized_agent(self, config: AgentConfig) -> MCPAgent:
        """Create agent optimized for specific capabilities."""

        # Build MCP config based on capabilities
        mcp_config = await self._build_mcp_config_for_capabilities(config.capabilities)

        agent = MCPAgent(
            name=config.agent_id,
            engine=AugLLMConfig(
                model="gpt-4",
                temperature=0.1  # More deterministic for specialized tasks
            ),
            mcp_config=mcp_config
        )

        await agent.setup()
        return agent

    async def _agent_worker(self, agent_id: str):
        """Worker process for handling agent requests."""
        agent = self.agents[agent_id]
        queue = self.request_queues[agent_id]

        while True:
            try:
                # Get request from queue
                request_data = await queue.get()

                # Process request
                start_time = asyncio.get_event_loop().time()
                result = await agent.arun(request_data['input'])
                duration = asyncio.get_event_loop().time() - start_time

                # Log metrics
                await self._log_request_metrics(agent_id, duration, "success")

                # Send response
                request_data['response_future'].set_result(result)

            except Exception as e:
                # Log error
                await self._log_request_metrics(agent_id, 0, "error", str(e))

                # Send error response
                if 'response_future' in request_data:
                    request_data['response_future'].set_exception(e)

            finally:
                queue.task_done()

    async def execute_request(self, agent_id: str, input_data: dict) -> str:
        """Execute request on specified agent."""

        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")

        queue = self.request_queues[agent_id]

        # Create future for response
        response_future = asyncio.Future()

        # Add to queue
        request_data = {
            'input': input_data,
            'response_future': response_future
        }

        await queue.put(request_data)

        # Wait for response
        return await response_future

    async def scale_agent(self, agent_id: str, scale_factor: float):
        """Scale agent capacity based on demand."""

        config = self.agent_configs[agent_id]
        if not config.auto_scale:
            return

        current_queue_size = self.request_queues[agent_id].qsize()
        max_queue_size = config.max_concurrent_requests * 2

        if current_queue_size > max_queue_size * 0.8:
            # Scale up - create additional agent instances
            await self._scale_up_agent(agent_id)
        elif current_queue_size < max_queue_size * 0.2:
            # Scale down - reduce agent instances
            await self._scale_down_agent(agent_id)

    async def get_system_status(self) -> dict:
        """Get comprehensive system status."""

        status = {
            "agents": {},
            "total_requests": 0,
            "avg_response_time": 0,
            "error_rate": 0
        }

        for agent_id, agent in self.agents.items():
            agent_status = await agent.mcp_manager.get_all_server_status()
            queue_size = self.request_queues[agent_id].qsize()

            status["agents"][agent_id] = {
                "server_status": agent_status,
                "queue_size": queue_size,
                "config": self.agent_configs[agent_id].__dict__
            }

        # Get metrics from Redis
        metrics = await self._get_system_metrics()
        status.update(metrics)

        return status

# Usage example
async def setup_enterprise_system():
    """Setup enterprise MCP system."""

    manager = EnterpriseAgentManager(
        redis_url="redis://localhost:6379",
        db_url="postgresql+asyncpg://user:pass@localhost/enterprise_mcp"
    )

    await manager.initialize()

    # Create different types of agents
    configs = [
        AgentConfig(
            agent_id="research_agent",
            agent_type=AgentType.INTELLIGENT,
            capabilities=["web_search", "document_analysis", "spreadsheet"],
            max_concurrent_requests=10
        ),
        AgentConfig(
            agent_id="data_agent",
            agent_type=AgentType.SPECIALIZED,
            capabilities=["database", "analytics", "visualization"],
            max_concurrent_requests=5
        ),
        AgentConfig(
            agent_id="general_agent",
            agent_type=AgentType.STATIC,
            capabilities=["filesystem", "basic_tools"],
            max_concurrent_requests=20
        )
    ]

    for config in configs:
        await manager.create_agent(config)

    return manager
```

## 🔒 Security Implementation

### Secure MCP Agent with Authentication

```python
# secure_mcp_agent.py
import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

class SecureAgentRequest(BaseModel):
    messages: list[dict]
    agent_id: str = "default"
    capabilities_required: Optional[List[str]] = None

class UserPermissions(BaseModel):
    user_id: str
    allowed_agents: List[str]
    allowed_capabilities: List[str]
    rate_limit: int = 100  # requests per hour

class SecurityManager:
    """Enterprise security manager for MCP agents."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.user_permissions: Dict[str, UserPermissions] = {}
        self.rate_limits: Dict[str, List[datetime]] = {}

    def create_token(self, user_id: str, permissions: UserPermissions) -> str:
        """Create JWT token for user."""
        payload = {
            "user_id": user_id,
            "permissions": permissions.dict(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> UserPermissions:
        """Verify JWT token and return permissions."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return UserPermissions(**payload["permissions"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def check_rate_limit(self, user_id: str, permissions: UserPermissions) -> bool:
        """Check if user is within rate limits."""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)

        # Clean old requests
        if user_id in self.rate_limits:
            self.rate_limits[user_id] = [
                req_time for req_time in self.rate_limits[user_id]
                if req_time > hour_ago
            ]
        else:
            self.rate_limits[user_id] = []

        # Check limit
        if len(self.rate_limits[user_id]) >= permissions.rate_limit:
            return False

        # Add current request
        self.rate_limits[user_id].append(now)
        return True

    def check_permissions(self, permissions: UserPermissions,
                         agent_id: str, capabilities: List[str]) -> bool:
        """Check if user has required permissions."""

        # Check agent access
        if agent_id not in permissions.allowed_agents:
            return False

        # Check capability access
        if capabilities:
            for cap in capabilities:
                if cap not in permissions.allowed_capabilities:
                    return False

        return True

# Security setup
security_manager = SecurityManager("your-secret-key")
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> UserPermissions:
    """Get current user from JWT token."""
    return security_manager.verify_token(credentials.credentials)

# Secure endpoint
@app.post("/secure/chat")
async def secure_chat_endpoint(
    request: SecureAgentRequest,
    current_user: UserPermissions = Depends(get_current_user)
):
    """Secure chat endpoint with authentication and authorization."""

    # Check rate limits
    if not security_manager.check_rate_limit(current_user.user_id, current_user):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Check permissions
    if not security_manager.check_permissions(
        current_user,
        request.agent_id,
        request.capabilities_required or []
    ):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Execute request (same as before)
    agent = agents.get(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")

    result = await agent.arun({"messages": request.messages})

    # Log security event
    await log_security_event(current_user.user_id, request.agent_id, "chat_request")

    return {"response": result, "agent_id": request.agent_id}
```

## 📊 Monitoring Implementation

### Comprehensive Monitoring and Observability

```python
# monitoring.py
import time
import asyncio
from typing import Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import structlog
import prometheus_client
from opentelemetry import trace, metrics

# Structured logging
logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = prometheus_client.Counter('mcp_requests_total', 'Total requests', ['agent_id', 'status'])
REQUEST_DURATION = prometheus_client.Histogram('mcp_request_duration_seconds', 'Request duration', ['agent_id'])
ACTIVE_CONNECTIONS = prometheus_client.Gauge('mcp_active_connections', 'Active MCP connections', ['server_name'])
SERVER_HEALTH = prometheus_client.Gauge('mcp_server_health', 'Server health status', ['server_name'])

# OpenTelemetry
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

@dataclass
class RequestMetrics:
    agent_id: str
    request_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: str = "pending"
    tools_used: List[str] = None
    error_message: Optional[str] = None

class MCPMonitor:
    """Comprehensive monitoring for MCP agents."""

    def __init__(self):
        self.active_requests: Dict[str, RequestMetrics] = {}

    async def start_request(self, agent_id: str, user_id: str, request_data: dict) -> str:
        """Start monitoring a request."""
        request_id = f"{agent_id}_{user_id}_{int(time.time())}"

        metrics = RequestMetrics(
            agent_id=agent_id,
            request_id=request_id,
            user_id=user_id,
            start_time=datetime.utcnow()
        )

        self.active_requests[request_id] = metrics

        # Log start
        logger.info("request_started", **asdict(metrics), request_data=request_data)

        return request_id

    async def end_request(self, request_id: str, status: str,
                         tools_used: List[str] = None, error: str = None):
        """End monitoring a request."""

        if request_id not in self.active_requests:
            return

        metrics = self.active_requests[request_id]
        metrics.end_time = datetime.utcnow()
        metrics.duration = (metrics.end_time - metrics.start_time).total_seconds()
        metrics.status = status
        metrics.tools_used = tools_used or []
        metrics.error_message = error

        # Update Prometheus metrics
        REQUEST_COUNT.labels(agent_id=metrics.agent_id, status=status).inc()
        REQUEST_DURATION.labels(agent_id=metrics.agent_id).observe(metrics.duration)

        # Log completion
        logger.info("request_completed", **asdict(metrics))

        # Clean up
        del self.active_requests[request_id]

    async def monitor_server_health(self, agent: MCPAgent):
        """Monitor MCP server health."""

        while True:
            try:
                status = await agent.mcp_manager.get_all_server_status()

                for server_name, server_status in status['servers'].items():
                    health_value = 1 if server_status['status'] == 'connected' else 0
                    SERVER_HEALTH.labels(server_name=server_name).set(health_value)

                    if server_status['status'] == 'connected':
                        connection_count = server_status.get('active_connections', 0)
                        ACTIVE_CONNECTIONS.labels(server_name=server_name).set(connection_count)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error("health_monitor_error", error=str(e))
                await asyncio.sleep(60)  # Wait longer on error

# Monitored agent wrapper
class MonitoredMCPAgent:
    """MCP agent with comprehensive monitoring."""

    def __init__(self, agent: MCPAgent, monitor: MCPMonitor):
        self.agent = agent
        self.monitor = monitor

        # Start health monitoring
        asyncio.create_task(self.monitor.monitor_server_health(self.agent))

    async def arun(self, input_data: dict, user_id: str = "anonymous") -> str:
        """Execute agent with monitoring."""

        request_id = await self.monitor.start_request(
            self.agent.name, user_id, input_data
        )

        with tracer.start_as_current_span("mcp_agent_execution") as span:
            span.set_attribute("agent.id", self.agent.name)
            span.set_attribute("user.id", user_id)

            try:
                # Execute agent
                result = await self.agent.arun(input_data)

                # Extract tools used (implementation dependent)
                tools_used = getattr(self.agent, 'last_tools_used', [])

                await self.monitor.end_request(request_id, "success", tools_used)

                span.set_attribute("execution.status", "success")
                span.set_attribute("tools.used", tools_used)

                return result

            except Exception as e:
                await self.monitor.end_request(request_id, "error", error=str(e))

                span.set_attribute("execution.status", "error")
                span.set_attribute("error.message", str(e))

                raise

# Usage
monitor = MCPMonitor()
monitored_agent = MonitoredMCPAgent(agent, monitor)
```

## 🔧 Configuration Management

### Environment-based Configuration

```python
# config.py
import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from haive.mcp.config import MCPConfig, MCPServerConfig

class ProductionSettings(BaseSettings):
    """Production configuration settings."""

    # Application settings
    app_name: str = "Haive MCP Service"
    debug: bool = False
    log_level: str = "INFO"

    # Database settings
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")

    # Security settings
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_expiry_hours: int = 24

    # MCP settings
    mcp_timeout: float = 60.0
    mcp_retry_attempts: int = 3
    max_concurrent_connections: int = 10

    # API keys
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    brave_api_key: Optional[str] = Field(None, env="BRAVE_API_KEY")
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")

    class Config:
        env_file = ".env"

def create_mcp_config(settings: ProductionSettings) -> MCPConfig:
    """Create MCP configuration from settings."""

    servers = {}

    # Always include filesystem server
    servers["filesystem"] = MCPServerConfig(
        name="filesystem",
        transport="stdio",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/app/workspace"],
        timeout=settings.mcp_timeout,
        retry_attempts=settings.mcp_retry_attempts
    )

    # Add database server if configured
    if settings.database_url:
        servers["postgres"] = MCPServerConfig(
            name="postgres",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres"],
            env={"DATABASE_URL": settings.database_url},
            timeout=settings.mcp_timeout,
            retry_attempts=settings.mcp_retry_attempts
        )

    # Add search server if API key available
    if settings.brave_api_key:
        servers["brave_search"] = MCPServerConfig(
            name="brave_search",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-brave-search"],
            env={"BRAVE_API_KEY": settings.brave_api_key},
            timeout=settings.mcp_timeout,
            retry_attempts=settings.mcp_retry_attempts
        )

    return MCPConfig(
        servers=servers,
        auto_health_check=True,
        health_check_interval=30.0,
        max_concurrent_connections=settings.max_concurrent_connections
    )
```

## 📋 Best Practices Summary

### 1. Production Deployment

- Use proper logging and monitoring
- Implement health checks and graceful shutdown
- Configure appropriate timeouts and retries
- Use connection pooling for better performance

### 2. Security

- Always authenticate and authorize users
- Implement rate limiting
- Validate all inputs
- Log security events
- Use secure communication channels

### 3. Scalability

- Design for horizontal scaling
- Use async/await throughout
- Implement proper queue management
- Monitor resource usage

### 4. Reliability

- Handle all exceptions gracefully
- Implement circuit breakers
- Use proper retry strategies
- Have fallback mechanisms

### 5. Observability

- Comprehensive logging
- Metrics collection
- Distributed tracing
- Error tracking

---

**Next**: [Examples](../examples/README.md) | [Troubleshooting](troubleshooting.md)
