# Haive Agents - Agent Architecture Library

## Overview

Haive Agents provides 50+ reusable agent architectures and patterns for building intelligent AI systems. These are general-purpose architectural patterns that can be adapted to any domain or use case.

## Agent Categories

### 1. RAG (Retrieval Augmented Generation) Agents

**What they do**: Combine document retrieval with generation for accurate, grounded responses.

- **Agentic RAG**: Makes intelligent decisions about when and how to retrieve
- **Dynamic RAG**: Adapts retrieval strategy based on query complexity
- **Self-Correcting RAG**: Validates retrieved info and self-corrects errors
- **Multi-Strategy RAG**: Combines multiple retrieval approaches
- **HYDE RAG**: Generates hypothetical documents to improve retrieval
- **Filtered RAG**: Advanced filtering based on metadata and relevance
- **DB RAG**: Specialized for structured data (SQL, GraphDB)
- **Typed RAG**: Enforces type safety on inputs and outputs

**Example Use:**

```python
from haive.agents.rag import DynamicRAG

agent = DynamicRAG(vector_store=my_store)
response = agent.invoke("What are the Q3 financial results?")
```

### 2. Reasoning & Critique Agents

**What they do**: Advanced reasoning with self-evaluation and improvement.

- **LATS (Language Agent Tree Search)**: Explores reasoning trees
- **MCTS (Monte Carlo Tree Search)**: Probabilistic decision making
- **Reflection**: Self-evaluates and improves responses
- **Reflexion**: Iterative improvement through self-reflection
- **Self-Discover**: Discovers own capabilities and limitations
- **Tree of Thoughts (ToT)**: Explores multiple reasoning paths

**Example Use:**

```python
from haive.agents.reasoning import TreeOfThoughts

agent = TreeOfThoughts(max_thoughts=5)
solution = agent.solve("Design a sustainable city")
```

### 3. Planning & Execution Agents

**What they do**: Break down complex tasks and execute them systematically.

- **Plan and Execute**: Creates and executes step-by-step plans
- **LLM Compiler**: Optimizes execution order for efficiency
- **ReWoo**: Reduces API calls through smart planning
- **Task Analysis**: Analyzes complexity before execution

**Example Use:**

```python
from haive.agents.planning import PlanAndExecute

agent = PlanAndExecute(tools=[calculator, web_search])
result = agent.run("Research and calculate ROI for solar panels")
```

### 4. Conversation & Collaboration Agents

**What they do**: Handle complex conversational scenarios and multi-agent coordination.

- **Collaborative**: Multiple agents working together
- **Debate**: Agents debate to reach better conclusions
- **Directed**: Goal-oriented conversation management
- **Round Robin**: Turn-based multi-agent discussion
- **Social Media**: Optimized for platform-specific interactions

**Example Use:**

```python
from haive.agents.conversation import DebateAgent

pro = DebateAgent(stance="pro")
con = DebateAgent(stance="con")
moderator = DebateAgent(role="moderator")

conclusion = moderator.moderate_debate(pro, con, topic="AI regulation")
```

### 5. Document Processing Agents

**What they do**: Extract, transform, and analyze documents intelligently.

- **Knowledge Graph Builders**: Extract entities and relationships
- **Iterative Refinement**: Progressively improve extraction quality
- **Map-Merge**: Parallel processing with intelligent merging
- **Complex Extraction**: Handle nested and complex structures
- **Summarizers**: Multi-level summarization strategies
- **TNT (Transform and Tag)**: Document transformation pipeline

**Example Use:**

```python
from haive.agents.document_modifiers import KnowledgeGraphBuilder

agent = KnowledgeGraphBuilder()
kg = agent.process("research_paper.pdf")
# Returns structured knowledge graph
```

### 6. Research & Analysis Agents

**What they do**: Conduct deep research and analysis on topics.

- **Storm**: Systematic topic research and report generation
- **Open Perplexity**: Open-source research assistant
- **Person Researcher**: Deep research on individuals
- **Wiki Writer**: Creates Wikipedia-style articles
- **Interview Agent**: Conducts and analyzes interviews

**Example Use:**

```python
from haive.agents.research import StormAgent

agent = StormAgent()
report = agent.research("quantum computing applications in medicine")
# Returns comprehensive research report
```

### 7. ReAct Agents

**What they do**: Reason and Act - combine reasoning with tool use.

- **ReAct v1/v2/v3**: Different implementations with improvements
- **ReAct Many Tools**: Optimized for 10+ tools
- **ReAct Class**: Object-oriented implementation

**Example Use:**

```python
from haive.agents.react import ReactV3

agent = ReactV3(tools=[search, calculator, database])
result = agent.solve("Find the market cap of the top 5 tech companies")
```

### 8. Specialized Agents

**What they do**: Unique capabilities for specific use cases.

- **Long-Term Memory**: Maintains context across sessions
- **Dynamic Supervisor**: Orchestrates other agents dynamically
- **Sequential**: Step-by-step execution with dependencies
- **Self-Healing Code**: Automatically fixes code errors
- **Simple Agent**: Basic single-purpose agents

## Common Patterns

### Agent Composition

```python
# Combine multiple agents
researcher = ResearchAgent()
writer = WriterAgent()
critic = CriticAgent()

# Chain them together
research = researcher.investigate(topic)
draft = writer.write(research)
final = critic.review_and_improve(draft)
```

### Dynamic Configuration

```python
# Adjust agent behavior at runtime
agent = DynamicRAG()
agent.set_retrieval_strategy("multi_query")
agent.set_temperature(0.2)  # More focused
```

### State Persistence

```python
# Save and restore agent state
agent = LongTermMemoryAgent()
conversation = agent.chat("Tell me about Paris")

# Save state
state = agent.save_state()

# Restore later
restored_agent = LongTermMemoryAgent.from_state(state)
```

## Best Practices

1. **Choose the Right Agent**: Match agent capabilities to your use case
2. **Extend Don't Replace**: Build on existing agents rather than starting from scratch
3. **Configure Appropriately**: Adjust parameters for your specific needs
4. **Monitor Performance**: Use built-in metrics and logging
5. **Test Thoroughly**: Each agent includes test suites - use them!

## Persistence & Configuration

### Supabase Integration

All Haive agents automatically integrate with Supabase for conversation persistence and state management.

**Quick Setup:**

1. Set your Supabase connection string:

   ```bash
   export POSTGRES_CONNECTION_STRING="postgresql://postgres.{project}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres"
   ```

2. Agents automatically detect and use Supabase:

   ```python
   from haive.agents.simple.agent import SimpleAgent

   agent = SimpleAgent(name="My Agent")

   # Conversations are automatically persisted to Supabase
   result = agent.run(
       {'messages': [HumanMessage(content="Hello!")]},
       config={'configurable': {'thread_id': 'conversation-1'}}
   )
   ```

**Features:**

- ✅ **Automatic Configuration**: Detects Supabase connection from environment
- ✅ **Conversation Persistence**: All agent interactions saved automatically
- ✅ **Resume Conversations**: Continue from any point using thread IDs
- ✅ **State Management**: Full conversation state preserved across sessions
- ✅ **Recursion Limits**: Configurable limits (default: 100) for agent safety

**Verification:**

```python
# Check if agent is using Supabase
if hasattr(agent, 'persistence') and agent.persistence:
    if "supabase.com" in agent.persistence.connection_string:
        print("✅ Using Supabase for persistence!")
```

### Configuration Options

**Environment Variables:**

- `POSTGRES_CONNECTION_STRING`: Supabase connection string (auto-detected)
- `HAIVE_RECURSION_LIMIT`: Override default recursion limit

**Runtime Configuration:**

```python
# Custom thread IDs for conversation management
config = {
    'configurable': {
        'thread_id': f'user-{user_id}-session-{session_id}',
        'recursion_limit': 150  # Override default
    }
}

result = agent.run(messages, config=config)
```

## Advanced Features

- **Modular Design**: Mix and match components
- **Tool Integration**: Add any tool to any agent
- **Custom Prompts**: Override default prompts
- **State Management**: Full control over agent state with Supabase persistence
- **Parallel Execution**: Many agents support concurrent operations
- **Conversation Continuity**: Resume any conversation from exact state

## Troubleshooting

### Common Issues

**Prepared Statement Errors:**

- Error: `prepared statement "_pg3_X" already exists`
- **Impact**: ⚠️ Does NOT prevent data persistence
- **Solution**: These errors can be safely ignored - conversations are still saved

**Missing Persistence:**

- **Cause**: `POSTGRES_CONNECTION_STRING` not set
- **Solution**: Set environment variable with your Supabase connection string

For detailed troubleshooting, see: [Supabase Integration Guide](../../project_docs/SUPABASE_INTEGRATION.md)

_Note: Detailed API documentation for each agent coming soon. Each agent is production-tested and includes examples._
