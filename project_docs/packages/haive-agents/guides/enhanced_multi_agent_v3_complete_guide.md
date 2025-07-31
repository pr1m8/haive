# Enhanced MultiAgent V3 - Complete Usage Guide

**Version**: 1.0  
**Created**: 2025-07-21  
**Status**: Production Ready  

## 🎯 Overview

Enhanced MultiAgent V3 is the most advanced multi-agent coordination system in Haive, providing type-safe, performance-optimized, and highly observable multi-agent workflows. This guide covers everything you need to know to build, configure, and deploy production multi-agent systems.

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Installation & Setup](#installation--setup)
4. [Building Your First MultiAgent](#building-your-first-multiagent)
5. [Execution Patterns](#execution-patterns)
6. [Advanced Configuration](#advanced-configuration)
7. [Performance & Monitoring](#performance--monitoring)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## 🚀 Quick Start

### Installation

```bash
# Ensure you're in the haive project
cd /path/to/haive/backend/haive

# Install with enhanced agents
poetry install --all-extras

# Verify installation
poetry run python -c "from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent; print('✅ Ready')"
```

### Your First MultiAgent (30 seconds)

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

# Create specialized agents
analyzer = EnhancedSimpleAgent(
    name="analyzer",
    temperature=0.3,
    system_message="You analyze data and provide insights."
)
summarizer = EnhancedSimpleAgent(
    name="summarizer", 
    temperature=0.7,
    system_message="You create concise summaries."
)

# Create multi-agent workflow
workflow = EnhancedMultiAgent(
    name="analysis_pipeline",
    agents=[analyzer, summarizer],
    execution_mode="sequential"
)

# Execute
compiled = workflow.compile()
result = compiled.invoke({
    "messages": [{"role": "user", "content": "Analyze Q3 sales data"}]
})

print(f"Result: {result['messages'][-1].content}")
```

## 🏗️ Architecture Overview

### Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                  Enhanced MultiAgent V3                     │
├─────────────────────────────────────────────────────────────┤
│  Generic Typing: EnhancedMultiAgent[AgentsT]               │
│  - AgentsT: Dict[str, Agent] | List[Agent]                 │
│  - Full type safety throughout                             │
├─────────────────────────────────────────────────────────────┤
│  Execution Patterns:                                       │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐ │
│  │ Sequential  │ Parallel    │ Conditional │ Branch      │ │
│  │ A → B → C   │ A ∥ B ∥ C   │ A → B|C|D   │ A→(B∥C)→D   │ │
│  └─────────────┴─────────────┴─────────────┴─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Enhanced Features:                                        │
│  • Performance tracking with adaptive routing             │
│  • Rich debugging and observability                       │
│  • Multi-engine coordination                              │
│  • Advanced routing algorithms                            │
│  • Comprehensive state management                         │
└─────────────────────────────────────────────────────────────┘
```

### State Management

```python
# Enhanced state automatically chosen based on features enabled
if any([performance_mode, debug_mode, advanced_routing]):
    state_schema = EnhancedMultiAgentState  # Rich tracking
else:
    state_schema = MultiAgentState  # Basic compatibility
```

## 🔧 Installation & Setup

### Prerequisites

```bash
# Check Python version (3.9+)
python --version

# Verify poetry installation
poetry --version

# Install Haive with all dependencies
poetry install --all-extras
```

### Import Setup

```python
# Core imports
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent
from haive.core.schema.prebuilt.enhanced_multi_agent_state import EnhancedMultiAgentState

# For typing
from typing import Dict, List
```

## 🛠️ Building Your First MultiAgent

### Step 1: Create Individual Agents

```python
# Specialized agents with different roles
researcher = EnhancedSimpleAgent(
    name="researcher",
    temperature=0.3,  # Lower temperature for factual research
    system_message="You are a thorough researcher who gathers comprehensive information on topics."
)

analyzer = EnhancedSimpleAgent(
    name="analyzer",
    temperature=0.5,  # Balanced for analysis
    system_message="You analyze information and identify key insights and patterns."
)

writer = EnhancedSimpleAgent(
    name="writer",
    temperature=0.8,  # Higher temperature for creativity
    system_message="You write clear, engaging content based on research and analysis."
)
```

### Step 2: Choose Your MultiAgent Pattern

#### Option A: Simple List (Sequential by default)
```python
content_team = EnhancedMultiAgent(
    name="content_creation_team",
    agents=[researcher, analyzer, writer]  # Will execute in order
)
```

#### Option B: Named Dictionary (Flexible routing)
```python
content_team = EnhancedMultiAgent(
    name="content_creation_team",
    agents={
        "researcher": researcher,
        "analyzer": analyzer, 
        "writer": writer
    },
    execution_mode="sequential"  # Can change to parallel, conditional, etc.
)
```

### Step 3: Add Enhanced Features

```python
advanced_team = EnhancedMultiAgent(
    name="advanced_content_team",
    agents={"researcher": researcher, "analyzer": analyzer, "writer": writer},
    
    # Enhanced features
    performance_mode=True,      # Track and optimize performance
    debug_mode=True,           # Rich debugging information
    multi_engine_mode=True,    # Different engines per agent
    advanced_routing=True,     # Sophisticated routing
    
    # Performance tuning
    adaptation_rate=0.2,       # How quickly to adapt (0.0-1.0)
    
    # Execution configuration
    execution_mode="sequential",
    entry_point="researcher"   # Start with researcher
)
```

### Step 4: Compile and Execute

```python
# Compile the workflow
compiled_team = advanced_team.compile()

# Execute with input
result = compiled_team.invoke({
    "messages": [
        {
            "role": "user", 
            "content": "Create a comprehensive article about the future of AI in healthcare"
        }
    ]
})

# Access results
final_content = result["messages"][-1].content
print(f"Generated content: {final_content}")
```

## 🔄 Execution Patterns

### 1. Sequential Execution (Pipeline)

**When to use**: Data processing pipelines, content creation workflows

```python
# A → B → C flow
pipeline = EnhancedMultiAgent(
    name="data_pipeline",
    agents=[preprocessor, analyzer, formatter],
    execution_mode="sequential"
)

# Each agent receives output from previous agent
result = compiled_pipeline.invoke({
    "messages": [{"role": "user", "content": "Process this dataset"}]
})
```

**Flow**: User Input → Preprocessor → Analyzer → Formatter → Final Result

### 2. Parallel Execution (Expert Panel)

**When to use**: Multi-perspective analysis, concurrent processing

```python
# A ∥ B ∥ C execution
expert_panel = EnhancedMultiAgent(
    name="expert_panel",
    agents=[tech_expert, business_expert, legal_expert],
    execution_mode="parallel"
)

# All agents process the same input simultaneously
result = compiled_panel.invoke({
    "messages": [{"role": "user", "content": "Evaluate this business proposal"}]
})
```

**Flow**: User Input → (Tech Expert ∥ Business Expert ∥ Legal Expert) → Combined Result

### 3. Conditional Execution (Smart Routing)

**When to use**: Customer service routing, request classification

```python
# Dynamic routing based on content
smart_router = EnhancedMultiAgent(
    name="customer_service",
    agents=[classifier, billing_agent, technical_agent, general_agent],
    entry_point="classifier",
    execution_mode="conditional",
    advanced_routing=True
)

# Add routing logic
def route_customer_request(state):
    content = str(state["messages"][-1].content).lower()
    if "billing" in content or "payment" in content:
        return "billing_agent"
    elif "technical" in content or "bug" in content:
        return "technical_agent"
    else:
        return "general_agent"

smart_router.add_conditional_routing(
    "classifier", 
    route_customer_request,
    {
        "billing_agent": "billing_agent",
        "technical_agent": "technical_agent", 
        "general_agent": "general_agent"
    }
)
```

**Flow**: User Input → Classifier → (Billing Agent | Technical Agent | General Agent)

### 4. Branch Execution (Complex Workflows)

**When to use**: Document processing, multi-stage validation

```python
# Complex workflow: A → (B ∥ C) → D
document_processor = EnhancedMultiAgent(
    name="document_processor",
    agents=[validator, ocr_processor, nlp_processor, aggregator],
    entry_point="validator",
    execution_mode="branch",
    advanced_routing=True
)

# Configure complex routing
document_processor.add_edge("validator", "ocr_processor")
document_processor.add_parallel_group(
    ["ocr_processor", "nlp_processor"], 
    next_agent="aggregator"
)
```

**Flow**: Document → Validator → (OCR Processor ∥ NLP Processor) → Aggregator → Final Result

## ⚙️ Advanced Configuration

### Performance Tracking

```python
adaptive_system = EnhancedMultiAgent(
    name="adaptive_workflow",
    agents={"fast": fast_agent, "accurate": slow_agent, "balanced": balanced_agent},
    performance_mode=True,
    adaptation_rate=0.3,  # How quickly to adapt to performance changes
)

# System automatically tracks:
# - Success rates per agent
# - Average execution duration
# - Efficiency scores (success_rate / duration)
# - Task counts

# Manual performance updates
adaptive_system.update_performance("fast", success=True, duration=0.5)
adaptive_system.update_performance("accurate", success=True, duration=2.0)

# Get best performer
best_agent = adaptive_system.get_best_agent_for_task()
print(f"Best performing agent: {best_agent}")

# Analyze performance
analysis = adaptive_system.analyze_agent_performance()
for agent_name, metrics in analysis["agents"].items():
    print(f"{agent_name}: {metrics['efficiency_score']} efficiency")
```

### Rich Debugging

```python
debug_workflow = EnhancedMultiAgent(
    name="debug_example",
    agents=[agent1, agent2, agent3],
    debug_mode=True,  # Enables comprehensive logging
    performance_mode=True
)

# Display all capabilities
debug_workflow.display_capabilities()

# Get detailed summary
summary = debug_workflow.get_capabilities_summary()
print(f"Features enabled: {summary['features']}")
print(f"Performance tracking: {summary['features']['has_performance_tracking']}")
```

### Multi-Engine Coordination

```python
multi_engine_team = EnhancedMultiAgent(
    name="diverse_team",
    agents={
        "creative": creative_agent,      # High temperature engine
        "analytical": analytical_agent,  # Low temperature engine
        "coordinator": coordinator_agent # Medium temperature engine
    },
    multi_engine_mode=True,
    advanced_routing=True
)

# Each agent can use different engine configurations
# Coordinator agent manages overall workflow decisions
```

### Custom Routing Patterns

```python
# Advanced conditional routing
def intelligent_router(state):
    """Custom routing logic based on multiple factors."""
    content = state["messages"][-1].content
    context = state.get("shared_context", {})
    
    # Route based on content complexity
    word_count = len(content.split())
    if word_count > 100:
        return "detailed_processor"
    elif any(keyword in content.lower() for keyword in ["urgent", "asap", "immediate"]):
        return "fast_processor" 
    else:
        return "standard_processor"

complex_router = EnhancedMultiAgent(
    name="intelligent_router",
    agents={"classifier": classifier, "detailed": detailed_agent, "fast": fast_agent, "standard": standard_agent},
    entry_point="classifier",
    advanced_routing=True
)

complex_router.add_conditional_routing(
    "classifier",
    intelligent_router,
    {
        "detailed_processor": "detailed",
        "fast_processor": "fast", 
        "standard_processor": "standard"
    }
)
```

## 📊 Performance & Monitoring

### Performance Metrics

Each agent automatically tracks:

- **Success Rate**: Percentage of successful executions
- **Average Duration**: Mean execution time in seconds  
- **Task Count**: Total number of tasks completed
- **Efficiency Score**: Success rate / duration ratio
- **Last Execution**: Timestamp of most recent execution

### Monitoring Dashboard

```python
def create_monitoring_dashboard(multi_agent):
    """Create a simple monitoring dashboard."""
    analysis = multi_agent.analyze_agent_performance()
    
    print("=" * 80)
    print(f"PERFORMANCE DASHBOARD: {multi_agent.name}")
    print("=" * 80)
    
    overall = analysis.get("overall", {})
    print(f"Overall Success Rate: {overall.get('average_success_rate', 0):.1%}")
    print(f"Average Duration: {overall.get('average_duration', 0):.2f}s")
    print(f"Total Tasks: {overall.get('total_tasks', 0)}")
    print(f"Best Performer: {overall.get('best_agent', 'Unknown')}")
    
    print("\nPER-AGENT METRICS:")
    for agent_name, metrics in analysis.get("agents", {}).items():
        print(f"  {agent_name:20} | "
              f"Success: {metrics['success_rate']:.1%} | "
              f"Duration: {metrics['avg_duration']:.2f}s | "
              f"Efficiency: {metrics['efficiency_score']:.3f}")

# Usage
create_monitoring_dashboard(your_multi_agent)
```

### Adaptive Behavior

```python
# Set adaptation rate to control learning speed
adaptive_multi = EnhancedMultiAgent(
    agents={"option_a": agent_a, "option_b": agent_b},
    performance_mode=True,
    adaptation_rate=0.1  # Gradual learning (0.0 = none, 1.0 = immediate)
)

# System automatically:
# 1. Tracks performance of each agent
# 2. Adjusts routing preferences based on success/speed
# 3. Favors better-performing agents over time
# 4. Maintains exploration vs exploitation balance
```

## 🚀 Production Deployment

### Environment Configuration

```python
# production_config.py
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent

def create_production_workflow():
    """Create production-ready multi-agent workflow."""
    
    # Production agents with appropriate settings
    agents = {
        "intake": EnhancedSimpleAgent(
            name="intake_processor",
            temperature=0.1,  # Low variance for intake
            system_message="You process and validate incoming requests."
        ),
        "analyzer": EnhancedSimpleAgent(
            name="request_analyzer", 
            temperature=0.3,  # Moderate for analysis
            system_message="You analyze requests and determine appropriate routing."
        ),
        "specialist": EnhancedSimpleAgent(
            name="domain_specialist",
            temperature=0.5,  # Balanced for specialized work
            system_message="You handle specialized domain requests with expertise."
        )
    }
    
    # Production workflow with monitoring
    workflow = EnhancedMultiAgent(
        name="production_request_processor",
        agents=agents,
        execution_mode="conditional",
        entry_point="intake",
        
        # Production features
        performance_mode=True,
        debug_mode=False,  # Disable verbose debugging in production
        advanced_routing=True,
        adaptation_rate=0.05,  # Conservative adaptation rate
        
        # Persistence for production
        persistence_config={
            "store_type": "postgres",
            "connection_string": "postgresql://user:pass@host/db"
        }
    )
    
    # Configure production routing
    def production_router(state):
        content = state["messages"][-1].content.lower()
        priority = state.get("shared_context", {}).get("priority", "normal")
        
        if priority == "high" or "urgent" in content:
            return "specialist"
        else:
            return "analyzer"
    
    workflow.add_conditional_routing(
        "intake",
        production_router,
        {
            "specialist": "specialist",
            "analyzer": "analyzer"
        }
    )
    
    return workflow

# Usage in production
production_workflow = create_production_workflow()
compiled = production_workflow.compile()

# Process production requests
def handle_request(user_input, priority="normal"):
    return compiled.invoke({
        "messages": [{"role": "user", "content": user_input}],
        "shared_context": {"priority": priority}
    })
```

### Error Handling & Resilience

```python
import logging
from typing import Optional

def robust_execution(multi_agent, input_data: dict, max_retries: int = 3) -> Optional[dict]:
    """Execute multi-agent with error handling and retries."""
    
    for attempt in range(max_retries):
        try:
            compiled = multi_agent.compile()
            result = compiled.invoke(input_data)
            
            # Validate result
            if result and "messages" in result and result["messages"]:
                logging.info(f"Multi-agent execution successful on attempt {attempt + 1}")
                return result
            else:
                logging.warning(f"Empty result on attempt {attempt + 1}")
                
        except Exception as e:
            logging.error(f"Execution failed on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                logging.error("All retry attempts exhausted")
                return None
            
            # Exponential backoff
            import time
            time.sleep(2 ** attempt)
    
    return None

# Usage
result = robust_execution(your_multi_agent, input_data)
if result:
    print("Success:", result["messages"][-1].content)
else:
    print("Failed after all retries")
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Import Errors
```python
# ❌ Wrong
from haive.agents.multi import EnhancedMultiAgent

# ✅ Correct  
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
```

#### 2. Message Format Issues
```python
# ❌ Wrong - Mixed formats cause validation errors
result = compiled.invoke({
    "messages": [{"role": "user", "content": "Hello"}]  # Dict format
})

# ✅ Correct - Use consistent BaseMessage format
from langchain_core.messages import HumanMessage
result = compiled.invoke({
    "messages": [HumanMessage(content="Hello")]
})
```

#### 3. Agent Not Found in Routing
```python
# ❌ Wrong - Agent referenced but not in collection
workflow = EnhancedMultiAgent(
    agents=[agent1, agent2],  # Only these exist
    entry_point="agent3"      # ❌ agent3 doesn't exist
)

# ✅ Correct - Ensure all referenced agents exist
workflow = EnhancedMultiAgent(
    agents={"agent1": agent1, "agent2": agent2},
    entry_point="agent1"  # ✅ agent1 exists
)
```

#### 4. Performance Mode Not Working
```python
# ❌ Wrong - Performance features disabled
workflow = EnhancedMultiAgent(agents=[agent1, agent2])
best = workflow.get_best_agent_for_task()  # Returns default

# ✅ Correct - Enable performance mode
workflow = EnhancedMultiAgent(
    agents=[agent1, agent2],
    performance_mode=True  # ✅ Now performance tracking works
)
```

### Debug Mode Investigation

```python
# Enable comprehensive debugging
debug_workflow = EnhancedMultiAgent(
    name="debug_investigation",
    agents=[agent1, agent2],
    debug_mode=True,
    performance_mode=True
)

# Check capabilities
debug_workflow.display_capabilities()

# Get detailed summary
summary = debug_workflow.get_capabilities_summary()

# Monitor execution
compiled = debug_workflow.compile()
result = compiled.invoke(test_input)

# Analyze what happened
if debug_workflow.performance_mode:
    analysis = debug_workflow.analyze_agent_performance()
    print("Performance Analysis:", analysis)
```

## 🎯 Best Practices

### 1. Agent Design
- **Clear Roles**: Give each agent a specific, well-defined responsibility
- **Appropriate Temperatures**: Lower for factual tasks, higher for creative tasks
- **Descriptive Names**: Use names that clearly indicate the agent's function
- **System Messages**: Provide clear instructions about the agent's role and behavior

```python
# ✅ Good agent design
data_validator = EnhancedSimpleAgent(
    name="data_validator",
    temperature=0.1,  # Low for consistency
    system_message="You validate data formats and check for errors. Return 'VALID' or 'INVALID' with specific error details."
)

creative_writer = EnhancedSimpleAgent(
    name="creative_writer", 
    temperature=0.8,  # High for creativity
    system_message="You write engaging, creative content that captures reader attention while maintaining factual accuracy."
)
```

### 2. Workflow Design
- **Start Simple**: Begin with sequential patterns, add complexity gradually
- **Test Each Pattern**: Validate each execution mode thoroughly before production
- **Monitor Performance**: Use performance_mode=True in production environments
- **Error Boundaries**: Implement proper error handling and fallback strategies

### 3. Performance Optimization
- **Adaptive Rates**: Start with low adaptation rates (0.1) and adjust based on needs
- **Performance Monitoring**: Regularly check agent performance metrics
- **Load Balancing**: Use performance data to balance workloads across agents
- **Caching**: Consider caching compiled workflows for repeated use

### 4. Production Readiness
- **Environment Variables**: Use environment variables for configuration
- **Logging**: Implement comprehensive logging with appropriate levels
- **Monitoring**: Set up dashboards to monitor multi-agent performance
- **Graceful Degradation**: Design workflows that can handle individual agent failures

### 5. Testing Strategy
- **Real Components**: Always test with real agents and LLMs (never mocks)
- **All Patterns**: Test each execution pattern your workflow uses
- **Edge Cases**: Test with unusual inputs and edge cases
- **Performance Validation**: Verify performance tracking features work correctly

## 📖 Example Workflows

### Content Creation Pipeline
```python
content_pipeline = EnhancedMultiAgent(
    name="content_creation",
    agents=[researcher, fact_checker, writer, editor],
    execution_mode="sequential",
    performance_mode=True
)
```

### Customer Service Router  
```python
customer_service = EnhancedMultiAgent(
    name="customer_service",
    agents={"intake": intake, "billing": billing, "tech": technical, "general": general},
    execution_mode="conditional",
    entry_point="intake",
    advanced_routing=True
)
```

### Data Processing Pipeline
```python
data_processor = EnhancedMultiAgent(
    name="data_processing",
    agents=[validator, transformer, analyzer, reporter],
    execution_mode="branch",
    performance_mode=True,
    debug_mode=True
)
```

---

## 🎉 Conclusion

Enhanced MultiAgent V3 provides a powerful, flexible foundation for building sophisticated multi-agent systems. With its type-safe design, comprehensive monitoring, and production-ready features, you can create robust workflows that scale with your needs.

**Ready to build?** Start with the Quick Start section and gradually explore the advanced features as your requirements grow.

**Need help?** Check the troubleshooting section or refer to the comprehensive test examples in the codebase.

**Happy Multi-Agent Building!** 🚀