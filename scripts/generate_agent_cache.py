#!/usr/bin/env python3
"""
Generate cached agent execution data for documentation demos.

This script runs agents with streaming to capture rich execution data
including state history, execution traces, and visualization data.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentExecutionCapture:
    """Captures comprehensive execution data from agent runs."""
    
    def __init__(self):
        self.execution_trace: List[Dict[str, Any]] = []
        self.state_history: List[Dict[str, Any]] = []
        self.graph_data: Dict[str, Any] = {}
        self.visualization_data: Dict[str, Any] = {}
        self.streaming_events: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
    def start_capture(self):
        """Start capturing execution data."""
        self.start_time = datetime.now()
        logger.info(f"🎬 Starting agent execution capture at {self.start_time}")
        
    def end_capture(self):
        """End capturing execution data."""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        logger.info(f"🎬 Finished agent execution capture. Duration: {duration:.2f}s")
        
    def capture_stream_event(self, event: Dict[str, Any]):
        """Capture a streaming event."""
        timestamp = datetime.now().isoformat()
        event_data = {
            "timestamp": timestamp,
            "event_type": event.get("event", "unknown"),
            "event_name": event.get("name", ""),
            "data": event.get("data", {}),
            "metadata": event.get("metadata", {})
        }
        self.streaming_events.append(event_data)
        
        # Extract specific data for visualization
        if event.get("event") == "on_chain_start":
            self.execution_trace.append({
                "step": len(self.execution_trace) + 1,
                "node": event.get("name", ""),
                "action": "start",
                "timestamp": timestamp,
                "data": event.get("data", {})
            })
            
        elif event.get("event") == "on_chain_end":
            self.execution_trace.append({
                "step": len(self.execution_trace) + 1,
                "node": event.get("name", ""),
                "action": "end",
                "timestamp": timestamp,
                "output": event.get("data", {}).get("output", {})
            })
            
    def capture_state_update(self, state: Dict[str, Any]):
        """Capture state update."""
        timestamp = datetime.now().isoformat()
        state_snapshot = {
            "timestamp": timestamp,
            "state": state.copy(),
            "step": len(self.state_history) + 1
        }
        self.state_history.append(state_snapshot)
        
    def capture_graph_data(self, graph_info: Dict[str, Any]):
        """Capture graph structure and visualization data."""
        self.graph_data = graph_info
        
    def capture_visualization_data(self, viz_data: Dict[str, Any]):
        """Capture visualization data from agent methods."""
        self.visualization_data.update(viz_data)
        
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            
        return {
            "execution_summary": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration_seconds": duration,
                "total_events": len(self.streaming_events),
                "total_steps": len(self.execution_trace),
                "state_updates": len(self.state_history)
            },
            "execution_trace": self.execution_trace,
            "state_history": self.state_history,
            "graph_data": self.graph_data,
            "visualization_data": self.visualization_data,
            "streaming_events": self.streaming_events
        }


async def run_simple_agent_with_streaming(input_text: str) -> Dict[str, Any]:
    """
    Run SimpleAgent with comprehensive streaming capture.
    
    Args:
        input_text: Input text for the agent
        
    Returns:
        Dictionary containing execution data, traces, and visualization
    """
    capture = AgentExecutionCapture()
    
    try:
        # Import SimpleAgent
        from haive.agents.simple import SimpleAgent
        from haive.core.engine.aug_llm import AugLLMConfig
        
        # Create agent with configuration
        config = AugLLMConfig(
            temperature=0.7,
            max_tokens=500,
            system_message="You are a helpful assistant demonstrating SimpleAgent capabilities."
        )
        
        agent = SimpleAgent(
            name="demo_simple_agent",
            engine=config
        )
        
        capture.start_capture()
        
        # Try to get graph visualization if available
        try:
            if hasattr(agent, 'get_graph'):
                graph = agent.get_graph()
                graph_info = {
                    "nodes": [],
                    "edges": [],
                    "has_graph": True
                }
                
                # Try to get Mermaid diagram if available
                try:
                    if hasattr(graph, 'draw_mermaid_png'):
                        graph_info["mermaid_available"] = True
                    if hasattr(graph, 'nodes'):
                        graph_info["nodes"] = list(graph.nodes.keys()) if hasattr(graph.nodes, 'keys') else []
                    if hasattr(graph, 'edges'):
                        graph_info["edges"] = list(graph.edges) if graph.edges else []
                except Exception as e:
                    logger.warning(f"Could not extract graph details: {e}")
                    
                capture.capture_graph_data(graph_info)
                
        except Exception as e:
            logger.warning(f"Agent doesn't have graph visualization: {e}")
            capture.capture_graph_data({"has_graph": False, "error": str(e)})
        
        # Run agent with timeout protection
        response = None
        
        # Use regular run method with timeout
        logger.info("Using regular run method with timeout")
        
        try:
            # Set timeout for LLM call
            response = await asyncio.wait_for(
                agent.arun(input_text) if hasattr(agent, 'arun') else asyncio.to_thread(agent.run, input_text),
                timeout=120.0  # 2 minute timeout
            )
        except asyncio.TimeoutError:
            logger.error("Agent execution timed out after 2 minutes")
            response = "Agent execution timed out - this would be a real response in production"
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            response = f"Agent execution failed: {e}"
        
        # Capture the response as a single event
        capture.capture_stream_event({
            "event": "agent_response",
            "name": "simple_agent_run",
            "data": {"output": response}
        })
        
        # Try to get visualization data from agent
        try:
            viz_data = {}
            
            # Check for visualization methods
            if hasattr(agent, 'get_visualization_data'):
                viz_data['visualization_data'] = agent.get_visualization_data()
                
            if hasattr(agent, 'get_graph_visualization'):
                viz_data['graph_visualization'] = agent.get_graph_visualization()
                
            if hasattr(agent, 'visualize'):
                viz_data['visualize_output'] = agent.visualize()
                
            # Check for state/memory access
            if hasattr(agent, 'get_state'):
                viz_data['final_state'] = agent.get_state()
                
            if hasattr(agent, 'conversation_history'):
                viz_data['conversation_history'] = getattr(agent, 'conversation_history', [])
                
            capture.capture_visualization_data(viz_data)
            
        except Exception as e:
            logger.warning(f"Could not extract visualization data: {e}")
            capture.capture_visualization_data({"error": str(e)})
        
        # Capture final state
        capture.capture_state_update({
            "input": input_text,
            "output": response,
            "agent_name": agent.name,
            "status": "completed"
        })
        
        capture.end_capture()
        
        # Return comprehensive execution data
        result = capture.get_summary()
        result["agent_output"] = response
        
        return result
        
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        capture.end_capture()
        
        # Return error data
        result = capture.get_summary()
        result["error"] = str(e)
        result["agent_output"] = None
        
        return result


async def run_react_agent_with_streaming(input_text: str) -> Dict[str, Any]:
    """
    Run ReactAgent with comprehensive streaming capture and tool calls.
    
    Args:
        input_text: Input text for the agent
        
    Returns:
        Dictionary containing execution data, traces, and tool call information
    """
    capture = AgentExecutionCapture()
    
    try:
        # Import ReactAgent and create tools
        from haive.agents.react import ReactAgent
        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.tools import tool
        
        # Create tools for ReactAgent
        @tool
        def calculator(expression: str) -> str:
            """Calculate mathematical expressions safely."""
            try:
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"Error: {e}"
        
        @tool
        def word_counter(text: str) -> str:
            """Count words in the provided text."""
            words = text.split()
            return f"Word count: {len(words)}"
        
        # Create agent with configuration and tools
        config = AugLLMConfig(
            temperature=0.3,
            max_tokens=500,
            system_message="You are a helpful assistant with access to tools. Think step by step and use tools when appropriate."
        )
        
        agent = ReactAgent(
            name="demo_react_agent",
            engine=config,
            tools=[calculator, word_counter]
        )
        
        capture.start_capture()
        
        # Try to get graph visualization
        try:
            if hasattr(agent, 'get_graph'):
                graph = agent.get_graph()
                graph_info = {
                    "has_graph": True,
                    "nodes": [],
                    "edges": [],
                    "graph_type": "react_agent"
                }
                
                # Extract graph structure
                if hasattr(graph, 'nodes'):
                    graph_info["nodes"] = [
                        {"id": node, "type": "agent_node" if "agent" in node else "tool_node"} 
                        for node in graph.nodes
                    ]
                if hasattr(graph, 'edges'):
                    graph_info["edges"] = [
                        {"from": edge[0], "to": edge[1]} 
                        for edge in graph.edges
                    ]
                    
                capture.capture_graph_data(graph_info)
                
        except Exception as e:
            logger.warning(f"Could not extract graph data: {e}")
            capture.capture_graph_data({"has_graph": False, "error": str(e)})
        
        # Run agent with timeout protection
        response = None
        
        try:
            # Use astream to capture intermediate steps
            logger.info("Using astream to capture tool calls and reasoning")
            
            steps = []
            async for chunk in agent.astream(input_text, stream_mode="values"):
                step_data = {
                    "timestamp": datetime.now().isoformat(),
                    "messages": [msg.dict() if hasattr(msg, 'dict') else str(msg) for msg in chunk.get("messages", [])],
                    "has_tool_calls": any(hasattr(msg, 'tool_calls') and msg.tool_calls for msg in chunk.get("messages", [])),
                    "step_number": len(steps) + 1
                }
                steps.append(step_data)
                
                # Capture streaming event
                capture.capture_stream_event({
                    "event": "agent_step",
                    "name": "react_agent_stream",
                    "data": step_data
                })
                
                # Extract final response if available
                if chunk.get("messages"):
                    last_msg = chunk["messages"][-1]
                    if hasattr(last_msg, 'content'):
                        response = last_msg.content
                        
        except Exception as e:
            logger.error(f"Streaming failed, trying regular execution: {e}")
            
            # Fallback to regular execution
            response = await asyncio.wait_for(
                agent.arun(input_text),
                timeout=120.0
            )
            
            capture.capture_stream_event({
                "event": "agent_response",
                "name": "react_agent_fallback",
                "data": {"output": response}
            })
        
        # Try to get visualization data
        try:
            viz_data = {}
            
            # Get conversation history
            if hasattr(agent, 'conversation_history'):
                viz_data['conversation_history'] = getattr(agent, 'conversation_history', [])
            
            # Get state information
            if hasattr(agent, 'get_state'):
                viz_data['final_state'] = agent.get_state()
            
            # Extract tool calls from messages
            tool_calls = []
            if hasattr(agent, 'get_messages'):
                messages = agent.get_messages()
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for call in msg.tool_calls:
                            tool_calls.append({
                                "tool_name": call.get("name"),
                                "tool_args": call.get("args"),
                                "tool_id": call.get("id")
                            })
            
            viz_data['tool_calls'] = tool_calls
            viz_data['total_tool_calls'] = len(tool_calls)
            
            capture.capture_visualization_data(viz_data)
            
        except Exception as e:
            logger.warning(f"Could not extract visualization data: {e}")
            capture.capture_visualization_data({"error": str(e)})
        
        # Capture final state
        capture.capture_state_update({
            "input": input_text,
            "output": response,
            "agent_name": agent.name,
            "agent_type": "react",
            "tools_used": ["calculator", "word_counter"],
            "status": "completed"
        })
        
        capture.end_capture()
        
        # Return comprehensive execution data
        result = capture.get_summary()
        result["agent_output"] = response
        result["agent_type"] = "react"
        
        return result
        
    except Exception as e:
        logger.error(f"Error during ReactAgent execution: {e}")
        capture.end_capture()
        
        # Return error data
        result = capture.get_summary()
        result["error"] = str(e)
        result["agent_output"] = None
        result["agent_type"] = "react"
        
        return result


async def generate_simple_agent_cache():
    """Generate cached execution data for SimpleAgent."""
    
    logger.info("🚀 Starting SimpleAgent cache generation")
    
    # Example inputs to test with (reduced to 1 for initial testing)
    test_inputs = [
        "Hello! Can you introduce yourself and explain what you can do?"
    ]
    
    cache_data = {
        "agent_type": "simple",
        "agent_name": "SimpleAgent",
        "agent_class": "haive.agents.simple.SimpleAgent",
        "generated_at": datetime.now().isoformat(),
        "executions": []
    }
    
    for i, input_text in enumerate(test_inputs):
        logger.info(f"🎯 Running execution {i+1}/{len(test_inputs)}: {input_text[:50]}...")
        
        execution_data = await run_simple_agent_with_streaming(input_text)
        execution_data["execution_id"] = f"simple_agent_demo_{i+1}"
        execution_data["input_text"] = input_text
        
        cache_data["executions"].append(execution_data)
        
        # Add delay between executions
        await asyncio.sleep(1)
        
        logger.info(f"✅ Execution {i+1} completed successfully")
    
    # Save to file
    cache_file = Path(__file__).parent.parent / "docs" / "source" / "agent_cache_simple.json"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, default=str)
    
    logger.info(f"✅ SimpleAgent cache saved to {cache_file}")
    
    return cache_data


async def generate_react_agent_cache():
    """Generate cached execution data for ReactAgent."""
    
    logger.info("🚀 Starting ReactAgent cache generation")
    
    # Example inputs that will trigger tool usage
    test_inputs = [
        "What is 15 * 23 + 47? Please calculate step by step.",
        "Count the words in this sentence: 'The quick brown fox jumps over the lazy dog'",
        "Can you help me with a math problem? Calculate (100 - 25) * 3 and then tell me how many words are in your explanation."
    ]
    
    cache_data = {
        "agent_type": "react",
        "agent_name": "ReactAgent",
        "agent_class": "haive.agents.react.ReactAgent",
        "generated_at": datetime.now().isoformat(),
        "executions": []
    }
    
    for i, input_text in enumerate(test_inputs):
        logger.info(f"🎯 Running execution {i+1}/{len(test_inputs)}: {input_text[:50]}...")
        
        execution_data = await run_react_agent_with_streaming(input_text)
        execution_data["execution_id"] = f"react_agent_demo_{i+1}"
        execution_data["input_text"] = input_text
        
        cache_data["executions"].append(execution_data)
        
        # Add delay between executions
        await asyncio.sleep(2)
        
        logger.info(f"✅ Execution {i+1} completed successfully")
    
    # Save to file
    cache_file = Path(__file__).parent.parent / "docs" / "source" / "agent_cache_react.json"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, default=str)
    
    logger.info(f"✅ ReactAgent cache saved to {cache_file}")
    
    return cache_data


if __name__ == "__main__":
    import sys
    
    # Determine which agent to generate cache for
    agent_type = sys.argv[1] if len(sys.argv) > 1 else "simple"
    
    if agent_type == "simple":
        logger.info("🚀 Generating SimpleAgent cache")
        cache_data = asyncio.run(generate_simple_agent_cache())
    elif agent_type == "react":
        logger.info("🚀 Generating ReactAgent cache")
        cache_data = asyncio.run(generate_react_agent_cache())
    else:
        logger.error(f"Unknown agent type: {agent_type}. Use 'simple' or 'react'")
        sys.exit(1)
    
    print(f"\n🎉 {agent_type.title()}Agent cache generation complete!")
    print(f"Generated {len(cache_data['executions'])} executions")
    print(f"Total events captured: {sum(len(exec['streaming_events']) for exec in cache_data['executions'])}")
    
    # Print summary
    for i, execution in enumerate(cache_data['executions']):
        print(f"\nExecution {i+1}:")
        print(f"  Input: {execution['input_text'][:50]}...")
        print(f"  Duration: {execution['execution_summary']['duration_seconds']:.2f}s")
        print(f"  Events: {execution['execution_summary']['total_events']}")
        print(f"  Steps: {execution['execution_summary']['total_steps']}")
        if execution.get('agent_type') == 'react':
            viz_data = execution.get('visualization_data', {})
            tool_calls = viz_data.get('total_tool_calls', 0)
            print(f"  Tool Calls: {tool_calls}")
            
    print(f"\n✅ Cache saved to agent_cache_{agent_type}.json")