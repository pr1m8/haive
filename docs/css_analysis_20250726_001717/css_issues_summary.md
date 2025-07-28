# CSS and Layout Issues Analysis

Generated: 2025-07-26 00:22:19

## Issue Summary


## Detailed Issues by Page

### homepage
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/
Call log:
  - navigating to "http://localhost:8004/", waiting until "networkidle"



### agents_index
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/agents/index.html
Call log:
  - navigating to "http://localhost:8004/agents/index.html", waiting until "networkidle"



### simple_agent
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/agents/simple.html
Call log:
  - navigating to "http://localhost:8004/agents/simple.html", waiting until "networkidle"



### react_agent
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/agents/react.html
Call log:
  - navigating to "http://localhost:8004/agents/react.html", waiting until "networkidle"



### games_index
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/games/index.html
Call log:
  - navigating to "http://localhost:8004/games/index.html", waiting until "networkidle"



### gallery
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/gallery.html
Call log:
  - navigating to "http://localhost:8004/gallery.html", waiting until "networkidle"



### api_index
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/api/index.html
Call log:
  - navigating to "http://localhost:8004/api/index.html", waiting until "networkidle"



### api_agents
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/api/haive.agents.html
Call log:
  - navigating to "http://localhost:8004/api/haive.agents.html", waiting until "networkidle"



### api_core
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/api/haive.core.html
Call log:
  - navigating to "http://localhost:8004/api/haive.core.html", waiting until "networkidle"



### examples
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/examples/index.html
Call log:
  - navigating to "http://localhost:8004/examples/index.html", waiting until "networkidle"



### getting_started
❌ Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8004/getting_started.html
Call log:
  - navigating to "http://localhost:8004/getting_started.html", waiting until "networkidle"



## Common Problems Found

1. **Content pushed to the right**: Main content area has excessive left margin
2. **Code blocks too narrow**: Code blocks not using full content width
3. **Sidebar too wide**: Sidebar taking up too much horizontal space
4. **CSS conflicts**: Multiple theme files may be conflicting
