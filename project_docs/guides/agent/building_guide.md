# Agent Building Guide - Haive Framework

**Version**: 1.0
**Purpose**: Comprehensive guide for building agents in Haive with practical examples
**Last Updated**: 2025-01-18

## 🎯 Overview

This guide provides a step-by-step approach to building agents in Haive, covering everything from basic setup to advanced patterns. We'll build real agents together as examples, documenting the process and best practices.

## 📋 Prerequisites

### Required Knowledge
- Basic Python and Pydantic understanding
- Familiarity with LangChain concepts
- Understanding of async/await patterns

### Environment Setup
```bash
# Ensure you're in the project directory
cd /home/will/Projects/haive/backend/haive

# Always use poetry run
poetry run python -c "from haive.core import *; print('✅ Imports working')"
```

## 🏗️ Agent Building Approach

### Our Methodology
1. **Start Simple** - Begin with basic functionality
2. **Build Incrementally** - Add features step by step
3. **Test Continuously** - Validate each addition with real components
4. **Document Everything** - Write Google-style docstrings
5. **Follow Patterns** - Use established Haive patterns

### Core Principles
- **No Mocks Ever** - Always test with real LLMs and components
- **Type Safety** - Use Pydantic models for all data structures
- **Explicit Imports** - Always use `from haive.core.*` style imports
- **Research First** - Check existing agents before building new ones

## 📚 Agent Types & Patterns

### 1. Simple Agent Pattern
- Basic conversational agent
- Single LLM interaction
- Simple input/output

### 2. Structured Output Agent Pattern
- Agent with defined output schema
- Type-safe responses
- Integration with multi-agent workflows

### 3. Tool-Using Agent Pattern
- Agent with external tools
- Dynamic tool selection
- Tool result processing

### 4. RAG Agent Pattern
- Retrieval-augmented generation
- Document processing
- Context-aware responses

### 5. Multi-Agent Coordination Pattern
- Sequential agent workflows
- Shared state management
- Cross-agent communication
- **See: [Multi-Agent Guide](multi/README.md)**

## 🔧 Building Your First Agent

### Step 1: Research Existing Patterns

Before building any agent, always research existing implementations:

```bash
# Check existing agent patterns
find packages/haive-agents/src -name "*.py" | head -10

# Look for similar functionality
grep -r "your_concept" packages/haive-agents/src | head -5

# Check test patterns
find packages/haive-agents/tests -name "test_*.py" | head -5
```

### Step 2: Choose Your Base Pattern

Based on your needs:

```python
# Simple conversational agent
from haive.agents.simple import SimpleAgent

# Tool-using agent
from haive.agents.react import ReactAgent

# RAG agent
from haive.agents.rag.base import BaseRAGAgent
```

### Step 3: Define Your Agent's Purpose

Write a clear purpose statement:

```python
"""
Agent Purpose: [Clear description of what this agent does]
Input: [What data it expects]
Output: [What it produces]
Use Case: [When to use this agent]
"""
```

## 🎯 Example 1: Building a Content Analyzer Agent

Let's build a practical agent together that analyzes content and provides structured feedback.

### Agent Specification

**Purpose**: Analyze text content and provide structured feedback on quality, clarity, and improvements.

**Input**: Text content to analyze
**Output**: Structured analysis with scores and recommendations
**Use Case**: Content review, writing assistance, quality assessment

### Implementation Steps

#### Step 1: Define the Output Schema

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ContentAnalysis(BaseModel):
    """Structured output for content analysis."""
    
    overall_score: float = Field(
        ge=0.0, le=10.0,
        description="Overall content quality score (0-10)"
    )
    
    clarity_score: float = Field(
        ge=0.0, le=10.0,
        description="Clarity and readability score (0-10)"
    )
    
    engagement_score: float = Field(
        ge=0.0, le=10.0,
        description="Engagement and interest score (0-10)"
    )
    
    strengths: List[str] = Field(
        description="List of content strengths"
    )
    
    improvements: List[str] = Field(
        description="List of suggested improvements"
    )
    
    key_themes: List[str] = Field(
        description="Main themes identified in content"
    )
    
    tone: str = Field(
        description="Overall tone of the content"
    )
    
    target_audience: str = Field(
        description="Identified target audience"
    )
    
    recommendations: List[str] = Field(
        description="Specific actionable recommendations"
    )
```

#### Step 2: Create the Agent

```python
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

class ContentAnalyzerAgent(SimpleAgent):
    """Agent that analyzes text content and provides structured feedback.
    
    This agent specializes in content analysis, providing detailed feedback
    on quality, clarity, engagement, and actionable recommendations for
    improvement.
    
    Examples:
        Basic usage::
        
            agent = ContentAnalyzerAgent()
            analysis = agent.run("Your content here...")
            print(f"Overall score: {analysis.overall_score}")
            
        With custom configuration::
        
            agent = ContentAnalyzerAgent(
                engine=AugLLMConfig(temperature=0.3)
            )
            analysis = agent.run(content, debug=True)
    """
    
    def __init__(
        self,
        name: str = "content_analyzer",
        engine: AugLLMConfig = None,
        **kwargs
    ):
        """Initialize the content analyzer agent.
        
        Args:
            name: Agent identifier
            engine: LLM configuration (uses default if None)
            **kwargs: Additional arguments passed to parent
        """
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.3,  # Lower temperature for consistent analysis
                system_message=self._get_system_message()
            )
        
        super().__init__(
            name=name,
            engine=engine,
            structured_output_model=ContentAnalysis,
            **kwargs
        )
    
    def _get_system_message(self) -> str:
        """Get the system message for content analysis."""
        return """You are a professional content analyst and writing coach.
        
        Your role is to:
        1. Analyze text content for quality, clarity, and engagement
        2. Provide constructive feedback with specific examples
        3. Identify strengths and areas for improvement
        4. Suggest actionable recommendations
        5. Assess tone and target audience
        
        Always be:
        - Constructive and helpful
        - Specific with examples
        - Balanced in feedback
        - Professional in tone
        
        Provide scores on a 1-10 scale where:
        - 1-3: Needs significant improvement
        - 4-6: Good with room for improvement
        - 7-8: Strong content
        - 9-10: Exceptional content
        """
```

#### Step 3: Create Test Cases

```python
import pytest
from haive.core.engine.aug_llm import AugLLMConfig

class TestContentAnalyzerAgent:
    """Test suite for ContentAnalyzerAgent."""
    
    def test_agent_creation(self):
        """Test agent can be created successfully."""
        agent = ContentAnalyzerAgent()
        assert agent.name == "content_analyzer"
        assert agent.structured_output_model == ContentAnalysis
    
    def test_content_analysis_with_real_llm(self):
        """Test content analysis with real LLM."""
        agent = ContentAnalyzerAgent()
        
        test_content = """
        Artificial intelligence is transforming how we work and live. 
        From automating routine tasks to enabling new forms of creativity,
        AI is becoming an integral part of our daily experiences.
        However, we must consider the ethical implications and ensure
        that AI development benefits everyone.
        """
        
        result = agent.run(test_content)
        
        # Verify structured output
        assert isinstance(result, ContentAnalysis)
        assert 0.0 <= result.overall_score <= 10.0
        assert 0.0 <= result.clarity_score <= 10.0
        assert 0.0 <= result.engagement_score <= 10.0
        assert len(result.strengths) > 0
        assert len(result.improvements) > 0
        assert len(result.key_themes) > 0
        assert result.tone
        assert result.target_audience
        assert len(result.recommendations) > 0
    
    def test_poor_content_analysis(self):
        """Test analysis of poor quality content."""
        agent = ContentAnalyzerAgent()
        
        poor_content = "this is bad content with no structure or clarity"
        
        result = agent.run(poor_content)
        
        # Should identify issues
        assert result.overall_score < 5.0
        assert len(result.improvements) > 0
        assert "clarity" in " ".join(result.improvements).lower()
    
    def test_high_quality_content_analysis(self):
        """Test analysis of high quality content."""
        agent = ContentAnalyzerAgent()
        
        quality_content = """
        The future of sustainable energy lies in the convergence of three 
        revolutionary technologies: advanced battery storage, smart grid 
        infrastructure, and renewable energy sources.
        
        Battery technology has evolved dramatically, with lithium-ion 
        efficiency improving by 300% over the past decade. This breakthrough 
        enables storing renewable energy during peak production times and 
        releasing it when demand is highest.
        
        Smart grids represent the nervous system of this new energy 
        ecosystem, using AI to predict consumption patterns and optimize 
        energy distribution in real-time. This intelligence reduces waste 
        by up to 40% compared to traditional grid systems.
        
        When combined with rapidly advancing solar and wind technologies, 
        these innovations create a sustainable energy future that is both 
        economically viable and environmentally responsible.
        """
        
        result = agent.run(quality_content)
        
        # Should recognize quality
        assert result.overall_score >= 7.0
        assert len(result.strengths) >= 3
        assert any("structure" in strength.lower() for strength in result.strengths)
```

#### Step 4: Run and Validate

```bash
# Test the agent
poetry run python -c "
from content_analyzer_agent import ContentAnalyzerAgent
agent = ContentAnalyzerAgent()
result = agent.run('This is a test content for analysis.')
print(f'Score: {result.overall_score}')
print(f'Strengths: {result.strengths}')
"

# Run full test suite
poetry run pytest test_content_analyzer_agent.py -v
```

## 🎯 Multi-Agent Systems

For building multi-agent systems and coordination patterns, see the dedicated guide:

**[Multi-Agent Systems Guide](multi/README.md)**

Topics covered:
- Sequential agent workflows
- Shared state management
- Cross-agent communication
- Self-Discover patterns
- Direct field updates
- Real-world examples

## 🔧 Advanced Patterns

### Pattern 1: Agent with Dynamic Tools

[To be documented as we build]

### Pattern 2: RAG Agent with Custom Retrieval

[To be documented as we build]

### Pattern 3: Multi-Modal Agent

[To be documented as we build]

## 📚 Best Practices

### 1. Agent Design Principles

- **Single Responsibility**: Each agent should have one clear purpose
- **Composability**: Agents should work well together
- **Configurability**: Allow customization without code changes
- **Testability**: Easy to test with real components

### 2. Code Organization

```
your_agent/
├── __init__.py          # Public API
├── agent.py             # Main agent implementation
├── schemas.py           # Pydantic models
├── prompts.py           # System messages and prompts
└── tests/
    ├── __init__.py
    ├── test_agent.py    # Agent tests
    └── test_integration.py  # Integration tests
```

### 3. Documentation Standards

- **Google-style docstrings** for all classes and methods
- **Usage examples** in docstrings
- **Type hints** for all parameters and returns
- **Integration examples** showing real usage

### 4. Testing Approach

- **No mocks** - always test with real components
- **Incremental testing** - test each feature as you add it
- **Edge case coverage** - test error conditions
- **Performance testing** - measure response times

## 🚨 Common Pitfalls to Avoid

1. **Overcomplicating**: Start simple, add complexity gradually
2. **Ignoring existing patterns**: Always research before building
3. **Skipping tests**: Test continuously during development
4. **Poor error handling**: Handle failures gracefully
5. **Unclear purpose**: Define agent's role clearly

## 🎯 Next Steps

As we build agents together, we'll:

1. **Add real examples** to each section
2. **Document patterns** we discover
3. **Create templates** for common agent types
4. **Build integration examples** showing agents working together
5. **Add troubleshooting sections** based on issues we encounter

## 📖 References

- [Multi-Agent Systems Guide](multi/README.md)
- [Multi-Agent Architecture](../../active/architecture/multi_agent_meta_agent_memory_hub.md)
- [Testing Philosophy](../../active/standards/testing/philosophy.md)
- [Pydantic Patterns](../../active/standards/coding/PYDANTIC_PATTERNS.md)
- [Command Execution Guide](../../active/standards/coding/COMMAND_EXECUTION_GUIDE.md)

---

**Note**: This guide is living documentation that grows as we build agents together. Each example will be fully implemented and tested with real components.