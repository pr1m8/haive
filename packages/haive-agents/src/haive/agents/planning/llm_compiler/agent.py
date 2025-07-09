"""LLM Compiler Agent Implementation

This implementation follows the LLM Compiler architecture from the paper by Kim et al.,
focusing on parallelizable task execution through a DAG structure.
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Any

from agents.llm_compiler.config import LLMCompilerAgentConfig
from agents.llm_compiler.models import (  # CompilerState,
    CompilerPlan,
    CompilerStep,
    FinalResponse,
    JoinerOutput,
)
from agents.llm_compiler.output_parser import LLMCompilerPlanParser
from agents.llm_compiler.state import CompilerState
from haive.core.engine.agent.agent import AgentArchitecture
from haive.core.engine.aug_llm import compose_runnable
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph


class LLMCompilerAgent(AgentArchitecture):
    """LLM Compiler Agent implementation.

    This agent architecture has three main components:
    1. Planner: Creates a task DAG
    2. Task Executor: Executes tasks as their dependencies are satisfied
    3. Joiner: Processes results and decides whether to output an answer or replan
    """

    def __init__(self, config: LLMCompilerAgentConfig):
        """Initialize the LLM Compiler agent."""
        # Initialize with base agent architecture
        super().__init__(config)

        self.config = config
        self.tools = config.tool_instances
        self.tool_map = {tool.name: tool for tool in self.tools}

        # Create parser
        self.parser = LLMCompilerPlanParser(tools=self.tools)

        # Build the LLMs using compose_runnable
        self.planner_llm = compose_runnable(config.planner_config)
        self.replanner_llm = compose_runnable(config.replanner_config)
        self.joiner_llm = compose_runnable(config.joiner_config)

        # Initialize graph
        self.graph = None

    def plan(self, state: CompilerState) -> dict[str, Any]:
        """Generate a plan based on the user's query.

        Args:
            state: Current agent state

        Returns:
            Updated state with a new plan
        """
        # Determine if we're replanning or creating a new plan
        is_replanning = state.replan_count > 0

        # Select the appropriate LLM and prepare inputs
        if is_replanning:
            llm = self.replanner_llm

            # Format evidence from past execution for replanning
            past_results = self._format_results_for_replanning(state)

            # Calculate the next step index for continuing
            next_idx = state.get_highest_step_id() + 1

            # Prepare replanner inputs
            inputs = {
                "query": state.query,
                "feedback": past_results,
                "next_idx": next_idx,
                "next_idx_plus_one": next_idx + 1,
                "next_idx_plus_two": next_idx + 2,
            }
        else:
            llm = self.planner_llm
            inputs = {"query": state.query}

        # Format tool descriptions for the prompt
        if hasattr(llm, "partial"):
            tool_descriptions = self._format_tool_descriptions()
            llm = llm.partial(
                tool_descriptions=tool_descriptions,
                num_tools=len(self.tools) + 1,  # +1 for join
            )

        # Generate a plan
        try:
            # Get raw text output
            result = llm.invoke(inputs)

            # Parse the plan
            if isinstance(result, str):
                plan = self.parser.parse(result)
            else:
                plan = self.parser.parse(str(result))

            print(f"Generated plan with {len(plan.steps)} steps")

            # Update state
            return {"plan": plan}

        except Exception as e:
            import traceback

            print(f"Error generating plan: {e}")
            print(traceback.format_exc())

            # Create a fallback plan
            plan = self._create_fallback_plan(state.query)
            return {"plan": plan}

    def _format_tool_descriptions(self) -> str:
        """Format tool descriptions for the planner prompt.

        Returns:
            Formatted tool descriptions
        """
        descriptions = []
        for i, tool in enumerate(self.tools):
            desc = f"{i+1}. {tool.name}: {tool.description}"

            # Add parameter info if available
            if hasattr(tool, "args_schema") and tool.args_schema:
                schema_props = getattr(tool.args_schema, "schema", {}).get(
                    "properties", {}
                )
                if schema_props:
                    desc += "\nParameters:"
                    for param_name, param_info in schema_props.items():
                        param_type = param_info.get("type", "any")
                        param_desc = param_info.get("description", "")
                        desc += f"\n  - {param_name} ({param_type}): {param_desc}"

            descriptions.append(desc)

        return "\n\n".join(descriptions)

    def _format_results_for_replanning(self, state: CompilerState) -> str:
        """Format previous results for replanning.

        Args:
            state: Current agent state

        Returns:
            Formatted results as a string
        """
        if not state.plan or not state.results:
            return "No previous results available."

        # Format the plan and results
        lines = ["Previous Plan and Results:"]

        for step in state.plan.steps:
            step_id = step.id
            tool_name = step.task.tool_name
            args = step.task.arguments

            # Format the step definition
            args_str = ", ".join(f'{k}="{v}"' for k, v in args.items())
            lines.append(f"{step_id}. {tool_name}({args_str})")

            # Add the result if available
            if step_id in state.results:
                result = state.results[step_id]
                lines.append(f"Observation: {result}")
                lines.append("")

        return "\n".join(lines)

    def _create_fallback_plan(self, query: str) -> CompilerPlan:
        """Create a fallback plan when planning fails.

        Args:
            query: The user's query

        Returns:
            A simple fallback plan
        """
        # Create a basic plan with a search and join step
        plan = CompilerPlan(
            description=f"Fallback plan for: {query}", status="not_started"
        )

        # Find a search tool
        search_tool = next(
            (tool.name for tool in self.tools if "search" in tool.name.lower()), None
        )

        if search_tool:
            # Add search step
            plan.add_compiler_step(
                step_id=1,
                description=f"Search for information about: {query}",
                tool_name=search_tool,
                arguments={"query": query},
            )

            # Add join step
            plan.add_compiler_step(
                step_id=2,
                description="Combine results and generate final answer",
                tool_name="join",
                arguments={},
                dependencies=[1],
            )
        else:
            # Just add a join step
            plan.add_compiler_step(
                step_id=1,
                description="Generate final answer",
                tool_name="join",
                arguments={},
            )

        return plan

    def execute_tasks(self, state: CompilerState) -> dict[str, Any]:
        """Execute tasks in parallel as their dependencies are satisfied.

        Args:
            state: Current agent state

        Returns:
            Updated state with executed task results
        """
        # Get executable steps (those with satisfied dependencies)
        executable_steps = state.get_executable_steps()

        if not executable_steps:
            # No steps to execute, might be done or stuck
            return {}

        print(f"Executing {len(executable_steps)} steps in parallel")

        # Track new results from this execution round
        new_results = {}

        # Execute steps in parallel
        with ThreadPoolExecutor() as executor:
            futures = {}

            # Submit tasks
            for step in executable_steps:
                future = executor.submit(
                    self._execute_step, step, state.results, self.tool_map
                )
                futures[step.id] = future

            # Wait for all to complete
            for step_id, future in futures.items():
                try:
                    result = future.result(timeout=self.config.max_execution_time)
                    new_results[step_id] = result

                    # Mark the step as complete in the plan
                    step = state.plan.get_step_by_id(step_id)
                    if step:
                        step.add_result(str(result))

                except Exception as e:
                    error_msg = f"Error executing step {step_id}: {e!s}"
                    print(error_msg)
                    new_results[step_id] = error_msg

        # Update results in state
        results = {**state.results, **new_results}

        # Check if we're done
        is_done = (
            state.plan.get_join_step() and state.plan.get_join_step().id in new_results
        )

        return {"results": results, "is_done": is_done}

    @staticmethod
    def _execute_step(
        step: CompilerStep, results: dict[int, Any], tool_map: dict[str, BaseTool]
    ) -> Any:
        """Execute a single step.

        Args:
            step: The step to execute
            results: Results from previous steps
            tool_map: Dictionary mapping tool names to tools

        Returns:
            Result of the step execution
        """
        try:
            return step.execute(tool_map, results)
        except Exception as e:
            import traceback

            return f"ERROR: {e!s}\n{traceback.format_exc()}"

    def join(self, state: CompilerState) -> dict[str, Any]:
        """Process the results and decide whether to provide a final answer or replan.

        Args:
            state: Current agent state

        Returns:
            Decision to end or replan
        """
        # If no plan or no results, create a plan
        if not state.plan or not state.results:
            return {"replan": True, "replan_count": state.replan_count + 1}

        # Format the executed tasks and their results
        executed_tasks = []
        for step in state.plan.steps:
            if step.id in state.results:
                tool_name = step.task.tool_name
                args = step.task.arguments
                result = state.results[step.id]

                args_str = ", ".join(f'{k}="{v}"' for k, v in args.items())
                executed_tasks.append(f"{step.id}. {tool_name}({args_str}) -> {result}")

        # Prepare joiner inputs
        joiner_inputs = {
            "query": state.query,
            "executed_tasks": "\n".join(executed_tasks),
            "results": "\n".join(f"Step {k}: {v}" for k, v in state.results.items()),
        }

        # Invoke joiner
        try:
            # The joiner will return a structured output due to AugLLMConfig settings
            output: JoinerOutput = self.joiner_llm.invoke(joiner_inputs)

            # Process decision
            if isinstance(output.action, FinalResponse):
                # Final answer
                message = AIMessage(content=output.action.response)
                return {"messages": [message], "done": True}
            # Replan
            feedback = output.action.feedback
            print(f"Replanning with feedback: {feedback}")
            return {"replan": True, "replan_count": state.replan_count + 1}

        except Exception as e:
            import traceback

            print(f"Error in joiner: {e}")
            print(traceback.format_exc())

            # Default to providing a simple response
            response = self._generate_fallback_response(state)
            message = AIMessage(content=response)
            return {"messages": [message], "done": True}

    def _generate_fallback_response(self, state):
        """Generates a fallback response when execution fails.

        Args:
            state (CompilerState | Dict): The final state after execution.

        Returns:
            str: The fallback response.
        """
        if not isinstance(state, CompilerState):
            return "ERROR: Execution failed due to invalid state type."

        join_step = state.plan.get_join_step() if state.plan else None
        return f"Execution failed. Join step: {join_step}"

    def should_execute_more(self, state: CompilerState, config=None) -> str:
        """Determine the next execution step.

        Args:
            state (CompilerState): The current agent state.
            config (Optional[Any]): Execution configuration (not used but required).

        Returns:
            str: The next node to execute in the state graph.
        """
        if not state.plan:
            return "planner"  # No plan exists → Generate a new plan

        if state.all_steps_complete():
            return "join"  # Plan complete → Join results

        if state.get_executable_steps():
            return "execute_tasks"  # Continue execution

        # Detect execution errors
        for result in state.results.values():
            if isinstance(result, str) and result.startswith("ERROR"):
                return "join"  # Error detected → Replan

        return "execute_tasks"  # Default to continuing execution

    def setup_workflow(self):
        """Set up the agent workflow as a state graph."""
        # Create the state graph
        self.graph = StateGraph(CompilerState)

        # Add nodes
        self.graph.add_node("planner", self.plan)
        self.graph.add_node("execute_tasks", self.execute_tasks)
        self.graph.add_node("join", self.join)

        # Add edges
        self.graph.add_edge("planner", "execute_tasks")

        # Add conditional edges
        self.graph.add_conditional_edges(
            "execute_tasks",
            self.should_execute_more,
            {"planner": "planner", "execute_tasks": "execute_tasks", "join": "join"},
        )

        def should_replan(state: CompilerState, config=None) -> bool:
            """Determines whether the agent should replan based on execution results.

            Args:
                state (CompilerState): The current state of execution.
                config (Optional[Any]): Unused but required by LangGraph.

            Returns:
                bool: True if replanning is needed, False otherwise.
            """
            # Prevent empty messages from causing index errors
            if not state.messages:
                return False

            # Ensure previous results exist
            if not state.results:
                return False

            return isinstance(state.messages[-1], SystemMessage)

        self.graph.add_conditional_edges(
            "join",
            should_replan,
            {
                True: "planner",  # If replanning needed, go back to planning
                False: END,  # Otherwise, terminate execution
            },
        )

        # Add start edge
        self.graph.add_edge(START, "planner")

        # Compile the graph
        # self.graph = self.graph.compile()

        # Visualize if configured

    def run(self, query: str):
        """Run the agent on a query.

        Args:
            query: The user's query

        Returns:
            Response from the agent
        """
        # Ensure graph is set up
        if not self.graph:
            self.setup_workflow()

        # Initialize state
        initial_state = CompilerState(query=query)

        # Run the agent
        print(f"Running query: {query}")
        final_state = self.app.ainvoke(
            initial_state, config=self.config.runnable_config, debug=True
        )

        # Return the final result
        if final_state.get("messages"):
            for message in final_state["messages"]:
                if isinstance(message, AIMessage):
                    return message.content

        # Fallback
        return self._generate_fallback_response(final_state)

    async def arun(self, query: str):
        """Run the agent asynchronously.

        Args:
            query: The user's query

        Returns:
            Response from the agent
        """
        # Ensure graph is set up
        if not self.graph:
            self.setup_workflow()

        # Initialize state
        initial_state = CompilerState(query=query)

        # Run the agent
        print(f"Running query asynchronously: {query}")
        final_state = await self.app.ainvoke(
            initial_state, config=self.config.runnable_config, debug=True
        )

        # Return the final result
        if final_state.get("messages"):
            for message in final_state["messages"]:
                if isinstance(message, AIMessage):
                    return message.content

        # Fallback
        return self._generate_fallback_response(final_state)

    def stream(self, query: str):
        """Stream the agent's execution.

        Args:
            query: The user's query

        Yields:
            Execution steps
        """
        # Ensure graph is set up
        if not self.graph:
            self.setup_workflow()

        # Initialize state
        initial_state = CompilerState(query=query)

        # Stream execution
        yield from self.app.stream(
            initial_state, config=self.config.runnable_config, debug=True
        )


import asyncio


def main():
    agent = LLMCompilerAgent(config=LLMCompilerAgentConfig())
    asyncio.run(
        agent.arun(
            "Find the winner of the most recent wimbldedon championship, and write a python program printing their name and execute it."
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
