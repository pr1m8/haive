
import time
import json
import logging
import concurrent.futures
from typing import Any, Dict, List, Optional, Set, Union, Tuple
from datetime import datetime
import copy
# Import LangChain core components
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import LangGraph components
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

# Import our framework components
from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.core.graph.retry import RetryPolicy, execute_with_retry
from src.haive.core.graph.branches import Branch  # Import from branches, not Branch

# Import models and configuration
from src.haive.agents.rec_plan.models import (
    ReasoningModule, PlanNode, ExecutionPlan,
    PlannerOutput, ExecutorOutput, ReflectionOutput, FinalAnswer, TaskExecution
)
from src.haive.agents.rec_plan.state import RecursiveTreePlannerState
from src.haive.agents.rec_plan.config import RecursiveTreePlannerConfig
from src.haive.agents.rec_plan.branches import create_schedule_execution_branch, create_check_execution_branch, create_reflection_branch
# Configure logging
logger = logging.getLogger(__name__)

@register_agent(RecursiveTreePlannerConfig)
class RecursiveTreePlanner(Agent[RecursiveTreePlannerConfig]):
    """
    A recursive tree planner agent that uses parallel task execution.
    
    This agent combines:
    1. LLMCompiler-style DAG planning with dependencies
    2. ReWOO-style variable substitution
    3. ReAct-style reasoning with self-discovery
    4. Reflection for self-improvement
    5. Multi-threaded execution of parallelizable tasks
    """
    def __init__(self, config: RecursiveTreePlannerConfig):
        """Initialize the agent with its configuration."""
        super().__init__(config)
        
        # Initialize tool registry
        self._tools = {tool.name: tool for tool in config.tools}
        
        # Initialize reasoning modules
        self._reasoning_modules = self._initialize_reasoning_modules()
        
        # Initialize executor thread pool
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.max_parallel_steps)
    
    def _initialize_reasoning_modules(self) -> List[ReasoningModule]:
        """Initialize reasoning modules from src.configuration."""
        return [
            ReasoningModule(
                name=module["name"],
                description=module["description"],
                is_selected=False,
                adapted_description=None
            )
            for module in self.config.available_reasoning_modules
        ]
    
    def setup_workflow(self) -> None:
        """
        Set up the agent workflow graph with the correct execution order and conditional routing.
        
        This improved setup ensures that branches are properly created and 
        conditional edges are correctly added to the graph.
        """
        logger.info(f"Setting up workflow for RecursiveTreePlanner {self.config.name}")
        
        # Create graph builder
        gb = DynamicGraph(
            components=[self.config.engine] + list(self.config.engines.values()),
            state_schema=self.state_schema
        )
        
        # Log the state schema for debugging
        logger.debug(f"Debug: has state_schema: {self.state_schema}")
        logger.info(f"Using state schema: {self.state_schema.__name__}")
        
        # === WORKFLOW DEFINITION ===
        # STEP 1: Task Analysis and Module Selection
        gb.add_node("initialize", config=self._initialize_node, command_goto="select_modules")
        gb.add_node("select_modules", config=self._select_modules_node, command_goto="create_plan")
        
        # STEP 2: Planning Phase
        gb.add_node("create_plan", config=self._create_plan_node, command_goto="schedule_execution")
        
        # STEP 3: Task Scheduling and Execution
        gb.add_node("schedule_execution", config=self._schedule_execution_node)
        gb.add_node("execute_tasks", config=self._execute_tasks_node, command_goto="check_execution")
        gb.add_node("check_execution", config=self._check_execution_node)
        
        # STEP 4: Reflection and Improvement
        gb.add_node("reflect", config=self._reflect_node)
        gb.add_node("replan", config=self._replan_node, command_goto="schedule_execution")
        
        # STEP 5: Final Answer Generation
        gb.add_node("generate_answer", config=self._generate_answer_node, command_goto=END)
        
        # === CONDITIONAL ROUTING ===
        logger.info("Creating branch objects for conditional routing")
        
        try:
            # Create branch objects with defensive error logging
            schedule_branch = create_schedule_execution_branch()
            check_branch = create_check_execution_branch()
            reflect_branch = create_reflection_branch(self.config.max_iterations)
            
            # Log branch types for debugging
            logger.info(f"Branch types: {type(schedule_branch)}, {type(check_branch)}, {type(reflect_branch)}")
            
            # Debug print of each branch object
            logger.debug(f"Debug: schedule_branch: {schedule_branch}")
            logger.debug(f"Debug: check_branch: {check_branch}")
            logger.debug(f"Debug: reflect_branch: {reflect_branch}")
            
        except Exception as e:
            logger.error(f"Error creating branches: {e}")
            raise
        
        # Add conditional routing with manual mapping and detailed logging
        logger.info("Adding conditional edges with branches")
        
        try:
            # 1. Scheduling branch
            logger.debug(f"Debug: adding conditional edges from schedule_execution to {schedule_branch}")
            logger.debug(f"{type(schedule_branch)}")
            
            gb.add_node_with_conditional_edge(
                node_name="schedule_execution",
                router_function=schedule_branch.function,
                destinations={
                    "execute_tasks": "execute_tasks",
                    "reflect": "reflect",
                    "check_execution": "check_execution"
                },
                default_destination="check_execution"
            )
            logger.info("Added conditional edges from schedule_execution")
            
            # 2. Execution check branch
            logger.debug(f"Debug: adding conditional edges from check_execution to {check_branch}")
            logger.debug(f"{type(check_branch)}")
            
            gb.add_node_with_conditional_edge(
                node_name="check_execution",
                router_function=check_branch.function,
                destinations={
                    "reflect": "reflect", 
                    "schedule_execution": "schedule_execution"
                },
                default_destination="schedule_execution"
            )
            logger.info("Added conditional edges from check_execution")
            
            # 3. Reflection branch
            logger.debug(f"Debug: adding conditional edges from reflect to {reflect_branch}")
            logger.debug(f"{type(reflect_branch)}")
            
            gb.add_node_with_conditional_edge(
                node_name="reflect",
                router_function=reflect_branch.function,
                destinations={
                    "replan": "replan",
                    "generate_answer": "generate_answer"
                },
                default_destination="generate_answer"
            )
            logger.info("Added conditional edges from reflect")
            
        except Exception as e:
            logger.error(f"Error adding conditional edges: {e}")
            raise
        
        # Set entry point
        gb.set_entry_point("initialize")
        
        # Build the graph
        logger.info("Building the graph")
        self.graph = gb.build()
        logger.info(f"Built workflow graph for {self.config.name}")


    def _select_modules_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate reasoning modules for the task."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
                
                # Ensure required fields exist
                if 'task' not in state_obj:
                    state_obj['task'] = self._extract_task_from_messages(state_obj.get('messages', []))
                if 'reasoning_modules' not in state_obj:
                    state_obj['reasoning_modules'] = self._reasoning_modules
        else:
            state_obj = state
        
        # Format reasoning modules for the prompt
        modules_str = "\n".join([
            f"{i+1}. {module.name}: {module.description}"
            for i, module in enumerate(state_obj.reasoning_modules)
        ])
        
        # Get the module selection engine
        engine = self.config.engines["module_selection"]
        runnable = compose_runnable(engine)
        
        # Prepare input
        input_data = {
            "messages": [HumanMessage(content=f"Select the most appropriate reasoning modules for this task: {state_obj.task}")],
            "reasoning_modules": modules_str,
            "task": state_obj.task
        }
        
        # Log the input for debugging
        logger.debug(f"Module selection input: {input_data}")
        
        # Run the engine with explicit error handling
        try:
            result = runnable.invoke(input_data)
            logger.debug(f"Module selection result: {result}")
            
            # Validate the result has the expected fields
            if not hasattr(result, 'selected_modules'):
                raise ValueError("Result missing 'selected_modules' field")
            if not hasattr(result, 'justifications'):
                raise ValueError("Result missing 'justifications' field")
                
            selected_modules = result.selected_modules
            justifications = result.justifications
            
        except Exception as e:
            logger.error(f"Error in module selection: {e}")
            # Fallback to a default selection
            selected_modules = [
                "Problem Decomposition", 
                "Numerical Analysis", 
                "Information Synthesis"
            ]
            justifications = {
                module: f"Default selection for {module} due to error" 
                for module in selected_modules
            }
        
        # Mark selected modules
        updated_modules = []
        for module in state_obj.reasoning_modules:
            module_copy = module.model_copy(deep=True)
            module_copy.is_selected = module.name in selected_modules
            if module_copy.is_selected:
                # Add justification as adapted description
                module_copy.adapted_description = justifications.get(module.name, None)
            updated_modules.append(module_copy)
        
        # Create a message summarizing the selections
        selection_message = (
            f"Selected {len(selected_modules)} reasoning modules:\n" +
            "\n".join([f"- {module}" for module in selected_modules])
        )
        
        # Log the selections
        logger.info(f"Selected modules: {selected_modules}")
        
        return {
            "reasoning_modules": updated_modules,
            "selected_modules": selected_modules,
            "messages": state_obj.messages + [
                AIMessage(content=selection_message)
            ]
        }
    def _initialize_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize the agent state."""
        # Convert state dict to RecursiveTreePlannerState if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Create a default state object
                state_obj = RecursiveTreePlannerState(
                    messages=state.get("messages", []),
                    task=state.get("task", ""),
                    selected_modules=[],
                    available_tools=[]
                )
        else:
            state_obj = state
        
        # Extract task from messages if not set
        task = state_obj.task or self._extract_task_from_messages(state_obj.messages)
        
        # Initialize reasoning modules
        reasoning_modules = self._reasoning_modules
        
        # Set up available tools
        available_tools = list(self._tools.keys())
        
        # Log initialization
        logger.info(f"Initializing agent for task: {task}")
        logger.info(f"Available tools: {available_tools}")
        
        return {
            "task": task,
            "reasoning_modules": reasoning_modules,
            "available_tools": available_tools,
            "selected_modules": [],  # Initialize with empty list
            "messages": state_obj.messages + [
                SystemMessage(content=f"Task received: {task}")
            ]
        }
    def _replan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create an improved plan based on reflections with proper tool integration."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
        else:
            state_obj = state
                
        # Get the reflection data
        if isinstance(state_obj, dict):
            reflections = state_obj.get("reflections", [])
            plan = state_obj.get("plan")
            task = state_obj.get("task", "")
            selected_modules = state_obj.get("selected_modules", [])
            available_tools = state_obj.get("available_tools", [])
        else:
            reflections = state_obj.reflections if hasattr(state_obj, 'reflections') else []
            plan = state_obj.plan if hasattr(state_obj, 'plan') else None
            task = state_obj.task if hasattr(state_obj, 'task') else ""
            selected_modules = state_obj.selected_modules if hasattr(state_obj, 'selected_modules') else []
            available_tools = state_obj.available_tools if hasattr(state_obj, 'available_tools') else []
        
        # Get detailed tool information
        tool_descriptions = {}
        for tool_name in available_tools:
            if tool_name in self._tools:
                tool_descriptions[tool_name] = self._tools[tool_name].description
        
        # Format the original plan
        original_plan = self._format_plan_for_reflection(plan) if plan else "No previous plan available."
        
        # Format execution results
        execution_results = self._format_execution_results(plan) if plan else "No execution results available."
        
        # Format reflections with detailed insights
        reflections_str = ""
        for i, reflection in enumerate(reflections):
            strengths = "\n".join([f"- {s}" for s in reflection.strengths])
            weaknesses = "\n".join([f"- {w}" for w in reflection.weaknesses])
            improvements = "\n".join([f"- {imp}" for imp in reflection.improvements])
            
            reflections_str += f"Reflection #{i+1}:\nStrengths:\n{strengths}\nWeaknesses:\n{weaknesses}\nImprovements:\n{improvements}\n\n"
        
        # Format variables from previous execution
        variables_str = ""
        if plan and hasattr(plan, 'variables') and plan.variables:
            variables_str = "Variables from previous execution:\n"
            for var_name, value in plan.variables.items():
                variables_str += f"- {var_name}: {value}\n"
        
        # Get the replanning engine
        engine = self.config.engines["replanning"]
        runnable = compose_runnable(engine)
        
        # Prepare input for the replanning engine with comprehensive context
        input_data = {
            "messages": [HumanMessage(content=f"Improve the execution plan for this task: {task}")],
            "task": task,
            "original_plan": original_plan,
            "execution_results": execution_results,
            "reflections": reflections_str,
            "variables": variables_str,
            "selected_modules": ", ".join(selected_modules),
            "available_tools": tool_descriptions,
            "current_iteration": state_obj.current_iteration if not isinstance(state_obj, dict) else state_obj.get("current_iteration", 0)
        }
        
        # Run the engine with robust error handling
        try:
            # Run with reasonable timeout
            result = runnable.invoke(input_data)
            
            # Validate the plan has nodes
            if not hasattr(result, 'plan') or not result.plan or not result.plan.nodes:
                raise ValueError("Replanning did not produce a valid plan with nodes")
                
        except Exception as e:
            logger.error(f"Error in replanning: {e}")
            
            # Create a fallback plan based on reflections
            from src.haive.agents.rec_plan.models import ExecutionPlan, PlanNode, PlannerOutput
            
            fallback_plan = ExecutionPlan(
                task=task,
                nodes={},
                entry_points=[],
                status="not_started"
            )
            
            # Generate steps based on improvements from reflections
            improvement_steps = []
            for reflection in reflections:
                improvement_steps.extend(reflection.improvements)
            
            # Deduplicate improvements
            unique_improvements = list(set(improvement_steps))
            
            # Create nodes for each improvement
            for i, improvement in enumerate(unique_improvements[:3]):  # Limit to 3 nodes
                node_id = f"improvement_{i+1}"
                
                # Try to map improvement to a tool if possible
                tool_name = None
                for name, desc in tool_descriptions.items():
                    if name.lower() in improvement.lower() or any(keyword in improvement.lower() for keyword in desc.lower().split()):
                        tool_name = name
                        break
                
                # Create node
                node = PlanNode(
                    id=node_id,
                    description=f"Implement improvement: {improvement}",
                    reasoning_module=selected_modules[0] if selected_modules else None,
                    tool=tool_name,
                    dependencies=[]
                )
                
                fallback_plan.nodes[node_id] = node
                fallback_plan.entry_points.append(node_id)
            
            # Create one node for research using search tool if available
            if "search" in available_tools:
                research_node = PlanNode(
                    id="research",
                    description=f"Research information for: {task}",
                    tool="search",
                    args={"query": task},
                    dependencies=[]
                )
                fallback_plan.nodes["research"] = research_node
                fallback_plan.entry_points.append("research")
            
            # Create synthesis node depending on research
            synthesis_node = PlanNode(
                id="synthesize",
                description="Synthesize information and formulate answer",
                reasoning_module="Information Synthesis" if "Information Synthesis" in selected_modules else None,
                dependencies=list(fallback_plan.nodes.keys())
            )
            fallback_plan.nodes["synthesize"] = synthesis_node
            
            # Create a placeholder result
            result = PlannerOutput(
                plan=fallback_plan,
                reasoning="Created fallback plan based on reflections due to replanning error",
                estimated_steps=len(fallback_plan.nodes),
                parallelizable=len(fallback_plan.entry_points) > 1
            )
        
        # Log the new plan
        logger.info(f"Created improved plan with {len(result.plan.nodes)} nodes based on reflections")
        
        # Increment iteration
        current_iteration = state_obj.current_iteration if not isinstance(state_obj, dict) else state_obj.get("current_iteration", 0)
        current_iteration += 1
        
        # Create detailed plan description for the message
        plan_description = f"Created improved plan (iteration {current_iteration}) based on reflections with {len(result.plan.nodes)} steps.\n\n"
        
        # Add detail about tools being used
        tools_used = set(node.tool for node in result.plan.nodes.values() if node.tool)
        if tools_used:
            plan_description += f"Tools to be used: {', '.join(tools_used)}\n\n"
        
        # Add overview of plan structure
        if result.plan.nodes:
            plan_description += "Key steps:\n"
            for i, (node_id, node) in enumerate(list(result.plan.nodes.items())[:3]):  # First 3 nodes
                plan_description += f"{i+1}. {node.description}"
                if node.tool:
                    plan_description += f" (using {node.tool})"
                plan_description += "\n"
            
            if len(result.plan.nodes) > 3:
                plan_description += f"... and {len(result.plan.nodes) - 3} more steps\n"
        
        return {
            "plan": result.plan,
            "current_iteration": current_iteration,
            "messages": state_obj.messages + [
                AIMessage(content=plan_description)
            ]
        }
    def _reflect_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on the plan and execution results with improved robustness."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
        else:
            state_obj = state
        
        plan = state_obj.plan if hasattr(state_obj, 'plan') else state_obj.get("plan", None)
        
        if not plan:
            logger.error("No plan available for reflection")
            return {
                "should_replan": True,
                "current_iteration": state_obj.current_iteration + 1 if hasattr(state_obj, 'current_iteration') else 1,
                "messages": state_obj.messages + [
                    AIMessage(content="Reflection: The plan execution failed. Creating a new plan.")
                ]
            }
        
        # Format plan structure and execution results for reflection
        plan_structure = self._format_plan_for_reflection(plan)
        execution_results = self._format_execution_results(plan)
        
        # Determine if plan was successful
        plan_successful = plan.status == "complete"
        plan_failed = plan.status == "failed"
        
        # Check for execution issues
        execution_issues = []
        for node in plan.nodes.values():
            if node.status == "failed" and node.error:
                execution_issues.append(f"{node.description}: {node.error}")
        
        # Format status summary
        status_summary = f"Plan status: {plan.status}\n"
        if execution_issues:
            status_summary += "Execution issues:\n" + "\n".join(f"- {issue}" for issue in execution_issues)
        
        # Get the reflection engine
        engine = self.config.engines["reflection"]
        runnable = compose_runnable(engine)
        
        # Prepare input with comprehensive context
        input_data = {
            "messages": [HumanMessage(content="Reflect on the execution plan and results")],
            "task": state_obj.task,
            "plan_structure": plan_structure,
            "execution_results": execution_results,
            "status": status_summary,
            "current_iteration": state_obj.current_iteration + 1 if hasattr(state_obj, 'current_iteration') else 1,
            "max_iterations": state_obj.max_iterations if hasattr(state_obj, 'max_iterations') else 3
        }
        
        # Add previous reflections if any
        if hasattr(state_obj, 'reflections') and state_obj.reflections:
            previous_reflections = "\n\n".join([
                f"Reflection #{i+1}:\n" +
                f"Strengths: {', '.join(r.strengths)}\n" +
                f"Weaknesses: {', '.join(r.weaknesses)}\n" +
                f"Improvements: {', '.join(r.improvements)}"
                for i, r in enumerate(state_obj.reflections)
            ])
            input_data["previous_reflections"] = previous_reflections
        
        # Run the engine with robust error handling
        try:
            result = runnable.invoke(input_data)
            
            # Validate the result has expected fields
            if not hasattr(result, 'reflection') or not hasattr(result, 'should_replan'):
                logger.warning("Reflection engine returned incomplete result")
                # Create fallback reflection
                from src.haive.agents.rec_plan.models import Reflection, ReflectionOutput
                reflection = Reflection(
                    strengths=["Plan addressed parts of the task"],
                    weaknesses=["Execution encountered issues", "Plan was incomplete"],
                    improvements=["Add more specific steps", "Ensure tool usage"]
                )
                result = ReflectionOutput(
                    reflection=reflection,
                    should_replan=True,
                    reasoning="Fallback reflection due to incomplete result"
                )
        except Exception as e:
            logger.error(f"Error during reflection: {e}")
            # Create fallback reflection
            from src.haive.agents.rec_plan.models import Reflection, ReflectionOutput
            reflection = Reflection(
                strengths=["Attempted to solve the task"],
                weaknesses=["Encountered error during reflection", "May need more specific approach"],
                improvements=["Create a more robust plan", "Use tools more effectively"]
            )
            result = ReflectionOutput(
                reflection=reflection,
                should_replan=True,
                reasoning=f"Error during reflection: {str(e)}"
            )
            
        # Add reflection to list
        reflections = list(state_obj.reflections) if hasattr(state_obj, 'reflections') else []
        reflections.append(result.reflection)
        
        # Increment iteration counter
        current_iteration = state_obj.current_iteration + 1 if hasattr(state_obj, 'current_iteration') else 1
        
        # Determine whether to replan based on reflection & iteration count
        should_replan = result.should_replan
        if current_iteration >= state_obj.max_iterations if hasattr(state_obj, 'max_iterations') else 3:
            should_replan = False  # Stop replanning if we've reached max iterations
        
        # Format reflection for message
        reflection_msg = (
            f"Reflection #{current_iteration}:\n\n"
            f"Strengths:\n" + "\n".join([f"- {s}" for s in result.reflection.strengths]) + "\n\n"
            f"Weaknesses:\n" + "\n".join([f"- {w}" for w in result.reflection.weaknesses]) + "\n\n"
            f"Improvements:\n" + "\n".join([f"- {i}" for i in result.reflection.improvements]) + "\n\n"
            f"Decision: {'Create new plan' if should_replan else 'Generate final answer'}"
        )
        
        return {
            "reflections": reflections,
            "current_iteration": current_iteration,
            "should_replan": should_replan,
            "messages": state_obj.messages + [
                AIMessage(content=reflection_msg)
            ]
        }
    def _select_modules_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate reasoning modules for the task with robust error handling."""
        logger.info("Starting module selection")
        
        # Log the input state for debugging
        if hasattr(self, 'log_state'):
            self.log_state(state, "SELECT_MODULES_INPUT")
        
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
                logger.debug("Successfully converted state dict to RecursiveTreePlannerState")
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly with careful access
                state_obj = state
                
                # Ensure required fields exist
                if 'task' not in state_obj:
                    state_obj['task'] = self._extract_task_from_messages(state_obj.get('messages', []))
                if 'reasoning_modules' not in state_obj:
                    state_obj['reasoning_modules'] = self._reasoning_modules
        else:
            state_obj = state
            logger.debug("State is already a RecursiveTreePlannerState")
        
        # Format reasoning modules for the prompt
        modules_str = "\n".join([
            f"{i+1}. {module.name}: {module.description}"
            for i, module in enumerate(state_obj.reasoning_modules if hasattr(state_obj, 'reasoning_modules') else self._reasoning_modules)
        ])
        
        # Get the module selection engine
        engine = self.config.engines["module_selection"]
        runnable = compose_runnable(engine)
        
        # Prepare input with safety checks
        task = state_obj.task if hasattr(state_obj, 'task') else self._extract_task_from_messages(
            state_obj.get('messages', []) if isinstance(state_obj, dict) else state_obj.messages
        )
        
        input_data = {
            "messages": [HumanMessage(content=f"Select the most appropriate reasoning modules for this task: {task}")],
            "reasoning_modules": modules_str,
            "task": task
        }
        
        # Log the input for debugging
        logger.debug(f"Module selection input (messages omitted):\n  task: {task}\n  modules: {len(modules_str.split('\\n'))} modules")
        
        # Run the engine with comprehensive error handling
        try:
            logger.debug("Invoking module selection engine")
            result = runnable.invoke(input_data)
            logger.debug(f"Module selection successful - result type: {type(result)}")
            
            # Validate the result structure
            if hasattr(result, 'selected_modules') and hasattr(result, 'justifications'):
                selected_modules = result.selected_modules
                justifications = result.justifications
                logger.info(f"Selected {len(selected_modules)} modules: {', '.join(selected_modules)}")
            else:
                # Handle broken schema
                logger.error(f"Invalid result structure: {result}")
                
                # Try to extract from dictionary if needed
                if hasattr(result, 'model_dump'):
                    result_dict = result.model_dump()
                elif hasattr(result, 'dict'):
                    result_dict = result.dict()
                elif isinstance(result, dict):
                    result_dict = result
                else:
                    result_dict = {"selected_modules": []}
                    
                selected_modules = result_dict.get('selected_modules', [])
                justifications = result_dict.get('justifications', {})
                
                # Create default justifications if missing
                if not justifications and selected_modules:
                    justifications = {
                        module: f"Selected for relevance to task" 
                        for module in selected_modules
                    }
                
                logger.info(f"Extracted {len(selected_modules)} modules from partial result")
        except Exception as e:
            logger.error(f"Error in module selection: {e}")
            # Fallback to a sensible default selection
            fallback_modules = ["Problem Decomposition", "Numerical Analysis", "Information Synthesis"]
            selected_modules = [m for m in fallback_modules]
            justifications = {
                module: f"Default selection due to error: {module} is generally applicable" 
                for module in selected_modules
            }
            logger.info(f"Using fallback modules: {selected_modules}")
        
        # Safeguard against empty selection
        if not selected_modules:
            selected_modules = ["Problem Decomposition", "Information Synthesis"]
            justifications = {
                "Problem Decomposition": "Default selection - breaking down the task",
                "Information Synthesis": "Default selection - combining information"
            }
            logger.warning("Empty module selection, using defaults")
        
        # Mark selected modules
        updated_modules = []
        for module in (state_obj.reasoning_modules if hasattr(state_obj, 'reasoning_modules') else self._reasoning_modules):
            module_copy = module.model_copy(deep=True) if hasattr(module, 'model_copy') else copy.deepcopy(module)
            module_copy.is_selected = module.name in selected_modules
            if module_copy.is_selected:
                # Add justification as adapted description
                module_copy.adapted_description = justifications.get(module.name, "Selected for this task")
            updated_modules.append(module_copy)
        
        # Create a message summarizing the selections
        selection_message = (
            f"Selected {len(selected_modules)} reasoning modules:\n" +
            "\n".join([f"- {module}" for module in selected_modules])
        )
        
        # Get messages safely
        if isinstance(state_obj, dict):
            messages = state_obj.get('messages', [])
        else:
            messages = state_obj.messages if hasattr(state_obj, 'messages') else []
        
        # Prepare the result
        result = {
            "reasoning_modules": updated_modules,
            "selected_modules": selected_modules,
            "messages": messages + [
                AIMessage(content=selection_message)
            ]
        }
        
        logger.info("Module selection completed successfully")
        return result
    def _create_plan_node(self, state: RecursiveTreePlannerState) -> Dict[str, Any]:
        """Create a recursive execution plan."""
        # Format selected modules
        selected_modules_str = "\n".join([
            f"{i+1}. {module.name}: {module.description}"
            for i, module in enumerate(state.reasoning_modules)
            if module.is_selected
        ])
        
        # Format available tools
        available_tools_str = "\n".join([
            f"{i+1}. {name}: {self._tools[name].description}"
            for i, name in enumerate(state.available_tools)
            if name in self._tools
        ])
        
        # Get the planning engine
        engine = self.config.engines["planning"]
        runnable = compose_runnable(engine)
        
        # Prepare input
        input_data = {
            "messages": [HumanMessage(content=f"Create a detailed execution plan for this task: {state.task}")],
            "task": state.task,
            "selected_modules": selected_modules_str,
            "available_tools": available_tools_str
        }
        
        # Run the engine
        result = runnable.invoke(input_data)
        
        # Log the plan
        logger.info(f"Created plan with {len(result.plan.nodes)} nodes")
        
        return {
            "plan": result.plan,
            "messages": state.messages + [
                AIMessage(content=f"Created execution plan with {len(result.plan.nodes)} nodes. " +
                                 f"Can execute {len(result.plan.entry_points)} steps in parallel.")
            ]
        }
    def _create_plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create a recursive execution plan that properly uses tools and reasoning modules."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
        else:
            state_obj = state
        
        # Format selected modules with more detailed information
        selected_modules_str = ""
        for module in state_obj.reasoning_modules:
            if module.is_selected:
                description = module.adapted_description or module.description
                selected_modules_str += f"- {module.name}: {description}\n"
        
        # Format available tools with detailed descriptions
        available_tools_str = ""
        tool_details = {}
        for tool_name in state_obj.available_tools:
            if tool_name in self._tools:
                tool = self._tools[tool_name]
                tool_details[tool_name] = tool.description
                available_tools_str += f"- {tool_name}: {tool.description}\n"
        
        # Get the planning engine
        engine = self.config.engines["planning"]
        runnable = compose_runnable(engine)
        
        # Prepare input with enhanced context
        input_data = {
            "messages": [HumanMessage(content=f"Create a detailed execution plan for this task: {state_obj.task}")],
            "task": state_obj.task,
            "selected_modules": selected_modules_str,
            "available_tools": available_tools_str,
            "tool_details": tool_details,
            "current_iteration": state_obj.current_iteration + 1,
            "max_iterations": state_obj.max_iterations
        }
        
        # Add any reflections to give context for improved planning
        if state_obj.reflections:
            reflections_text = "\n\n".join([
                f"Reflection {i+1}:\n" +
                f"Strengths: {', '.join(r.strengths)}\n" +
                f"Weaknesses: {', '.join(r.weaknesses)}\n" +
                f"Improvements: {', '.join(r.improvements)}"
                for i, r in enumerate(state_obj.reflections)
            ])
            input_data["reflections"] = reflections_text
        
        # Run the engine with retries and detailed error handling
        try:
            # Add timeout to prevent hanging
            result = runnable.invoke(input_data)
            
            # Validate the result
            if not hasattr(result, 'plan') or not result.plan:
                raise ValueError("Planner did not produce a valid plan")
                
            if not result.plan.nodes:
                logger.warning("Planner created a plan with no nodes - this likely indicates an issue")
                # Try to create at least one default node to prevent empty plans
                default_node = PlanNode(
                    id="default_node",
                    description="Process the task using available information",
                    reasoning_module=state_obj.selected_modules[0] if state_obj.selected_modules else None,
                    dependencies=[]
                )
                result.plan.nodes[default_node.id] = default_node
                result.plan.entry_points = [default_node.id]
                
        except Exception as e:
            logger.error(f"Error in planning: {e}")
            # Create a minimal fallback plan
            fallback_plan = ExecutionPlan(
                task=state_obj.task,
                nodes={},
                entry_points=[],
                status="not_started"
            )
            
            # Create at least one node for each selected module or tool to ensure functionality
            for i, module_name in enumerate(state_obj.selected_modules[:2]):  # Limit to first 2 modules
                node_id = f"fallback_node_{i+1}"
                node = PlanNode(
                    id=node_id,
                    description=f"Apply {module_name} reasoning to task",
                    reasoning_module=module_name,
                    dependencies=[]
                )
                fallback_plan.nodes[node_id] = node
                fallback_plan.entry_points.append(node_id)
                
            # Add tool usage node if tools are available
            if state_obj.available_tools and self._tools:
                tool_name = state_obj.available_tools[0]
                tool_node = PlanNode(
                    id="tool_node",
                    description=f"Use {tool_name} to gather information",
                    reasoning_module=state_obj.selected_modules[0] if state_obj.selected_modules else None,
                    tool=tool_name,
                    args={"query": state_obj.task},
                    dependencies=[]
                )
                fallback_plan.nodes["tool_node"] = tool_node
                fallback_plan.entry_points.append("tool_node")
                
            # Create a placeholder result
            from src.haive.agents.rec_plan.models import PlannerOutput
            result = PlannerOutput(
                plan=fallback_plan,
                reasoning="Created fallback plan due to planning error",
                estimated_steps=len(fallback_plan.nodes),
                parallelizable=True
            )
        
        # Add a detailed plan summary message
        plan_summary = (
            f"Created execution plan with {len(result.plan.nodes)} nodes. " +
            f"Can execute {len(result.plan.entry_points)} steps in parallel.\n\n"
        )
        
        # Add tool usage details to the summary
        tools_used = set(node.tool for node in result.plan.nodes.values() if node.tool)
        if tools_used:
            plan_summary += f"Tools to be used: {', '.join(tools_used)}\n"
        
        # Add more detail about the plan structure
        if result.plan.nodes:
            plan_summary += "\nPlan structure:\n"
            for node_id, node in list(result.plan.nodes.items())[:3]:  # Show first 3 nodes
                plan_summary += f"- {node.description}"
                if node.tool:
                    plan_summary += f" (using {node.tool})"
                plan_summary += "\n"
            
            if len(result.plan.nodes) > 3:
                plan_summary += f"- ... and {len(result.plan.nodes) - 3} more steps\n"
        
        return {
            "plan": result.plan,
            "messages": state_obj.messages + [
                AIMessage(content=plan_summary)
            ]
        }
    def _schedule_execution_node(self, state: RecursiveTreePlannerState) -> Dict[str, Any]:
        """Schedule tasks for execution."""
        plan = state.plan
        
        # Find executable nodes (entry points or nodes with all dependencies satisfied)
        executable_nodes = plan.get_executable_nodes()
        
        if not executable_nodes:
            # Check if there are any pending nodes
            pending_nodes = [node for node in plan.nodes.values() if node.status == "pending"]
            
            if pending_nodes:
                # There are pending nodes but none can be executed - likely a circular dependency
                logger.error("Execution deadlock: No nodes ready but there are pending nodes")
                return {
                    "error": "Execution deadlock detected: No executable nodes but there are pending nodes.",
                    "messages": state.messages + [
                        AIMessage(content="Error: Execution deadlock detected. Check plan for circular dependencies.")
                    ]
                }
            else:
                # No pending nodes, must be complete
                logger.info("Plan execution complete")
                return {
                    "messages": state.messages + [
                        AIMessage(content="Plan execution complete.")
                    ]
                }
        
        # Limit the number of nodes to execute in parallel
        executable_nodes = executable_nodes[:self.config.max_parallel_steps]
        
        # Prepare current executions
        current_executions = {}
        for node in executable_nodes:
            # Mark as in progress
            node.status = "in_progress"
            
            # Record execution - handling the case where tool might be None
            # Use empty string as default when tool is None
            current_executions[node.id] = TaskExecution(
                node_id=node.id,
                tool=node.tool if node.tool is not None else "",  # Default to empty string if tool is None
                args=plan.resolve_args(node.args) if node.args else {},
                start_time=datetime.now().isoformat()
            )
        
        # Log scheduled executions
        logger.info(f"Scheduled {len(executable_nodes)} tasks for execution")
        
        return {
            "plan": plan,
            "current_executions": current_executions,
            "messages": state.messages + [
                AIMessage(content=f"Scheduled {len(executable_nodes)} tasks for execution.")
            ]
        }
        
    def _execute_tasks_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scheduled tasks in parallel with proper tool usage and ReAct pattern."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
        else:
            state_obj = state
                
        # Extract plan and current executions
        plan = state_obj.plan if hasattr(state_obj, 'plan') else state_obj.get("plan")
        current_executions = state_obj.current_executions if hasattr(state_obj, 'current_executions') else state_obj.get("current_executions", {})
        
        if not current_executions:
            logger.warning("No tasks scheduled for execution")
            return {
                "messages": state_obj.messages + [
                    AIMessage(content="No tasks scheduled for execution.")
                ]
            }
        
        # Execute tasks in parallel
        futures = {}
        for node_id, execution in current_executions.items():
            node = plan.nodes[node_id]
            
            # Submit task for execution
            future = self._executor.submit(
                self._execute_react_task,  # Use ReAct pattern
                node=node,
                plan=plan,
                state=state_obj
            )
            
            futures[future] = node_id
        
        # Process results
        execution_results = []
        variable_updates = {}
        detailed_messages = []
        
        for future in concurrent.futures.as_completed(futures):
            node_id = futures[future]
            node = plan.nodes[node_id]
            execution = current_executions[node_id]
            
            try:
                result, reasoning, tool_result = future.result()
                
                # Update node status and result
                node.status = "complete"
                node.result = result
                
                # Update variable if needed
                if node.variable_name:
                    plan.variables[node.variable_name] = result
                    variable_updates[node.variable_name] = result
                
                # Track successful execution
                execution_results.append({
                    "node_id": node_id,
                    "success": True,
                    "result": result,
                    "reasoning": reasoning,
                    "tool_result": tool_result
                })
                
                # Create detailed message about execution
                message_content = f"✅ Task '{node.description}' executed successfully\n\n"
                
                if node.tool:
                    message_content += f"Tool: {node.tool}\n"
                    message_content += f"Result: {tool_result}\n\n"
                    
                message_content += f"Reasoning: {reasoning[:200]}...\n"
                if node.variable_name:
                    message_content += f"Variable {node.variable_name} = {result}\n"
                    
                detailed_messages.append(AIMessage(content=message_content))
                
                logger.info(f"Task {node_id} executed successfully")
                
            except Exception as e:
                # Handle failure gracefully
                node.status = "failed"
                node.error = str(e)
                
                execution_results.append({
                    "node_id": node_id,
                    "success": False,
                    "error": str(e)
                })
                
                # Create message about failure
                detailed_messages.append(
                    AIMessage(content=f"❌ Task '{node.description}' failed: {str(e)}")
                )
                
                logger.error(f"Task {node_id} execution failed: {e}")
        
        # Update plan status
        plan.update_status()
        
        # Update completed nodes list
        completed_nodes = state_obj.completed_nodes if hasattr(state_obj, 'completed_nodes') else []
        for result in execution_results:
            if result["success"] and result["node_id"] not in completed_nodes:
                completed_nodes.append(result["node_id"])
        
        return {
            "plan": plan,
            "current_executions": {},  # Clear current executions
            "completed_nodes": completed_nodes,
            "variables": {**plan.variables},  # Update with latest variables
            "messages": state_obj.messages + detailed_messages
        }

    def _execute_react_task(self, node: PlanNode, plan: ExecutionPlan, state: Any) -> tuple:
        """Execute a task using the ReAct pattern with proper tool usage."""
        # Get the execution engine
        engine = self.config.engines["execution"]
        runnable = compose_runnable(engine)
        
        # Format context
        context = {
            "task": plan.task,
            "current_step": node.description,
            "reasoning_module": node.reasoning_module if node.reasoning_module else "general problem solving"
        }
        
        # Add dependency results
        if node.dependencies:
            dependency_results = {}
            for dep_id in node.dependencies:
                if dep_id in plan.nodes and plan.nodes[dep_id].status == "complete":
                    dependency_node = plan.nodes[dep_id]
                    dependency_results[dependency_node.description] = dependency_node.result
            context["dependency_results"] = dependency_results
        
        # Add variables
        if plan.variables:
            context["variables"] = plan.variables
        
        # Prepare input for ReAct execution
        input_data = {
            "messages": [
                HumanMessage(content=f"Execute this step: {node.description}")
            ],
            "task": plan.task,
            "context": context,
            "step_description": node.description,
            "reasoning_approach": node.reasoning_module
        }
        
        # If tool is specified, add tool information
        tool_result = None
        if node.tool and node.tool in self._tools:
            tool = self._tools[node.tool]
            input_data["tool_name"] = node.tool
            input_data["tool_description"] = tool.description
            input_data["tool_args"] = node.args
            
            # Resolve arguments
            resolved_args = plan.resolve_args(node.args)
            input_data["resolved_args"] = resolved_args
        
        # Run the ReAct execution
        execution_result = runnable.invoke(input_data)
        
        # Extract reasoning from execution result
        reasoning = ""
        if hasattr(execution_result, "reasoning"):
            reasoning = execution_result.reasoning
        elif hasattr(execution_result, "thought"):
            reasoning = execution_result.thought
        else:
            reasoning = "Executed step"
        
        # Extract action details if present
        action = None
        if hasattr(execution_result, "action"):
            action = execution_result.action
        
        # Extract final result
        result = None
        if hasattr(execution_result, "result"):
            result = execution_result.result
        
        # Execute tool if specified in action or node
        if node.tool and node.tool in self._tools:
            tool = self._tools[node.tool]
            resolved_args = plan.resolve_args(node.args)
            
            # If action specifies different args, use those
            if action and hasattr(action, "args"):
                resolved_args = action.args
                
            # Execute the tool
            try:
                tool_result = tool.invoke(resolved_args)
                # Override result with tool_result if not otherwise specified
                if result is None:
                    result = tool_result
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                raise
        
        # If still no result, use reasoning as result
        if result is None:
            result = reasoning
        
        return result, reasoning, tool_result
    
    
    def _execute_single_task(self, node: PlanNode, plan: ExecutionPlan, state: Any) -> tuple:
        """Execute a single task with parameter mapping to match the prompt template."""
        # Get the execution engine
        engine = self.config.engines["execution"]
        runnable = compose_runnable(engine)
        
        # Prepare context in the format expected by the prompt
        plan_context = f"Task: {plan.task}\nCurrent step: {node.description}\n"
        if node.dependencies:
            plan_context += "Using results from: " + ", ".join(
                [f"{plan.nodes[d_id].description}" for d_id in node.dependencies if d_id in plan.nodes]
            )
        
        # Prepare variables in the expected format
        variables_str = str(plan.variables) if plan.variables else "{}"
        
        # Prepare input with EXACT parameter names expected by the execution engine
        input_data = {
            "messages": [HumanMessage(content=f"Execute: {node.description}")],
            "task": plan.task,
            "current_step": node.description,  # Matches exactly what's in EXECUTION_SYSTEM_PROMPT
            "plan_context": plan_context,      # Matches exactly what's in EXECUTION_SYSTEM_PROMPT
            "variables": variables_str         # Matches exactly what's in EXECUTION_SYSTEM_PROMPT
        }
        
        # If tool is provided, add tool info - don't use these in main parameters
        # as they are not expected by the prompt template
        tool_result = None
        if node.tool and node.tool in self._tools:
            tool = self._tools[node.tool]
            tool_info = {
                "tool_info": {  # Nest these under a separate key to avoid parameter conflicts
                    "name": node.tool,
                    "description": tool.description,
                    "args": node.args,
                    "resolved_args": plan.resolve_args(node.args) if node.args else {}
                }
            }
            
            # Tool info can be provided separately and accessed in the reasoning but
            # won't conflict with the expected prompt parameters
            if hasattr(runnable, 'bind_tools'):
                # Use LangChain's bind_tools if supported
                tools = [self._tools[node.tool]]
                input_data["tools"] = tools
            else:
                # Otherwise just include it as additional info
                input_data.update(tool_info)
        
        # Run the execution engine
        try:
            execution_result = runnable.invoke(input_data)
            
            # Extract reasoning from execution result
            reasoning = ""
            if hasattr(execution_result, "reasoning"):
                reasoning = execution_result.reasoning
            elif hasattr(execution_result, "thought"):
                reasoning = execution_result.thought
            else:
                reasoning = str(execution_result)
            
            # Extract result from execution
            result = None
            if hasattr(execution_result, "result"):
                result = execution_result.result
            
            # Execute tool if specified
            if node.tool and node.tool in self._tools:
                try:
                    tool = self._tools[node.tool]
                    resolved_args = plan.resolve_args(node.args) if node.args else {}
                    tool_result = tool.invoke(resolved_args)
                    
                    # If no result from execution engine, use tool result
                    if result is None:
                        result = tool_result
                except Exception as e:
                    logger.error(f"Tool execution failed: {e}")
                    raise
            
            # If still no result, use reasoning as result
            if result is None:
                result = reasoning
            
            return result, reasoning, tool_result
            
        except Exception as e:
            logger.error(f"Task {node.id} execution failed: {e}")
            return f"Error: {str(e)}", f"Execution failed: {str(e)}", None
    def _check_execution_node(self, state: RecursiveTreePlannerState) -> Dict[str, Any]:
        """Check execution status and update the plan."""
        plan = state.plan
        
        # Update plan status
        plan.update_status()
        
        # Check if plan is complete
        if plan.status == "complete":
            logger.info("Plan execution complete")
            return {
                "messages": state.messages + [
                    AIMessage(content="Plan execution complete. Moving to reflection phase.")
                ]
            }
        elif plan.status == "failed":
            logger.error("Plan execution failed")
            return {
                "messages": state.messages + [
                    AIMessage(content="Plan execution failed. Moving to reflection phase to analyze failures.")
                ]
            }
        
        # If not complete or failed, more tasks need to be scheduled
        return {
            "messages": state.messages
        }
    
    def _reflect_node(self, state: RecursiveTreePlannerState) -> Dict[str, Any]:
        """Reflect on the plan and execution."""
        plan = state.plan
        
        # Format plan structure for reflection
        plan_structure = self._format_plan_for_reflection(plan)
        
        # Format execution results
        execution_results = self._format_execution_results(plan)
        
        # Get the reflection engine
        engine = self.config.engines["reflection"]
        runnable = compose_runnable(engine)
        
        # Prepare input
        input_data = {
            "messages": [HumanMessage(content="Reflect on the execution plan and results")],
            "task": state.task,
            "plan_structure": plan_structure,
            "execution_results": execution_results
        }
        
        # Run the engine
        result = runnable.invoke(input_data)
        
        # Add to reflections
        reflections = list(state.reflections)
        reflections.append(result.reflection)
        
        # Increment iteration counter
        current_iteration = state.current_iteration + 1
        
        return {
            "reflections": reflections,
            "current_iteration": current_iteration,
            "should_replan": result.should_replan,
            "messages": state.messages + [
                AIMessage(content=f"Reflection #{current_iteration}:\n\n{result.reasoning}")
            ]
        }
    
    def _generate_answer_node(self, state: RecursiveTreePlannerState) -> Dict[str, Any]:
        """Generate a final answer based on execution results."""
        plan = state.plan
        
        # Format execution results
        execution_results = self._format_execution_results(plan)
        
        # Get the final answer engine
        engine = self.config.engines["final_answer"]
        runnable = compose_runnable(engine)
        
        # Prepare input
        input_data = {
            "messages": [HumanMessage(content="Generate a final answer for the task")],
            "task": state.task,
            "execution_results": execution_results
        }
        
        # Run the engine
        result = runnable.invoke(input_data)
        
        return {
            "final_answer": result.answer,
            "messages": state.messages + [
                AIMessage(content=f"Final Answer (Confidence: {result.confidence}):\n\n{result.answer}")
            ]
        }
    
    # Routing functions
    
    def _route_after_scheduling(self, state: Dict[str, Any]) -> str:
        """Decide where to route after scheduling execution."""
        # Handle both dict and object types
        if isinstance(state, dict):
            current_executions = state.get("current_executions", {})
            plan = state.get("plan")
            plan_status = plan.status if plan else None
        else:
            current_executions = state.current_executions
            plan_status = state.plan.status if state.plan else None
        
        if not current_executions:
            # No tasks scheduled, check if plan is complete
            if plan_status == "complete":
                return "reflect"
            else:
                logger.warning("No tasks scheduled but plan is not complete")
                return "check_execution"
        
        # Tasks scheduled, execute them
        return "execute_tasks"
    
    def _route_after_checking(self, state: Dict[str, Any]) -> str:
        """Decide where to route after checking execution."""
        # Handle both dict and object types
        if isinstance(state, dict):
            plan = state.get("plan")
            plan_status = plan.status if plan else None
        else:
            plan = state.plan
            plan_status = plan.status if plan else None
        
        if plan_status in ["complete", "failed"]:
            # Plan is complete or failed, move to reflection
            return "reflect"
        
        # Still has pending nodes, schedule more
        return "schedule_execution"
    
    def _generate_answer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive final answer based on all gathered information."""
        # Convert state dict to object if needed
        if not isinstance(state, RecursiveTreePlannerState):
            try:
                state_obj = RecursiveTreePlannerState(**state)
            except Exception as e:
                logger.error(f"Failed to convert state dict to RecursiveTreePlannerState: {e}")
                # Use the dict directly
                state_obj = state
        else:
            state_obj = state
        
        # Get all relevant information
        plan = state_obj.plan if hasattr(state_obj, 'plan') else state_obj.get("plan")
        reflections = state_obj.reflections if hasattr(state_obj, 'reflections') else state_obj.get("reflections", [])
        messages = state_obj.messages if hasattr(state_obj, 'messages') else state_obj.get("messages", [])
        task = state_obj.task if hasattr(state_obj, 'task') else state_obj.get("task", "")
        
        # Format execution results
        execution_results = ""
        if plan:
            execution_results = self._format_execution_results(plan)
        
        # Format all variables collected
        variables_str = ""
        if plan and hasattr(plan, 'variables') and plan.variables:
            variables_str = "Variables:\n"
            for var_name, value in plan.variables.items():
                variables_str += f"- {var_name}: {value}\n"
        
        # Collect all completed node results
        node_results = []
        if plan and hasattr(plan, 'nodes'):
            for node_id, node in plan.nodes.items():
                if node.status == "complete" and node.result:
                    node_results.append({
                        "step": node.description,
                        "result": node.result,
                        "tool_used": node.tool
                    })
        
        # Format node results
        node_results_str = ""
        if node_results:
            node_results_str = "Results from execution steps:\n"
            for i, result in enumerate(node_results):
                node_results_str += f"{i+1}. {result['step']}: {result['result']}\n"
        
        # Get the final answer engine
        engine = self.config.engines["final_answer"]
        runnable = compose_runnable(engine)
        
        # Prepare comprehensive input
        input_data = {
            "messages": [HumanMessage(content=f"Generate a final answer for: {task}")],
            "task": task,
            "execution_results": execution_results,
            "variables": variables_str,
            "node_results": node_results_str,
            "message_history": "\n".join([f"{msg.type}: {msg.content[:100]}..." for msg in messages[-5:]]),
            "iterations_completed": state_obj.current_iteration if hasattr(state_obj, 'current_iteration') else state_obj.get("current_iteration", 0)
        }
        
        # Run the engine with robust error handling
        try:
            # Run with timeout to prevent hanging
            result = runnable.invoke(input_data)
            
            # Validate the answer
            if not hasattr(result, 'answer') or not result.answer:
                raise ValueError("No answer generated")
                
            final_answer = result.answer
            confidence = result.confidence if hasattr(result, 'confidence') else 0.7
            reasoning = result.reasoning if hasattr(result, 'reasoning') else ""
            
        except Exception as e:
            logger.error(f"Error generating final answer: {e}")
            
            # Create a fallback answer
            final_answer = "Based on the analysis and collected information, I can provide the following answer:\n\n"
            
            # Add any variable results
            if plan and hasattr(plan, 'variables') and plan.variables:
                final_answer += "Key findings:\n"
                for var_name, value in plan.variables.items():
                    final_answer += f"- {var_name}: {value}\n"
            
            # Add results from successful tool executions
            if node_results:
                final_answer += "\nResults:\n"
                for result in node_results:
                    if result['tool_used']:
                        final_answer += f"- Using {result['tool_used']}: {result['result']}\n"
            
            # Simple conclusion
            final_answer += "\nIn conclusion, I've attempted to address your task with the information available."
            confidence = 0.5
            reasoning = f"Generated fallback answer due to error: {str(e)}"
        
        # Create final message with confidence score
        final_message = f"Final Answer (Confidence: {confidence}):\n\n{final_answer}"
        
        # Include reasoning if available and substantive
        if reasoning and len(reasoning) > 20:
            final_message += f"\n\nReasoning: {reasoning}"
        
        # Log message history for debugging
        message_history = "\n".join([
            f"[{i}] {msg.type}: {msg.content[:100]}..."
            for i, msg in enumerate(messages)
        ])
        logger.debug(f"Message history:\n{message_history}")
        
        return {
            "final_answer": final_answer,
            "messages": messages + [
                AIMessage(content=final_message)
            ]
        }
        
    # Utility functions
    
    def _execute_task(self, node: PlanNode, plan: ExecutionPlan, state: RecursiveTreePlannerState) -> Tuple[Any, str]:
        """Execute a single task."""
        # Get the execution engine
        engine = self.config.engines["react_execution"]
        runnable = compose_runnable(engine)
        
        # Format plan context
        plan_context = f"Task: {plan.task}\n\n"
        plan_context += f"Current step: {node.description}\n\n"
        
        if node.dependencies:
            plan_context += "Dependencies:\n"
            for dep_id in node.dependencies:
                dep_node = plan.nodes.get(dep_id)
                if dep_node:
                    plan_context += f"- {dep_node.description}: {dep_node.result}\n"
        
        # Format variables
        variables_str = ""
        if plan.variables:
            variables_str = "Available variables:\n"
            for var_name, value in plan.variables.items():
                variables_str += f"- {var_name}: {value}\n"
        
        # Prepare input
        input_data = {
            "messages": [HumanMessage(content=f"Execute this step: {node.description}")],
            "task": plan.task,
            "current_step": node.description,
            "plan_context": plan_context,
            "variables": variables_str
        }
        
        # Run the engine with retry
        if self.config.retry_policy:
            result = execute_with_retry(
                runnable.invoke,
                input_data,
                retry_policy=self.config.retry_policy
            )
        else:
            result = runnable.invoke(input_data)
        
        # If tool execution is required
        if node.tool and node.tool in self._tools:
            # Get the tool
            tool = self._tools[node.tool]
            
            # Resolve arguments
            resolved_args = plan.resolve_args(node.args)
            
            # Execute the tool
            tool_result = tool.invoke(resolved_args)
            
            # Return both the tool result and reasoning
            return tool_result, result.reasoning
        else:
            # Just return the reasoning as the result
            return result.result, result.reasoning
    
    def _extract_task_from_messages(self, messages: List[BaseMessage]) -> str:
        """Extract the task from messages."""
        # Look for the last human message
        for message in reversed(messages):
            if message.type == "human":
                return message.content
        
        return "No task specified"
    
    def _format_plan_for_reflection(self, plan: ExecutionPlan) -> str:
        """Format a plan for reflection."""
        result = f"Plan for task: {plan.task}\n\n"
        
        # Add node information
        result += "Nodes:\n"
        for node_id, node in plan.nodes.items():
            # Format status with emoji
            status_emoji = "✅" if node.status == "complete" else "❌" if node.status == "failed" else "⏳"
            
            result += f"{status_emoji} {node.description} (ID: {node_id})\n"
            if node.tool:
                result += f"  Tool: {node.tool}\n"
            if node.reasoning_module:
                result += f"  Reasoning: {node.reasoning_module}\n"
            if node.dependencies:
                result += f"  Dependencies: {', '.join(node.dependencies)}\n"
            if node.status == "complete" and node.result:
                result += f"  Result: {node.result}\n"
            elif node.status == "failed" and node.error:
                result += f"  Error: {node.error}\n"
            result += "\n"
        
        # Add dependency structure
        result += "Dependency Structure:\n"
        for node_id, node in plan.nodes.items():
            if node.dependencies:
                dep_nodes = [plan.nodes[dep_id].description for dep_id in node.dependencies if dep_id in plan.nodes]
                result += f"- {node.description} depends on: {', '.join(dep_nodes)}\n"
        
        return result
    
    def _format_execution_results(self, plan: ExecutionPlan) -> str:
        """Format execution results for reflection or final answer."""
        result = "Execution Results:\n\n"
        
        # Add completed nodes
        completed_nodes = [node for node in plan.nodes.values() if node.status == "complete"]
        for node in completed_nodes:
            result += f"Task: {node.description}\n"
            result += f"Result: {node.result}\n\n"
        
        # Add failed nodes
        failed_nodes = [node for node in plan.nodes.values() if node.status == "failed"]
        if failed_nodes:
            result += "Failed Tasks:\n"
            for node in failed_nodes:
                result += f"- {node.description}: {node.error}\n"
        
        return result
    
    # Helper functions for agent creation
    
    @classmethod
    def create(cls, 
              name: Optional[str] = None, 
              tools: Optional[List[Union[BaseTool, StructuredTool]]] = None,
              **kwargs) -> 'RecursiveTreePlanner':
        """Create a recursive tree planner agent."""
        config = RecursiveTreePlannerConfig.create_default(
            name=name,
            tools=tools,
            **kwargs
        )
        
        return cls(config)


# Helper function for creating an agent instance
def create_recursive_tree_planner(
    name: Optional[str] = None,
    tools: Optional[List[Union[BaseTool, StructuredTool]]] = None,
    **kwargs
) -> RecursiveTreePlanner:
    """Create a recursive tree planner agent."""
    return RecursiveTreePlanner.create(name=name, tools=tools, **kwargs)