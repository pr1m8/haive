.. title:: Building Agents
.. _building_agents:

Building Agents
===============

This comprehensive guide shows you how to build powerful, production-ready agents with Haive. From simple assistants to complex multi-agent systems, you'll learn the patterns and best practices that make great agents.

.. raw:: html

   .. raw:: html

   <div class="guide-hero">
   <h2>🤖 Master the Art of Agent Building</h2>
   <p>Learn how to create agents that can reason, use tools, maintain state, and work together</p>
   </div>

   <style>
   .guide-hero {
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   color: white;
   padding: 2rem;
   border-radius: 12px;
   text-align: center;
   margin: 1rem 0 2rem;
   }
   .guide-hero h2 {
   margin: 0 0 0.5rem;
   }
   .guide-hero p {
   margin: 0;
   opacity: 0.9;
   }
   </style>

Agent Fundamentals

------------------

At their core, Haive agents are stateful processing units that:

1. **Receive input***s** - Process queries, commands, and data**

2.*** **Think and reaso***n** - Use cognitive engines (LLMs) to understand and plan

3.*** **Take action***s** - Execute tools and interact with external systems
4.*** **Produce output***s** - Return responses, data, or trigger actions
5.*** **Maintain stat***e** - Remember context and learn from interactions

Complete Agent Creation Examples

--------------------------------

🎯 Example 1: Basic Conversational Agent

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_01.py
    """Creating Your First Production-Ready Agent

    This example shows best practices for creating a robust agent
    with proper error handling, logging, and configuration.   """"""""""""""""""""""""""""""""""""""""""""""""""

    from haive.agents import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig
    import logging
    import os
    from typing import Optional

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class ConversationalAssistant:
    """A well-structured conversational agent."""

    def __init__(self, 
    name: str = "Assistant",
    model: str = "gpt-4",
    temperature: float = 0.7,
    system_prompt: Optional[str] = None):
    """Initialize the assistant with configuration.

    Args:
    name: Agent's name
    model: LLM model to use
    temperature: Response randomness (0-1)
    system_prompt: Custom system instructions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""
           self.name = name
           self.model = model
           
           # Default system prompt
           if system_prompt is None:
               system_prompt = f"""You are {name}, a helpful AI assistant.
               You are knowledgeable, friendly, and concise.
               Always strive to be helpful while being honest about limitations."""
           
           # Create the agent
           self.agent = SimpleAgent(
               name=name,
               engine=AugLLMConfig(
                   model=model,
                   temperature=temperature,
                   system_prompt=system_prompt,
                   api_key=os.getenv("OPENAI_API_KEY")
               ),
               description=f"{name} - A conversational AI assistant"
           )
           
           logger.info(f"Initialized {name} with model {model}")
       
       def chat(self, message: str) -> str:
           """Send a message to the assistant.
           
           Args:
               message: User's message
               
           Returns:
               Assistant's response

"""""""""""""""""""""""""""""""""""
           try:
               logger.info(f"Processing message: {message[:50]}...")
               response = self.agent.invoke(message)
               logger.info(f"Generated response: {response[:50]}...")
               return response
           except Exception as e:
               logger.error(f"Error in chat: {e}")
               return f"I apologize, but I encountered an error: {str(e)}"
       
       async def chat_async(self, message: str) -> str:
           """Async version of chat."""
           try:
               response = await self.agent.ainvoke(message)
               return response
           except Exception as e:
               logger.error(f"Error in async chat: {e}")
               return f"I apologize, but I encountered an error: {str(e)}"

   
    # Example usage
    def demo_basic_agent():

       """Demonstrate basic agent usage."""
       
       # Create assistant
       assistant = ConversationalAssistant(
           name="Sophia",
           model="gpt-4",
           temperature=0.7
       )
       
       # Example conversations
       queries = [
           "What are the key principles of good software design?",
           "Can you explain SOLID principles with examples?",
           "How do I know when to refactor my code?"
       ]
       
       print("💬 Conversational Assistant Demo\n")
       
       for query in queries:
           print(f"Human: {query}")
           response = assistant.chat(query)
           print(f"Sophia: {response}\n")
           print("-"*** * 80 + "\n")*

   
    if __name__ == "__main__":

       demo_basic_agent()

    🎯 Example 2: Specialized Domain Expert

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_02.py
    """Creating Specialized Domain Experts

    This example shows how to create agents with specific expertise
    and custom behaviors for different domains.   """"""""""""""""""""""""""""""""""""""

    from haive.agents import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig
    from pydantic import BaseModel, Field
    from typing import List, Optional
    from datetime import datetime

    class MedicalAdvice(BaseModel):
    """Structured medical advice output."""
    symptoms_understood: List[str]
    possible_conditions: List[str]
    recommended_actions: List[str]
    urgency_level: str = Field(description="low, medium, high, emergency")
    disclaimer: str = "This is not a substitute for professional medical advice"

    class TechnicalAnalysis(BaseModel):
    """Structured technical analysis output."""
    problem_summary: str
    root_causes: List[str]
    solutions: List[dict]  # [{"step": 1, "action": "...", "details": "..."}]
    estimated_time: str
    difficulty_level: str = Field(description="beginner, intermediate, advanced")

    def create_medical_advisor() -> SimpleAgent:
    """Create a medical advice agent (for educational purposes only)."""

    system_prompt = """You are a medical information assistant designed to 
    provide educational health information only. You are NOT a replacement 
    for professional medical advice. Always remind users to consult with 
    healthcare professionals for actual medical concerns.

    Guidelines:
    1. Listen carefully to symptoms
    2. Provide general educational information
    3. Always emphasize the importance of professional consultation
    4. Never diagnose or prescribe treatments
    5. Flag emergency symptoms immediately

"""""""""""""""""""""""""""""""""""""""""""""
       
       return SimpleAgent(
           name="Medical Info Assistant",
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.3,  # Lower temperature for consistency
               system_prompt=system_prompt
           ),
           structured_output_model=MedicalAdvice,
           description="Provides educational medical information"
       )

   
    def create_tech_support_expert() -> SimpleAgent:

       """Create a technical support expert agent."""
       
       system_prompt = """You are an expert technical support engineer with 
       deep knowledge of:
       - Software development and debugging
       - System administration (Linux, Windows, MacOS)
       - Network troubleshooting
       - Database management
       - Cloud services (AWS, Azure, GCP)
       
       Your approach:
       1. Gather detailed information about the problem
       2. Analyze potential root causes systematically
       3. Provide step-by-step solutions
       4. Offer preventive measures
       5. Estimate time and complexity honestly

"""""""""""""""""""""""""""""""""""""""""""""""
       
       return SimpleAgent(
           name="Tech Support Expert",
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.5,
               system_prompt=system_prompt
           ),
           structured_output_model=TechnicalAnalysis,
           description="Expert technical support and troubleshooting"
       )

   
    def create_financial_analyst() -> SimpleAgent:

       """Create a financial analysis agent."""
       
       system_prompt = """You are a seasoned financial analyst with expertise in:
       - Investment analysis and portfolio management
       - Risk assessment and mitigation
       - Market trends and economic indicators
       - Financial planning and budgeting
       - Cryptocurrency and emerging markets
       
       Provide balanced, well-researched financial insights while always 
       reminding users that this is educational content, not personalized 
       financial advice.

""""""""""""""""""""""""
       
       return SimpleAgent(
           name="Financial Analyst",
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.4,
               system_prompt=system_prompt
           ),
           description="Financial analysis and market insights"
       )

   
    def demo_domain_experts():

       """Demonstrate specialized domain experts."""
       
       print("🏥 Medical Information Assistant Demo\n")
       medical = create_medical_advisor()
       result = medical.invoke(
           "I've been having headaches for 3 days, especially in the morning, "
           "and I feel dizzy when I stand up quickly."
       )
       print(f"Symptoms understood: {', '.join(result.symptoms_understood)}")
       print(f"Urgency level: {result.urgency_level}")
       print(f"Recommended actions:")
       for action in result.recommended_actions:
           print(f"  • {action}")
       print(f"\n⚠️  {result.disclaimer}\n")
       
       print("\n" + "=*"*80 + "\n")
       
       print("💻 Technical Support Expert Demo\n")
       tech = create_tech_support_expert()
       result = tech.invoke(
           "My Python application is consuming 100% CPU and the memory usage "
           "keeps growing. It's a web scraper that processes large datasets."
       )
       print(f"Problem: {result.problem_summary}")
       print(f"Root causes:")
       for cause in result.root_causes:
           print(f"  • {cause}")
       print(f"\nSolutions:")
       for solution in result.solutions[:3]:
           print(f"  Step {solution['step']}: {solution['action']}")
           print(f"    Details: {solution['details']}")
       print(f"\nEstimated time: {result.estimated_time}")
       print(f"Difficulty: {result.difficulty_level}")

   
    if __name__ == "__main__":

       demo_domain_experts()

    Advanced Tool Integration

    -------------------------

    🔧 Example 3: Multi-Tool Research Assistant

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_03.py
    """Advanced Tool Integration for Agents

    This example demonstrates how to create agents that effectively
    use multiple tools to solve complex problems.   """"""""""""""""""""""""""""""""""""""""

    from haive.agents import SimpleAgent, ReactAgent
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.tools import (
    WebSearchTool, CalculatorTool, FileReaderTool,
    CodeInterpreterTool, DataVisualizationTool
    )
    from haive.tools.base import Tool
    from typing import List, Dict, Any
    import json

    # Custom tool example
    class StockAnalyzerTool(Tool):
    """Custom tool for stock analysis."""

    name = "stock_analyzer"
    description = "Analyze stock performance and metrics"

    def __init__(self):
    super().__init__()
    # In real implementation, this would connect to a financial API
    self.mock_data = {
    "AAPL": {"price": 189.50, "change": 2.3, "pe": 31.2},
    "GOOGL": {"price": 142.20, "change": -0.8, "pe": 25.4},
    "MSFT": {"price": 378.90, "change": 1.5, "pe": 35.1}
    }

    def run(self, ticker: str) -> str:
    """Get stock information.

    Args:
    ticker: Stock ticker symbol

    Returns:
    JSON string with stock data

""""""""""""""""""""""""""""""""""""""""""
           if ticker.upper() in self.mock_data:
               data = self.mock_data[ticker.upper()]
               return json.dumps({
                   "ticker": ticker.upper(),
                   "current_price": data["price"],
                   "change_percent": data["change"],
                   "pe_ratio": data["pe"],
                   "analysis": f"{ticker} is {'up' if data['change'] > 0 else 'down'} {abs(data['change'])}% today"
               })
           else:
               return json.dumps({
                   "error": f"No data available for {ticker}"
               })

   
    class DatabaseQueryTool(Tool):

       """Custom tool for database queries."""
       
       name = "database_query"
       description = "Query internal company database for business metrics"
       
       def run(self, query: str) -> str:
           """Execute a database query.
           
           Args:
               query: SQL-like query string
               
           Returns:
               Query results as JSON

""""""""""""""""""""""""""""""""""""
           # Mock implementation
           if "sales" in query.lower():
               return json.dumps({
                   "result": [
                       {"month": "Jan", "revenue": 125000, "units": 850},
                       {"month": "Feb", "revenue": 132000, "units": 920},
                       {"month": "Mar", "revenue": 141000, "units": 980}
                   ],
                   "query": query,
                   "rows_returned": 3
               })
           else:
               return json.dumps({
                   "error": "Query not recognized",
                   "suggestion": "Try querying for 'sales' data"
               })

   
    def create_research_assistant() -> ReactAgent:

       """Create a powerful research assistant with multiple tools."""
       
       tools = [
           WebSearchTool(
               name="web_search",
               description="Search the internet for current information"
           ),
           CalculatorTool(
               name="calculator",
               description="Perform mathematical calculations"
           ),
           StockAnalyzerTool(),
           DatabaseQueryTool(),
           CodeInterpreterTool(
               name="python_executor",
               description="Execute Python code for data analysis"
           ),
           DataVisualizationTool(
               name="chart_creator",
               description="Create charts and visualizations"
           )
       ]
       
       system_prompt = """You are a comprehensive research assistant with access 
       to multiple tools. Your goal is to provide thorough, accurate research by:
       
       1. Understanding the user's research needs
       2. Selecting appropriate tools for the task
       3. Combining information from multiple sources
       4. Performing calculations and analysis as needed
       5. Creating visualizations when helpful
       6. Providing well-structured, actionable insights
       
       Always cite your sources and explain your methodology.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       
       return ReactAgent(
           name="Research Assistant",
           tools=tools,
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.5,
               system_prompt=system_prompt
           ),
           max_iterations=5,  # Allow multiple tool uses
           description="Comprehensive research assistant with multiple tools"
       )

   
    def demo_tool_integration():

       """Demonstrate advanced tool usage."""
       
       print("🔍 Multi-Tool Research Assistant Demo\n")
       
       assistant = create_research_assistant()
       
       # Example 1: Financial Analysis
       print("📊 Example 1: Financial Market Analysis")
       print("Query: Analyze Apple stock and compare with our Q1 sales performance\n")
       
       result = assistant.invoke(
           "Analyze Apple (AAPL) stock performance and compare it with our "
           "internal Q1 sales data. Calculate the correlation if any and "
           "create a visualization showing both trends."
       )
       print(f"Assistant: {result}\n")
       print("-"* * 80 + "\n")
       
       # Example 2: Complex Research
       print("🌍 Example 2: Multi-Source Research")
       print("Query: Impact of AI on software development productivity\n")
       
       result = assistant.invoke(
           "Research the impact of AI tools on software development productivity. "
           "Find recent statistics, calculate productivity gains, and analyze "
           "the trend. Include both benefits and challenges."
       )
       print(f"Assistant: {result}\n")
       print("-"* * 80 + "\n")
       
       # Example 3: Data Analysis
       print("📈 Example 3: Data Analysis and Visualization")
       print("Query: Analyze our sales growth rate and project next quarter\n")
       
       result = assistant.invoke(
           "Using our sales database, calculate the month-over-month growth rate, "
           "identify trends, and project next quarter's revenue. Create a chart "
           "showing historical data and projections."
       )
       print(f"Assistant: {result}\n")

   
    def demonstrate_tool_selection():

       """Show how agents select appropriate tools."""
       
       print("\n🎯 Tool Selection Intelligence Demo\n")
       
       assistant = create_research_assistant()
       
       # Different queries that require different tools
       queries = [
           ("Calculate compound interest on $10,000 at 5% for 10 years",
            "Should use: Calculator"),
           ("What's the current Bitcoin price?",
            "Should use: Web Search"),
           ("Analyze our Q1 sales data and find the best performing month",
            "Should use: Database Query + Python"),
           ("Create a fibonacci sequence and plot it",
            "Should use: Python + Visualization")
       ]
       
       for query, expected in queries:
           print(f"Query: {query}")
           print(f"Expected: {expected}")
           result = assistant.invoke(query)
           print(f"Result: {result[:150]}...\n")

   
    if __name__ == "__main__":

       demo_tool_integration()
       print("\n" + "=*"*80 + "\n")
       demonstrate_tool_selection()

    Building Custom Agent Classes

    -----------------------------

    🏗️ Example 4: Stateful Custom Agents

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_04.py
    """Building Custom Agent Classes

    This example shows how to create custom agent classes with
    specialized behavior, state management, and advanced features.   """""""""""""""""""""""""""""""""""""""""""""""""""""""""

    from haive.agents import BaseAgent
    from haive.core.schema import AgentState
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.tools import WebSearchTool, FileReaderTool
    from pydantic import BaseModel, Field
    from typing import List, Dict, Optional, Any
    from datetime import datetime
    import json
    from enum import Enum

    # Custom state definitions
    class ResearchPhase(str, Enum):
    """Research workflow phases."""
    PLANNING = "planning"
    GATHERING = "gathering"
    ANALYZING = "analyzing"
    SYNTHESIZING = "synthesizing"
    COMPLETE = "complete"

    class ResearchItem(BaseModel):
    """A single research item."""
    topic: str
    query: str
    findings: str
    confidence: float = Field(ge=0, le=1)
    sources: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

    class ResearchPlan(BaseModel):
    """Research plan structure."""
    objective: str
    questions: List[str]
    methodology: str
    estimated_time: str

    class AdvancedResearchState(AgentState):
    """State for advanced research agent."""
    current_phase: ResearchPhase = ResearchPhase.PLANNING
    research_plan: Optional[ResearchPlan] = None
    research_items: List[ResearchItem] = Field(default_factory=list)
    synthesis: Optional[str] = None
    total_queries: int = 0
    start_time: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class AdvancedResearchAgent(BaseAgent):
    """A sophisticated research agent with workflow management."""

    state_class = AdvancedResearchState

    def __init__(self, name: str = "Advanced Researcher",* **kwargs):**
    """Initialize the research agent."""
    # Set up tools
    tools = [
    WebSearchTool(),
    FileReaderTool()
    ]

    # Configure engine
    engine = AugLLMConfig(
    model="gpt-4",
    temperature=0.6,
    system_prompt="""You are an advanced research agent capable of:
    1. Planning comprehensive research strategies
    2. Gathering information from multiple sources
    3. Analyzing and validating findings
    4. Synthesizing insights into actionable recommendations

    Always maintain objectivity and cite sources."""
    )

    super().__init__(
    name=name,
    tools=tools,
    engine=engine,
    *** **kwargs
    )

    def plan_research(self, objective: str) -> ResearchPlan:
    """Create a research plan based on the objective.

    Args:
    objective: Research objective

    Returns:
    Structured research plan

"""""""""""""""""""""""""""""""""""""""
           self.state.current_phase = ResearchPhase.PLANNING
           
           # Generate research plan
           plan_prompt = f"""Create a detailed research plan for: {objective}
           
           Include:
           1. Key research questions (5-7 questions)
           2. Methodology approach
           3. Estimated time needed

"""""""""""""""""""""""""""""""""""
           
           response = self.invoke(plan_prompt)
           
           # Parse into structured plan (in real implementation, 
           # this would use structured output)
           plan = ResearchPlan(
               objective=objective,
               questions=[
                   "What is the current state of this topic?",
                   "What are the main challenges?",
                   "What solutions exist?",
                   "What are future trends?",
                   "What are the implications?"
               ],
               methodology="Mixed-method research using web sources and analysis",
               estimated_time="30-45 minutes"
           )
           
           self.state.research_plan = plan
           return plan
       
       def gather_information(self) -> List[ResearchItem]:
           """Gather information based on the research plan.
           
           Returns:
               List of research findings

""""""""""""""""""""""""""""""""""""""""
           if not self.state.research_plan:
               raise ValueError("No research plan available. Call plan_research first.")
           
           self.state.current_phase = ResearchPhase.GATHERING
           
           for question in self.state.research_plan.questions:
               # Research each question
               findings = self.invoke(f"Research: {question}")
               
               item = ResearchItem(
                   topic=self.state.research_plan.objective,
                   query=question,
                   findings=findings,
                   confidence=0.85,  # In real implementation, calculate this
                   sources=["web_search", "analysis"]
               )
               
               self.state.research_items.append(item)
               self.state.total_queries += 1
           
           return self.state.research_items
       
       def analyze_findings(self) -> Dict[str, Any]:
           """Analyze all gathered information.
           
           Returns:
               Analysis results

"""""""""""""""""""""""""""""""
           self.state.current_phase = ResearchPhase.ANALYZING
           
           # Compile all findings
           all_findings = "\n\n".join([
               f"Q: {item.query}\nA: {item.findings}"
               for item in self.state.research_items
           ])
           
           analysis_prompt = f"""Analyze these research findings and identify:
           1. Key themes and patterns
           2. Contradictions or gaps
           3. Strength of evidence
           4. Actionable insights
           
           Findings:
           {all_findings}

"""""""""""""""""""""""""
           
           analysis = self.invoke(analysis_prompt)
           
           return {
               "themes": ["Theme 1", "Theme 2"],  # Parsed from analysis
               "gaps": ["Gap 1", "Gap 2"],
               "insights": ["Insight 1", "Insight 2"],
               "raw_analysis": analysis
           }
       
       def synthesize_research(self) -> str:
           """Create final synthesis of all research.
           
           Returns:
               Final research synthesis

"""""""""""""""""""""""""""""""""""""""
           self.state.current_phase = ResearchPhase.SYNTHESIZING
           
           synthesis_prompt = f"""Create a comprehensive synthesis of the research on:
           {self.state.research_plan.objective}
           
           Include:
           1. Executive summary
           2. Key findings
           3. Recommendations
           4. Future considerations
           
           Base this on all the research gathered and analyzed.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
           
           synthesis = self.invoke(synthesis_prompt)
           self.state.synthesis = synthesis
           self.state.current_phase = ResearchPhase.COMPLETE
           
           return synthesis
       
       def get_research_summary(self) -> Dict[str, Any]:
           """Get a summary of the research process.
           
           Returns:
               Research summary with metrics

""""""""""""""""""""""""""""""""""""""""""""
           duration = (datetime.now() - self.state.start_time).total_seconds() / 60
           
           return {
               "objective": self.state.research_plan.objective if self.state.research_plan else None,
               "current_phase": self.state.current_phase.value,
               "total_queries": self.state.total_queries,
               "items_researched": len(self.state.research_items),
               "duration_minutes": round(duration, 2),
               "has_synthesis": bool(self.state.synthesis)
           }
       
       def export_research(self, format: str = "json") -> str:
           """Export research in specified format.
           
           Args:
               format: Export format (json, markdown, html)
               
           Returns:
               Formatted research export

""""""""""""""""""""""""""""""""""""""""
           if format == "json":
               return json.dumps({
                   "research_plan": self.state.research_plan.dict() if self.state.research_plan else None,
                   "findings": [item.dict() for item in self.state.research_items],
                   "synthesis": self.state.synthesis,
                   "metadata": self.get_research_summary()
               }, default=str, indent=2)
           
           elif format == "markdown":
               md = f"# Research Report: {self.state.research_plan.objective}\n\n"
               md += f"## Summary\n{self.state.synthesis}\n\n"
               md += "## Detailed Findings\n"
               for item in self.state.research_items:
                   md += f"### {item.query}\n{item.findings}\n\n"
               return md
           
           else:
               raise ValueError(f"Unsupported format: {format}")

   
    # Demonstration
    def demo_custom_agent():

       """Demonstrate the custom research agent."""
       
       print("🔬 Advanced Research Agent Demo\n")
       
       # Create agent
       researcher = AdvancedResearchAgent()
       
       # Define research objective
       objective = "The impact of quantum computing on cryptography and cybersecurity"
       
       print(f"Research Objective: {objective}\n")
       
       # Step 1: Planning
       print("📋 Phase 1: Planning Research")
       plan = researcher.plan_research(objective)
       print(f"Questions to research:")
       for i, q in enumerate(plan.questions, 1):
           print(f"  {i}. {q}")
       print(f"Methodology: {plan.methodology}")
       print(f"Estimated time: {plan.estimated_time}\n")
       
       # Step 2: Gathering
       print("🔍 Phase 2: Gathering Information")
       items = researcher.gather_information()
       print(f"Gathered {len(items)} research items\n")
       
       # Step 3: Analysis
       print("📊 Phase 3: Analyzing Findings")
       analysis = researcher.analyze_findings()
       print(f"Identified {len(analysis['themes'])} key themes")
       print(f"Found {len(analysis['gaps'])} research gaps\n")
       
       # Step 4: Synthesis
       print("📝 Phase 4: Synthesizing Research")
       synthesis = researcher.synthesize_research()
       print(f"Synthesis preview: {synthesis[:200]}...\n")
       
       # Summary
       print("📈 Research Summary")
       summary = researcher.get_research_summary()
       for key, value in summary.items():
           print(f"  {key}: {value}")
       
       # Export
       print("\n💾 Exporting Research")
       export_path = "quantum_cryptography_research.json"
       with open(export_path, "w") as f:
           f.write(researcher.export_research("json"))
       print(f"Research exported to {export_path}")

   
    if __name__ == "__main__":

       demo_custom_agent()

    Agent Design Patterns

    ---------------------

    🎯 Example 5: Implementing Core Agent Patterns

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_05.py
    """Core Agent Design Patterns

    This example demonstrates the main agent patterns supported by Haive
    and when to use each one.   """"""""""""""""""""

    from haive.agents import SimpleAgent, ReactAgent, PlanExecuteAgent
    from haive.agents.rag import SimpleRAGAgent
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.tools import WebSearchTool, CalculatorTool, CodeInterpreterTool
    from haive.tools.retrieval import VectorRetriever
    import asyncio
    from typing import List, Dict

    # Pattern 1: ReAct (Reasoning + Action)
    def create_react_problem_solver() -> ReactAgent:
    """Create a ReAct agent for complex problem solving.

    Best for: Multi-step problems requiring tool use and reasoning

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       return ReactAgent(
           name="ReAct Problem Solver",
           tools=[
               WebSearchTool(),
               CalculatorTool(),
               CodeInterpreterTool()
           ],
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.5,
               system_prompt="""You solve problems step by step using the ReAct pattern:
               1. Thought: Analyze what you need to do
               2. Action: Use a tool to gather information or perform a task
               3. Observation: Examine the result
               4. Repeat until solved

"""""""""""""""""""""""""""""""""""""
           ),
           max_iterations=5,
           description="Solves complex problems with reasoning and actions"
       )

   
    # Pattern 2: RAG (Retrieval-Augmented Generation)
    def create_rag_knowledge_assistant() -> SimpleRAGAgent:

       """Create a RAG agent for knowledge-intensive tasks.
       
       Best for: Q&A over documents, knowledge bases, or specific domains

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       # In real implementation, this would load your documents
       retriever = VectorRetriever(
           collection_name="knowledge_base",
           embedding_model="openai"
       )
       
       return SimpleRAGAgent(
           name="RAG Knowledge Assistant",
           retriever=retriever,
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.3,
               system_prompt="""You are a knowledge assistant that answers questions 
               based on retrieved context. Always cite your sources and indicate 
               when information is not available in the knowledge base."""
           ),
           chunk_size=512,
           top_k=5,
           description="Answers questions using retrieved knowledge"
       )

   
    # Pattern 3: Plan-Execute
    def create_plan_execute_agent() -> PlanExecuteAgent:

       """Create a Plan-Execute agent for complex workflows.
       
       Best for: Tasks requiring upfront planning and systematic execution

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       return PlanExecuteAgent(
           name="Strategic Planner",
           planner_engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.7,
               system_prompt="You create detailed, step-by-step plans"
           ),
           executor_engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.3,
               system_prompt="You execute plans precisely and report results"
           ),
           tools=[WebSearchTool(), CalculatorTool()],
           max_replanning_attempts=2,
           description="Plans and executes complex workflows"
       )

   
    # Pattern 4: Multi-Agent Collaboration
    class MultiAgentSystem:

       """Coordinate multiple agents for complex tasks.
       
       Best for: Tasks requiring different expertise or parallel processing

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       
       def __init__(self):
           # Create specialized agents
           self.researcher = SimpleAgent(
               name="Researcher",
               tools=[WebSearchTool()],
               engine=AugLLMConfig(model="gpt-4"),
               description="Gathers information"
           )
           
           self.analyst = SimpleAgent(
               name="Analyst",
               tools=[CalculatorTool(), CodeInterpreterTool()],
               engine=AugLLMConfig(model="gpt-4"),
               description="Analyzes data"
           )
           
           self.writer = SimpleAgent(
               name="Writer",
               engine=AugLLMConfig(
                   model="gpt-4",
                   temperature=0.8
               ),
               description="Creates content"
           )
           
           self.coordinator = SimpleAgent(
               name="Coordinator",
               engine=AugLLMConfig(model="gpt-4"),
               description="Coordinates other agents"
           )
       
       async def process_request(self, request: str) -> Dict[str, str]:
           """Process a request using multiple agents.
           
           Args:
               request: User request
               
           Returns:
               Results from each agent

""""""""""""""""""""""""""""""""""""""
           # Coordinator creates task breakdown
           task_breakdown = await self.coordinator.ainvoke(
               f"Break down this request into tasks for Researcher, Analyst, and Writer: {request}"
           )
           
           # Execute tasks in parallel where possible
           research_task = self.researcher.ainvoke(
               f"Research: {request}"
           )
           
           research_results = await research_task
           
           # Analyst uses research results
           analysis_task = self.analyst.ainvoke(
               f"Analyze this research: {research_results}"
           )
           
           analysis_results = await analysis_task
           
           # Writer creates final output
           writing_task = self.writer.ainvoke(
               f"Create a report based on:\nResearch: {research_results}\nAnalysis: {analysis_results}"
           )
           
           final_report = await writing_task
           
           return {
               "task_breakdown": task_breakdown,
               "research": research_results,
               "analysis": analysis_results,
               "final_report": final_report
           }

   
    # Demonstration of patterns
    def demo_agent_patterns():

       """Demonstrate different agent patterns."""
       
       print("🎭 Agent Design Patterns Demo\n")
       
       # Pattern 1: ReAct
       print("1️⃣ ReAct Pattern Demo")
       print("Use case: Solving multi-step problems\n")
       
       react_agent = create_react_problem_solver()
       problem = "What would be the total cost to drive from NYC to LA, including gas, "
       problem += "assuming 28 mpg, current gas prices, and 2,800 miles?"
       
       print(f"Problem: {problem}")
       solution = react_agent.invoke(problem)
       print(f"Solution: {solution[:300]}...\n")
       print("-"*** * 80 + "\n")*
       
       # Pattern 2: Plan-Execute
       print("2️⃣ Plan-Execute Pattern Demo")
       print("Use case: Complex projects requiring planning\n")
       
       planner = create_plan_execute_agent()
       project = "Create a comprehensive market analysis for launching a new coffee shop in Seattle"
       
       print(f"Project: {project}")
       result = planner.invoke(project)
       print(f"Execution Result: {result[:300]}...\n")
       print("-"* * 80 + "\n")
       
       # Pattern 3: Multi-Agent
       print("3️⃣ Multi-Agent Pattern Demo")
       print("Use case: Complex tasks requiring multiple expertise\n")
       
       async def run_multi_agent_demo():
           system = MultiAgentSystem()
           request = "Analyze the impact of AI on job markets in the next 5 years"
           
           print(f"Request: {request}")
           results = await system.process_request(request)
           
           print("\nResults from each agent:")
           print(f"📊 Task Breakdown: {results['task_breakdown'][:150]}...")
           print(f"🔍 Research: {results['research'][:150]}...")
           print(f"📈 Analysis: {results['analysis'][:150]}...")
           print(f"📝 Final Report: {results['final_report'][:200]}...")
       
       asyncio.run(run_multi_agent_demo())

   
    # Pattern selection guide
    def print_pattern_guide():

       """Print a guide for selecting agent patterns."""
       
       print("\n📚 Agent Pattern Selection Guide\n")
       
       patterns = [
           {
               "pattern": "SimpleAgent",
               "best_for": "Basic Q&A, single-turn interactions, simple tasks",
               "example": "Chatbots, FAQ systems, simple assistants"
           },
           {
               "pattern": "ReactAgent",
               "best_for": "Multi-step reasoning, tool use, problem solving",
               "example": "Research tasks, calculations, data analysis"
           },
           {
               "pattern": "RAGAgent",
               "best_for": "Knowledge-intensive tasks, Q&A over documents",
               "example": "Documentation assistant, knowledge base Q&A"
           },
           {
               "pattern": "PlanExecuteAgent",
               "best_for": "Complex workflows, project planning, systematic execution",
               "example": "Project management, multi-stage analysis"
           },
           {
               "pattern": "Multi-Agent",
               "best_for": "Tasks requiring different expertise, parallel processing",
               "example": "Research reports, complex analysis, content creation"
           }
       ]
       
       for p in patterns:
           print(f"🎯 {p['pattern']}")
           print(f"   Best for: {p['best_for']}")
           print(f"   Example: {p['example']}\n")

   
    if __name__ == "__main__":

       demo_agent_patterns()
       print_pattern_guide()

    Production Best Practices

    -------------------------

    🚀 Example 6: Production-Ready Agent Implementation

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # pycon_building_agents_06.py
    """Production-Ready Agent Implementation

    This example shows best practices for deploying agents in production
    including error handling, monitoring, caching, and scaling.   """"""""""""""""""""""""""""""""""""""""""""""""""""""

    from haive.agents import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.cache import ResponseCache
    from haive.core.monitoring import AgentMonitor
    import logging
    import asyncio
    from typing import Optional, Dict, Any, List
    from datetime import datetime
    import json
    from dataclasses import dataclass
    import redis
    from functools import wraps
    import time

    # Configure logging
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    @dataclass
    class AgentMetrics:
    """Metrics for agent performance."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    total_tokens_used: int = 0

    class ProductionAgent:
    """Production-ready agent with monitoring and caching."""

    def __init__(self,
    name: str,
    model: str = "gpt-4",
    redis_url: Optional[str] = None,
    cache_ttl: int = 3600,
    max_retries: int = 3,
    timeout: int = 30):
    """Initialize production agent.

    Args:
    name: Agent name
    model: LLM model
    redis_url: Redis URL for caching
    cache_ttl: Cache time-to-live in seconds
    max_retries: Maximum retry attempts
    timeout: Request timeout in seconds

""""""""""""""""""""""""""""""""""""""""""""""""""
           self.name = name
           self.model = model
           self.max_retries = max_retries
           self.timeout = timeout
           self.metrics = AgentMetrics()
           
           # Initialize cache
           self.cache = None
           if redis_url:
               try:
                   self.redis_client = redis.from_url(redis_url)
                   self.cache_ttl = cache_ttl
                   logger.info(f"Redis cache initialized for {name}")
               except Exception as e:
                   logger.warning(f"Failed to initialize Redis: {e}")
           
           # Create agent
           self.agent = SimpleAgent(
               name=name,
               engine=AugLLMConfig(
                   model=model,
                   temperature=0.7,
                   timeout=timeout,
                   max_tokens=500
               )
           )
           
           # Initialize monitor
           self.monitor = AgentMonitor(agent_name=name)
       
       def _get_cache_key(self, prompt: str) -> str:
           """Generate cache key for prompt."""
           return f"agent:{self.name}:prompt:{hash(prompt)}"
       
       def _get_from_cache(self, prompt: str) -> Optional[str]:
           """Get response from cache."""
           if not self.redis_client:
               return None
           
           try:
               key = self._get_cache_key(prompt)
               cached = self.redis_client.get(key)
               if cached:
                   self.metrics.cache_hits += 1
                   logger.debug(f"Cache hit for prompt: {prompt[:50]}...")
                   return cached.decode('utf-8')
               else:
                   self.metrics.cache_misses += 1
                   return None
           except Exception as e:
               logger.error(f"Cache retrieval error: {e}")
               return None
       
       def _set_cache(self, prompt: str, response: str) -> None:
           """Set response in cache."""
           if not self.redis_client:
               return
           
           try:
               key = self._get_cache_key(prompt)
               self.redis_client.setex(
                   key,
                   self.cache_ttl,
                   response.encode('utf-8')
               )
               logger.debug(f"Cached response for prompt: {prompt[:50]}...")
           except Exception as e:
               logger.error(f"Cache storage error: {e}")
       
       def _with_retry(func):
           """Decorator for retry logic."""
           @wraps(func)
           async def wrapper(self,* *args,* **kwargs):**
               last_error = None
               for attempt in range(self.max_retries):
                   try:
                       return await func(self,*** *args,* **kwargs)
                   except Exception as e:
                       last_error = e
                       wait_time = 2*** ** attempt  # Exponential backoff
                       logger.warning(
                           f"Attempt {attempt + 1} failed: {e}. "
                           f"Retrying in {wait_time}s..."
                       )
                       await asyncio.sleep(wait_time)
               
               raise last_error
           return wrapper
       
       @_with_retry
       async def process(self, prompt: str) -> str:
           """Process a prompt with full production features.
           
           Args:
               prompt: Input prompt
               
           Returns:
               Agent response

"""""""""""""""""""""""""""""
           start_time = time.time()
           self.metrics.total_requests += 1
           
           try:
               # Check cache first
               cached_response = self._get_from_cache(prompt)
               if cached_response:
                   self.metrics.successful_requests += 1
                   return cached_response
               
               # Monitor start
               self.monitor.record_request_start(prompt)
               
               # Process with agent
               response = await self.agent.ainvoke(prompt)
               
               # Cache response
               self._set_cache(prompt, response)
               
               # Update metrics
               response_time = time.time() - start_time
               self.metrics.successful_requests += 1
               self.metrics.average_response_time = (
                   (self.metrics.average_response_time*** * (self.metrics.successful_requests - 1) + response_time)*
                   / self.metrics.successful_requests
               )
               
               # Monitor end
               self.monitor.record_request_end(response, response_time)
               
               logger.info(
                   f"Processed request in {response_time:.2f}s "
                   f"(cache: {'hit' if cached_response else 'miss'})"
               )
               
               return response
               
           except Exception as e:
               self.metrics.failed_requests += 1
               self.monitor.record_error(str(e))
               logger.error(f"Error processing request: {e}")
               raise
       
       def get_metrics(self) -> Dict[str, Any]:
           """Get current metrics."""
           return {
               "agent_name": self.name,
               "total_requests": self.metrics.total_requests,
               "successful_requests": self.metrics.successful_requests,
               "failed_requests": self.metrics.failed_requests,
               "success_rate": (
                   self.metrics.successful_requests / self.metrics.total_requests
                   if self.metrics.total_requests > 0 else 0
               ),
               "average_response_time": round(self.metrics.average_response_time, 2),
               "cache_hit_rate": (
                   self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses)
                   if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0
               )
           }
       
       def health_check(self) -> Dict[str, Any]:
           """Perform health check."""
           health = {
               "status": "healthy",
               "timestamp": datetime.now().isoformat(),
               "agent": self.name,
               "issues": []
           }
           
           # Check cache connection
           if self.redis_client:
               try:
                   self.redis_client.ping()
               except:
                   health["issues"].append("Cache connection failed")
           
           # Check error rate
           if self.metrics.total_requests > 10:
               error_rate = self.metrics.failed_requests / self.metrics.total_requests
               if error_rate > 0.1:  # 10% error threshold
                   health["status"] = "degraded"
                   health["issues"].append(f"High error rate: {error_rate:.1%}")
           
           # Check response time
           if self.metrics.average_response_time > 10:  # 10 second threshold
               health["status"] = "degraded"
               health["issues"].append(
                   f"Slow response time: {self.metrics.average_response_time:.1f}s"
               )
           
           return health

   
    # Demonstration
    async def demo_production_agent():

       """Demonstrate production agent features."""
       
       print("🏭 Production Agent Demo\n")
       
       # Create production agent
       agent = ProductionAgent(
           name="Production Assistant",
           model="gpt-4",
           redis_url=None,  # Set to "redis://localhost:6379" if available
           cache_ttl=3600,
           max_retries=3
       )
       
       # Test queries
       queries = [
           "What are the SOLID principles in software engineering?",
           "What are the SOLID principles in software engineering?",  # Duplicate for cache test
           "Explain microservices architecture",
           "What is the CAP theorem?"
       ]
       
       print("Processing queries...\n")
       
       for i, query in enumerate(queries, 1):
           print(f"Query {i}: {query}")
           try:
               response = await agent.process(query)
               print(f"Response: {response[:100]}...\n")
           except Exception as e:
               print(f"Error: {e}\n")
       
       # Display metrics
       print("\n📊 Agent Metrics")
       metrics = agent.get_metrics()
       for key, value in metrics.items():
           print(f"  {key}: {value}")
       
       # Health check
       print("\n🏥 Health Check")
       health = agent.health_check()
       print(f"  Status: {health['status']}")
       if health['issues']:
           print(f"  Issues: {', '.join(health['issues'])}")
       else:
           print("  Issues: None")

   
    # Scaling considerations
    class AgentPool:

       """Pool of agents for load balancing."""
       
       def __init__(self, pool_size: int = 5,* **agent_kwargs):**
           """Initialize agent pool."""
           self.agents = [
               ProductionAgent(
                   name=f"Agent-{i}",
                  *** **agent_kwargs
               )
               for i in range(pool_size)
           ]
           self.current_index = 0
       
       async def process(self, prompt: str) -> str:
           """Process using round-robin selection."""
           agent = self.agents[self.current_index]
           self.current_index = (self.current_index + 1) % len(self.agents)
           return await agent.process(prompt)
       
       def get_pool_metrics(self) -> List[Dict[str, Any]]:
           """Get metrics for all agents in pool."""
           return [agent.get_metrics() for agent in self.agents]

   
    if __name__ == "__main__":

       asyncio.run(demo_production_agent())

    Next Steps

    ----------

    Continue your journey with these advanced topics:

    - :doc:`agent_patterns` - Master advanced agent patterns like ReAct, RAG, and multi-agent systems

    - :doc:`custom_agents` - Create highly specialized agents for your domain
    - :doc:`using_tools` - Learn to create and integrate custom tools
    - :doc:`state_management` - Understand agent state and memory systems
    - :doc:`engine_system` - Deep dive into cognitive engines and LLM configuration

    .. tip::

   

    *** **Quick Reference Command***s**

   

.. code-block:: bash

    # Install Haive
    pip install haive-core haive-agents haive-tools

    # Run examples
    python pycon_building_agents_01.py  # Basic agent
    python pycon_building_agents_02.py  # Domain experts
    python pycon_building_agents_03.py  # Tool integration
    python pycon_building_agents_04.py  # Custom agents
    python pycon_building_agents_05.py  # Agent patterns
    python pycon_building_agents_06.py  # Production setup***
