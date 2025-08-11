haive-dataflow
==============

Data streaming and API services for the Haive framework.

Overview
--------

The ``haive-dataflow`` package provides production-ready data streaming and API infrastructure:

- **REST API Framework** - FastAPI-based REST endpoints for agents and tools
- **WebSocket Support** - Real-time streaming for conversations and games
- **Authentication & Auth** - Supabase integration with credit system
- **Model Registry** - Dynamic model discovery and management
- **Persistence Layer** - Conversation and state persistence
- **MCP Integration** - Model Context Protocol client support

Installation
------------

.. code-block:: bash

   pip install haive-dataflow

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.dataflow.api import create_app
   from haive.dataflow.config import Settings
   
   # Create FastAPI app
   settings = Settings()
   app = create_app(settings)
   
   # Run with uvicorn
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)

Core Components
---------------

API Framework
^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: FastAPI App
      :link: ../api/dataflow/api/app/index
      :link-type: doc

      Main API application
      
      - Auto-generated docs
      - Request validation
      - Error handling
      - CORS support

   .. grid-item-card:: Game API
      :link: ../api/dataflow/api/game_api/index
      :link-type: doc

      Game-specific endpoints
      
      - WebSocket games
      - Move validation
      - State streaming
      - Multiplayer support

Authentication
^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Supabase Auth
      :link: ../api/dataflow/auth/supabase/index
      :link-type: doc

      Authentication system
      
      - JWT tokens
      - User management
      - Role-based access
      - Session handling

   .. grid-item-card:: Credits System
      :link: ../api/dataflow/auth/credits/index
      :link-type: doc

      Usage credits
      
      - Credit tracking
      - Usage limits
      - Billing integration
      - Rate limiting

Data Management
^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Persistence
      :link: ../api/dataflow/persistence/index
      :link-type: doc

      Data persistence
      
      - Conversation storage
      - State snapshots
      - History tracking
      - Backup/restore

   .. grid-item-card:: Model Registry
      :link: ../api/dataflow/registries/model_registry/index
      :link-type: doc

      Model management
      
      - Auto-discovery
      - Version tracking
      - Provider routing
      - Cost tracking

Core Classes
------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.api.app.create_app
   haive.dataflow.config.settings.Settings
   haive.dataflow.auth.supabase.SupabaseAuth
   haive.dataflow.registries.model_registry.ModelRegistry

API Components
--------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.api.base.BaseRouter
   haive.dataflow.api.game_api.GameAPI
   haive.dataflow.api.routes.agent_routes.AgentRouter
   haive.dataflow.api.routes.conversation_routes.ConversationRouter
   haive.dataflow.api.routes.llm_routes.LLMRouter

WebSocket Handlers
------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.internal_websockets.manager.WebSocketManager
   haive.dataflow.internal_websockets.handlers.MessageHandler
   haive.dataflow.api.game_socket.GameWebSocket

Authentication & Middleware
---------------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.auth.dependencies.get_current_user
   haive.dataflow.auth.middleware.AuthMiddleware
   haive.dataflow.api.middleware.logging.LoggingMiddleware
   haive.dataflow.api.middleware.rate_limit.RateLimitMiddleware

Data Models
-----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.models.ConversationCreate
   haive.dataflow.models.MessageCreate
   haive.dataflow.models.AgentRequest
   haive.dataflow.models.GameState

Persistence & Storage
---------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.dataflow.persistence.conversations.ConversationStore
   haive.dataflow.persistence.supabase_adapter.SupabaseAdapter
   haive.dataflow.db.supabase.SupabaseClient

Complete API Reference
----------------------

For the complete API documentation with all dataflow components:

.. toctree::
   :maxdepth: 3

   ../api/dataflow/index

Examples
--------

Basic API Server
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.api import create_app
   from haive.dataflow.config import Settings
   
   # Configure settings
   settings = Settings(
       app_name="Haive API",
       supabase_url="https://your-project.supabase.co",
       supabase_key="your-anon-key",
       enable_cors=True
   )
   
   # Create app
   app = create_app(settings)
   
   # Add custom route
   @app.get("/health")
   async def health_check():
       return {"status": "healthy"}

Agent API Endpoint
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.api.routes.agent_routes import router
   from haive.agents.simple.agent import SimpleAgent
   
   # Register agent endpoint
   @router.post("/agents/simple")
   async def run_simple_agent(request: AgentRequest):
       agent = SimpleAgent(
           name=request.agent_name,
           engine=request.engine_config
       )
       
       result = await agent.arun(request.input)
       
       return {
           "agent": request.agent_name,
           "result": result,
           "tokens_used": agent.token_count
       }

WebSocket Game Server
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.api.game_socket import GameWebSocket
   from haive.games.chess.agent import ChessAgent
   
   @app.websocket("/ws/chess/{game_id}")
   async def chess_game(websocket: WebSocket, game_id: str):
       await websocket.accept()
       
       # Create game handler
       handler = GameWebSocket(
           websocket=websocket,
           game_agent=ChessAgent(),
           game_id=game_id
       )
       
       # Handle game loop
       await handler.game_loop()

Authenticated Endpoints
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.auth.dependencies import get_current_user
   from fastapi import Depends
   
   @app.get("/protected/data")
   async def get_protected_data(
       current_user: User = Depends(get_current_user)
   ):
       return {
           "user_id": current_user.id,
           "data": "This is protected data"
       }

Model Registry Usage
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.registries.model_registry import ModelRegistry
   
   # Initialize registry
   registry = ModelRegistry()
   
   # Discover available models
   models = await registry.discover_models()
   
   # Get model info
   gpt4_info = registry.get_model("gpt-4")
   print(f"Cost per 1k tokens: ${gpt4_info.cost_per_1k}")

Conversation Persistence
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.dataflow.persistence.conversations import ConversationStore
   
   # Create store
   store = ConversationStore()
   
   # Save conversation
   conversation_id = await store.create_conversation(
       user_id="user123",
       agent_name="assistant",
       initial_message="Hello!"
   )
   
   # Add messages
   await store.add_message(
       conversation_id=conversation_id,
       role="assistant",
       content="Hello! How can I help you?"
   )
   
   # Retrieve history
   history = await store.get_conversation(conversation_id)

Best Practices
--------------

1. **Use environment variables** for configuration
2. **Implement proper error handling** for all endpoints
3. **Add request validation** using Pydantic models
4. **Use dependency injection** for shared resources
5. **Implement rate limiting** for public endpoints
6. **Monitor WebSocket connections** for cleanup

Deployment Guidelines
---------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Component
     - Recommendation
   * - **Web Server**
     - Use Uvicorn with Gunicorn for production
   * - **Database**
     - PostgreSQL via Supabase or direct
   * - **Caching**
     - Redis for session and result caching
   * - **Monitoring**
     - Prometheus + Grafana for metrics
   * - **Logging**
     - Structured JSON logs to centralized system

Configuration
-------------

Environment variables for haive-dataflow:

- ``SUPABASE_URL`` - Supabase project URL
- ``SUPABASE_KEY`` - Supabase anonymous key
- ``DATABASE_URL`` - PostgreSQL connection string
- ``REDIS_URL`` - Redis connection for caching
- ``LOG_LEVEL`` - Logging level (INFO, DEBUG, etc.)
- ``CORS_ORIGINS`` - Allowed CORS origins
- ``MAX_CONNECTIONS`` - WebSocket connection limit

Related Documentation
---------------------

- :doc:`../guide/api` - API development guide
- :doc:`../api/dataflow/index` - Complete dataflow API reference
- :doc:`haive-agents` - Agent implementations
- :doc:`../deployment` - Deployment guide