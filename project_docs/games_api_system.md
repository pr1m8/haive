# Games API System Documentation

## Overview

The Games API System provides a unified interface for all games in haive-games, with automatic game discovery, OpenAPI documentation, and flexible configuration options. The system enables users to:

1. **Discover** all available games automatically
2. **Select** any game and configure AI opponents
3. **Play** games via REST API or WebSocket
4. **Document** APIs with auto-generated OpenAPI specs

## Architecture

### General API (`general_api.py`)

The `GeneralGameAPI` class automatically:
- Scans the `haive.games` package for available games
- Imports game agents and configurations
- Creates endpoints for each game
- Generates OpenAPI documentation

### Key Components

1. **Game Discovery**
   - Scans game directories
   - Imports agent classes
   - Extracts configuration metadata
   - Handles import failures gracefully

2. **Dynamic Endpoint Creation**
   - `/api/games/` - List all games
   - `/api/games/create` - Create any game
   - `/api/games/{game_id}/` - Game-specific endpoints
   - `/ws/games/{game_id}/{thread_id}` - WebSocket connections

3. **Configuration Modes**
   - **Simple**: Specify model strings
   - **Example**: Use predefined configs
   - **Advanced**: Full PlayerAgentConfig
   - **Legacy**: Backward compatibility

## API Endpoints

### List Games
```
GET /api/games/
```
Returns all discovered games with metadata:
- Game name and ID
- Available players
- Example configurations
- Default models
- API endpoints

### Create Game
```
POST /api/games/create
```
Body:
```json
{
  "game_id": "chess",
  "config_mode": "simple",
  "player_models": {
    "player1": "gpt-4",
    "player2": "claude-3-opus"
  },
  "game_settings": {
    "enable_analysis": true,
    "max_moves": 100
  }
}
```

### Game-Specific Endpoints

After creating a game:
- `GET /api/games/{game_id}/{thread_id}` - Get state
- `POST /api/games/{game_id}/{thread_id}/move` - Make move
- `GET /api/games/{game_id}/{thread_id}/ai-move` - AI move
- `WS /ws/games/{game_id}/{thread_id}` - WebSocket

## Configuration Examples

### Simple Mode
```python
{
  "game_id": "chess",
  "config_mode": "simple",
  "player_models": {
    "player1": "gpt-4",
    "player2": "claude-3-opus"
  }
}
```

### Example Mode
```python
{
  "game_id": "tic_tac_toe",
  "config_mode": "example",
  "example_config": "budget"
}
```

### Advanced Mode
```python
{
  "game_id": "connect4",
  "config_mode": "advanced",
  "player_configs": {
    "red_player": {
      "llm_config": "gpt-4",
      "temperature": 0.7,
      "player_name": "Strategic Red"
    },
    "yellow_player": {
      "llm_config": "claude-3-opus",
      "temperature": 0.3,
      "player_name": "Defensive Yellow"
    }
  }
}
```

## Usage

### Basic Setup
```python
from haive.games.api import create_general_game_api

# Create API that discovers all games
app, game_api = create_general_game_api()

# Run with uvicorn
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Custom Configuration
```python
app, game_api = create_general_game_api(
    route_prefix="/games",
    ws_route_prefix="/ws",
    exclude_games=["go", "monopoly"]
)
```

## Game Discovery Process

1. **Package Scanning**
   - Iterates through `haive.games` subdirectories
   - Skips excluded games and private directories

2. **Agent Import**
   - Imports `{game}.agent` module
   - Finds Agent subclass
   - Gets config class

3. **Metadata Extraction**
   - If config extends `BaseGameConfig`:
     - Gets role definitions
     - Lists example configs
     - Extracts player names
   - Falls back to defaults if needed

4. **API Creation**
   - Creates GameAPI instance
   - Registers routes
   - Adds to discovered games

## OpenAPI Documentation

The system automatically generates OpenAPI documentation:

- **Title**: "Haive Games API"
- **Endpoints**: All discovered games
- **Schemas**: Game-specific configurations
- **Examples**: Request/response samples

Access at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc interface
- `/openapi.json` - Raw schema

## Error Handling

- **Game Not Found**: 404 with available games list
- **Invalid Config Mode**: 400 with requirements
- **Import Failures**: Logged, game skipped
- **Missing State Schema**: Game excluded from API

## Extending the System

### Adding a New Game

1. Create game package in `haive.games.{name}`
2. Implement Agent class extending `Agent`
3. Config class should extend `BaseGameConfig`
4. System automatically discovers it!

### Custom Game Mapping

Override player model mapping in `_register_routes`:
```python
if game_id == "your_game":
    config_kwargs["special_model"] = request.player_models.get("player1")
```

## Performance Considerations

- Games are discovered once at startup
- Agent instances cached per thread
- WebSocket connections managed efficiently
- Lazy loading of game modules

## Security

- CORS enabled by default
- Thread IDs prevent cross-game access
- Input validation on all endpoints
- Configurable authentication hooks

## Examples

See `/examples/general_api_example.py` for:
- Complete API setup
- Various configuration modes
- HTTP client usage
- WebSocket connections

## Testing

Test the API:
```bash
# Run the server
python examples/general_api_example.py --serve

# In another terminal
curl http://localhost:8000/api/games/
```

## Future Enhancements

1. **Authentication**: Add user management
2. **Persistence**: Save game history
3. **Tournaments**: Multi-game competitions
4. **Analytics**: Game statistics
5. **Rate Limiting**: API usage controls