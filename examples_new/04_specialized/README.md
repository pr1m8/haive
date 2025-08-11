# Specialized Examples

Domain-specific applications showcasing Haive's capabilities across different fields and use cases. These examples demonstrate real-world applications and advanced patterns.

## Purpose

Explore how Haive agents solve real-world problems in specific domains. Each subdirectory focuses on a particular application area with production-ready patterns and best practices.

## Prerequisites

- Strong understanding of single and multi-agent patterns
- Familiarity with domain-specific concepts in areas of interest
- Experience with relevant Python libraries (varies by domain)
- Understanding of async programming patterns

## Domains

### 🔍 [RAG (Retrieval-Augmented Generation)](rag/)

**Knowledge-enhanced AI systems**

- Document processing and indexing
- Vector databases and embeddings
- Multi-source information synthesis
- Question-answering systems
- **Skill Level**: Intermediate to Advanced
- **Use Cases**: Knowledge bases, document analysis, research assistance

### 🎯 [Planning and Reasoning](planning/)

**Complex task planning and execution**

- Goal decomposition and planning
- Resource allocation and scheduling
- Constraint satisfaction
- Dynamic re-planning
- **Skill Level**: Advanced
- **Use Cases**: Project management, logistics, automated planning

### 🎮 [Games and Simulations](games/)

**Interactive environments and gaming**

- Game-playing agents
- Multi-agent simulations
- Environment interaction
- Strategy development
- **Skill Level**: Intermediate to Advanced
- **Use Cases**: Game AI, simulations, testing environments

### 🏢 [Business Applications](business/)

**Enterprise and business workflows**

- Customer service automation
- Data analysis and reporting
- Process automation
- Decision support systems
- **Skill Level**: Intermediate
- **Use Cases**: CRM, analytics, workflow automation

### 🧪 [Research and Analysis](research/)

**Scientific and analytical applications**

- Literature review and synthesis
- Data collection and analysis
- Hypothesis generation
- Experimental design
- **Skill Level**: Advanced
- **Use Cases**: Academic research, market analysis, scientific computing

### 🎨 [Creative Applications](creative/)

**Content creation and artistic tasks**

- Writing and storytelling
- Image and media generation
- Creative collaboration
- Style transfer and adaptation
- **Skill Level**: Beginner to Intermediate
- **Use Cases**: Content marketing, creative writing, design assistance

## Quick Start by Domain

### For Knowledge Work (RAG)

```bash
poetry run python examples_new/04_specialized/rag/simple_rag.py
```

### For Planning Tasks

```bash
poetry run python examples_new/04_specialized/planning/task_planner.py
```

### For Interactive Systems

```bash
poetry run python examples_new/04_specialized/games/simple_game.py
```

### For Business Applications

```bash
poetry run python examples_new/04_specialized/business/customer_support.py
```

## Common Patterns Across Domains

### Domain-Specific Agent Configuration

```python
# Each domain has optimized configurations
rag_config = AugLLMConfig(
    temperature=0.2,  # Lower for factual accuracy
    system_message="You are a knowledgeable research assistant."
)

creative_config = AugLLMConfig(
    temperature=0.8,  # Higher for creativity
    system_message="You are a creative writing assistant."
)
```

### Specialized Tool Integration

```python
# Domain-specific tools
rag_agent = ReactAgent(
    name="researcher",
    engine=rag_config,
    tools=[vector_search, document_loader, citation_formatter]
)

planning_agent = ReactAgent(
    name="planner",
    engine=planning_config,
    tools=[calendar_integration, resource_checker, constraint_validator]
)
```

### Multi-Agent Domain Workflows

```python
# Domain-specific agent coordination
research_pipeline = EnhancedMultiAgentV4([
    DocumentCollectorAgent(),
    AnalysisAgent(),
    SynthesisAgent(),
    ReportGeneratorAgent()
], mode="sequential")
```

## Cross-Domain Integration

### Combining Domains

Many real applications combine multiple domains:

```python
# Business intelligence system combining multiple domains
bi_system = BusinessIntelligenceWorkflow([
    DataCollectorAgent(),      # Research domain
    AnalysisAgent(),          # Research domain
    PlanningAgent(),          # Planning domain
    ReportAgent(),            # Business domain
    CustomerNotificationAgent() # Business domain
])
```

### Shared Components

- **State Management**: Common state patterns across domains
- **Error Handling**: Domain-agnostic error recovery
- **Monitoring**: Cross-domain performance tracking
- **Authentication**: Unified auth for domain-specific APIs

## Performance by Domain

### RAG Systems

- **Bottleneck**: Vector similarity search
- **Optimization**: Efficient embedding models, index tuning
- **Caching**: Document embeddings, frequently accessed content

### Planning Systems

- **Bottleneck**: Constraint solving, search space
- **Optimization**: Heuristic search, pruning strategies
- **Caching**: Computed plans, constraint evaluations

### Game Systems

- **Bottleneck**: Real-time decision making
- **Optimization**: Fast inference models, action caching
- **Scaling**: Parallel game simulations

### Business Systems

- **Bottleneck**: External API calls, data processing
- **Optimization**: Async operations, connection pooling
- **Reliability**: Retry logic, graceful degradation

## Selecting the Right Domain

### Questions to Consider

1. **What type of problem are you solving?**
   - Information retrieval → RAG
   - Task planning → Planning
   - Interactive systems → Games
   - Business processes → Business

2. **What are your accuracy requirements?**
   - High accuracy → RAG, Business
   - Creative flexibility → Creative
   - Strategic thinking → Planning

3. **What's your integration complexity?**
   - External data sources → RAG, Research
   - Business systems → Business
   - Real-time interaction → Games

4. **What's your performance requirement?**
   - Real-time → Games, Business (simplified)
   - Batch processing → Research, RAG
   - Interactive → All domains

## Development Workflow

### 1. Choose Domain

Start with the domain closest to your use case

### 2. Study Examples

Review examples in your chosen domain subdirectory

### 3. Adapt Patterns

Modify examples for your specific requirements

### 4. Integrate Components

Combine with other domains if needed

### 5. Test and Optimize

Use domain-specific testing and optimization strategies

## Next Steps

1. **Choose Your Domain**: Pick the subdirectory most relevant to your use case
2. **Follow Domain README**: Each subdirectory has detailed guidance
3. **Combine Patterns**: Mix and match across domains as needed
4. **Scale Up**: Move to [Advanced Examples](../05_advanced/) for custom architectures

## Resources

### General

- [Architecture Patterns](../../docs/architecture/)
- [Performance Optimization](../../docs/guides/performance.md)
- [Production Deployment](../../docs/guides/deployment.md)

### Domain-Specific

- Each subdirectory contains domain-specific resources and references
- External libraries and APIs documentation
- Academic papers and research (where applicable)

## Getting Help

- **General Issues**: Check [main documentation](../../README.md)
- **Domain-Specific**: See individual domain README files
- **Performance**: [Performance guide](../../docs/guides/performance.md)
- **Integration**: [Integration patterns](../../docs/patterns/)
