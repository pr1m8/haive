"""Complex Multi-Agent Workflows - Advanced Patterns

This example demonstrates the most advanced multi-agent patterns:
- Recursive agent hierarchies
- Dynamic graph modification
- Conditional loops and retries
- State-dependent agent spawning
- Complex error handling and recovery
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.agents.multi.base import MultiAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool
from haive.core.schema import StateSchema


# === 1. RECURSIVE PROBLEM SOLVER ===

class ProblemDecomposition(BaseModel):
    """Problem breakdown structure."""
    is_atomic: bool = Field(..., description="Can this be solved directly?")
    sub_problems: List[str] = Field(default_factory=list)
    solution_approach: Optional[str] = None
    estimated_complexity: float = Field(..., ge=0, le=1)


class Solution(BaseModel):
    """Solution to a problem."""
    problem_statement: str
    solution: str
    confidence: float
    sub_solutions: List['Solution'] = Field(default_factory=list)


# Allow recursive model
Solution.model_rebuild()


class RecursiveProblemSolver(MultiAgent):
    """Recursively decomposes and solves complex problems."""
    
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.current_depth = 0
        
        # Problem analyzer
        analyzer = SimpleAgent(
            name="problem_analyzer",
            engine=AugLLMConfig(temperature=0.3),
            structured_output_model=ProblemDecomposition,
            system_message="Analyze if a problem can be solved directly or needs decomposition."
        )
        
        # Direct solver for atomic problems
        solver = SimpleAgent(
            name="atomic_solver",
            engine=AugLLMConfig(temperature=0.5),
            structured_output_model=Solution,
            system_message="Solve atomic problems directly."
        )
        
        # Solution synthesizer
        synthesizer = SimpleAgent(
            name="solution_synthesizer",
            engine=AugLLMConfig(temperature=0.4),
            structured_output_model=Solution,
            system_message="Combine sub-solutions into a complete solution."
        )
        
        agents = {
            "analyzer": analyzer,
            "solver": solver,
            "synthesizer": synthesizer
        }
        
        super().__init__(
            name="recursive_solver",
            agents=agents,
            entry_point="analyzer"
        )
        
        self._setup_recursive_routing()
    
    def _setup_recursive_routing(self):
        """Setup routing for recursive problem solving."""
        
        def route_after_analysis(state: Dict[str, Any]) -> str:
            """Route based on problem analysis."""
            decomposition = state.get("problem_decomposition", {})
            
            if decomposition.get("is_atomic", False):
                return "solver"
            elif self.current_depth < self.max_depth:
                # Recursively spawn new instances for sub-problems
                return "spawn_recursive"
            else:
                # Max depth reached, force direct solution
                return "solver"
        
        self.add_conditional_edges(
            source="analyzer",
            path=route_after_analysis
        )
        
        # Add recursive spawning logic
        async def spawn_recursive_solvers(state: Dict[str, Any]) -> Dict[str, Any]:
            """Spawn new solver instances for sub-problems."""
            decomposition = state.get("problem_decomposition", {})
            sub_problems = decomposition.get("sub_problems", [])
            
            sub_solutions = []
            for sub_problem in sub_problems:
                # Create new instance with incremented depth
                sub_solver = RecursiveProblemSolver(max_depth=self.max_depth)
                sub_solver.current_depth = self.current_depth + 1
                
                # Solve sub-problem
                sub_result = await sub_solver.arun(sub_problem)
                sub_solutions.append(sub_result)
            
            state["sub_solutions"] = sub_solutions
            return state
        
        # Add custom node for spawning
        self.add_node("spawn_recursive", spawn_recursive_solvers)
        self.add_edge("spawn_recursive", "synthesizer")


# === 2. SELF-IMPROVING WORKFLOW ===

class PerformanceMetrics(BaseModel):
    """Workflow performance metrics."""
    success_rate: float
    average_time: float
    error_count: int
    bottlenecks: List[str]
    improvement_suggestions: List[str]


class WorkflowOptimization(BaseModel):
    """Optimization recommendations."""
    add_agents: List[Dict[str, str]]
    remove_agents: List[str]
    modify_routes: List[Dict[str, Any]]
    parameter_adjustments: Dict[str, Any]


class SelfImprovingWorkflow(MultiAgent):
    """Workflow that monitors and improves itself."""
    
    def __init__(self):
        # Performance monitor
        monitor = SimpleAgent(
            name="performance_monitor",
            engine=AugLLMConfig(temperature=0.2),
            structured_output_model=PerformanceMetrics,
            system_message="Monitor workflow performance and identify issues."
        )
        
        # Optimization planner
        optimizer = SimpleAgent(
            name="workflow_optimizer",
            engine=AugLLMConfig(temperature=0.6),
            structured_output_model=WorkflowOptimization,
            system_message="Suggest workflow optimizations based on performance data."
        )
        
        # Core workers (start simple)
        worker1 = SimpleAgent(name="worker_1", engine=AugLLMConfig())
        worker2 = SimpleAgent(name="worker_2", engine=AugLLMConfig())
        
        agents = {
            "monitor": monitor,
            "optimizer": optimizer,
            "worker_1": worker1,
            "worker_2": worker2
        }
        
        super().__init__(
            name="self_improving_workflow",
            agents=agents
        )
        
        self.execution_history = []
        self._setup_monitoring()
    
    def _setup_monitoring(self):
        """Setup performance monitoring and optimization."""
        
        async def monitor_and_optimize(state: Dict[str, Any]) -> Dict[str, Any]:
            """Monitor performance and apply optimizations."""
            # Track execution
            self.execution_history.append({
                "timestamp": asyncio.get_event_loop().time(),
                "state": state.copy()
            })
            
            # Every 10 executions, run optimization
            if len(self.execution_history) % 10 == 0:
                # Analyze performance
                perf_state = {"history": self.execution_history}
                metrics = await self.agents["monitor"].arun(perf_state)
                
                # Get optimization suggestions
                opt_state = {"metrics": metrics}
                optimizations = await self.agents["optimizer"].arun(opt_state)
                
                # Apply optimizations dynamically
                await self._apply_optimizations(optimizations)
            
            return state
        
        # Add monitoring node
        self.add_node("monitor_performance", monitor_and_optimize)
    
    async def _apply_optimizations(self, optimizations: WorkflowOptimization):
        """Dynamically modify workflow based on optimizations."""
        # Add new agents
        for agent_spec in optimizations.add_agents:
            new_agent = SimpleAgent(
                name=agent_spec["name"],
                engine=AugLLMConfig(**agent_spec.get("config", {}))
            )
            self.agents[agent_spec["name"]] = new_agent
            self.mark_for_recompile(f"Added agent: {agent_spec['name']}")
        
        # Remove underperforming agents
        for agent_name in optimizations.remove_agents:
            if agent_name in self.agents:
                del self.agents[agent_name]
                self.mark_for_recompile(f"Removed agent: {agent_name}")
        
        # Modify routes
        for route_mod in optimizations.modify_routes:
            self.add_edge(route_mod["from"], route_mod["to"])


# === 3. COMPETITIVE AGENT RACING ===

class RaceResult(BaseModel):
    """Result of agent race."""
    winner: str
    completion_times: Dict[str, float]
    quality_scores: Dict[str, float]
    outputs: Dict[str, Any]


class CompetitiveAgentRace(MultiAgent):
    """Multiple agents compete to solve the same problem."""
    
    def __init__(self, competitors: List[SimpleAgent]):
        self.competitors = competitors
        
        # Judge to evaluate results
        judge = SimpleAgent(
            name="competition_judge",
            engine=AugLLMConfig(temperature=0.1),
            structured_output_model=RaceResult,
            system_message="Evaluate competing solutions for quality and speed."
        )
        
        agents = {"judge": judge}
        for competitor in competitors:
            agents[competitor.name] = competitor
        
        super().__init__(
            name="agent_race",
            agents=agents
        )
        
        self._setup_race()
    
    def _setup_race(self):
        """Setup competitive execution."""
        
        async def run_competition(state: Dict[str, Any]) -> Dict[str, Any]:
            """Run all competitors in parallel."""
            input_data = state.get("input", "")
            
            # Create tasks for all competitors
            tasks = []
            for competitor in self.competitors:
                task = asyncio.create_task(
                    self._timed_execution(competitor, input_data)
                )
                tasks.append((competitor.name, task))
            
            # Wait for first to complete (race condition)
            results = {}
            completion_order = []
            
            for name, task in tasks:
                try:
                    result = await task
                    results[name] = result
                    completion_order.append(name)
                except Exception as e:
                    results[name] = {"error": str(e), "time": float('inf')}
            
            state["race_results"] = results
            state["completion_order"] = completion_order
            return state
        
        self.add_node("race", run_competition)
        self.add_edge("race", "judge")
    
    async def _timed_execution(self, agent: SimpleAgent, input_data: Any) -> Dict[str, Any]:
        """Execute agent with timing."""
        start_time = asyncio.get_event_loop().time()
        try:
            output = await agent.arun(input_data)
            end_time = asyncio.get_event_loop().time()
            return {
                "output": output,
                "time": end_time - start_time,
                "success": True
            }
        except Exception as e:
            end_time = asyncio.get_event_loop().time()
            return {
                "error": str(e),
                "time": end_time - start_time,
                "success": False
            }


# === 4. AGENT SWARM WITH EMERGENT BEHAVIOR ===

class SwarmState(StateSchema):
    """Shared state for agent swarm."""
    pheromone_trails: Dict[str, float] = Field(default_factory=dict)
    discovered_solutions: List[Dict[str, Any]] = Field(default_factory=list)
    swarm_consensus: Optional[str] = None
    exploration_map: Dict[str, int] = Field(default_factory=dict)


class SwarmAgent(SimpleAgent):
    """Individual agent in a swarm."""
    
    def __init__(self, agent_id: int, behavior_type: str):
        super().__init__(
            name=f"swarm_agent_{agent_id}",
            engine=AugLLMConfig(temperature=0.8),  # High creativity
            system_message=f"You are swarm agent {agent_id} with {behavior_type} behavior."
        )
        self.behavior_type = behavior_type
    
    async def explore(self, state: SwarmState, problem: str) -> Dict[str, Any]:
        """Explore solution space based on pheromone trails."""
        # Follow or avoid trails based on behavior
        if self.behavior_type == "explorer":
            # Avoid well-trodden paths
            avoid_areas = [k for k, v in state.pheromone_trails.items() if v > 0.7]
            prompt = f"Solve '{problem}' with a novel approach. Avoid: {avoid_areas}"
        elif self.behavior_type == "follower":
            # Follow strong trails
            follow_areas = [k for k, v in state.pheromone_trails.items() if v > 0.5]
            prompt = f"Solve '{problem}' building on: {follow_areas}"
        else:  # "hybrid"
            prompt = f"Solve '{problem}' balancing novelty and proven approaches"
        
        solution = await self.arun(prompt)
        
        # Update pheromone trails
        solution_key = str(hash(solution))[:8]
        state.pheromone_trails[solution_key] = state.pheromone_trails.get(solution_key, 0) + 0.1
        
        return {
            "agent": self.name,
            "behavior": self.behavior_type,
            "solution": solution,
            "trail_key": solution_key
        }


class SwarmIntelligence(MultiAgent):
    """Swarm of agents with emergent problem-solving behavior."""
    
    def __init__(self, swarm_size: int = 10):
        # Create diverse swarm
        swarm_agents = []
        behaviors = ["explorer", "follower", "hybrid"]
        
        for i in range(swarm_size):
            behavior = behaviors[i % len(behaviors)]
            agent = SwarmAgent(i, behavior)
            swarm_agents.append(agent)
        
        # Consensus builder
        consensus = SimpleAgent(
            name="swarm_consensus",
            engine=AugLLMConfig(temperature=0.3),
            system_message="Analyze swarm solutions and build consensus."
        )
        
        agents = {"consensus": consensus}
        for agent in swarm_agents:
            agents[agent.name] = agent
        
        super().__init__(
            name="swarm_intelligence",
            agents=agents
        )
        
        self.swarm_agents = swarm_agents
        self.swarm_state = SwarmState()
        self._setup_swarm_behavior()
    
    def _setup_swarm_behavior(self):
        """Setup swarm exploration and consensus."""
        
        async def swarm_explore(state: Dict[str, Any]) -> Dict[str, Any]:
            """All swarm agents explore in parallel."""
            problem = state.get("problem", "")
            
            # Parallel exploration
            tasks = []
            for agent in self.swarm_agents:
                task = agent.explore(self.swarm_state, problem)
                tasks.append(task)
            
            solutions = await asyncio.gather(*tasks)
            
            # Store discovered solutions
            self.swarm_state.discovered_solutions.extend(solutions)
            
            # Evaporate pheromone trails
            for key in self.swarm_state.pheromone_trails:
                self.swarm_state.pheromone_trails[key] *= 0.9
            
            state["swarm_solutions"] = solutions
            state["swarm_state"] = self.swarm_state.model_dump()
            
            return state
        
        self.add_node("swarm_explore", swarm_explore)
        self.add_edge("swarm_explore", "consensus")


# === 5. NEGOTIATION AND CONSENSUS PROTOCOL ===

class NegotiationPosition(BaseModel):
    """Negotiation position."""
    agent_name: str
    position: str
    priorities: List[str]
    concessions: List[str]
    red_lines: List[str]


class NegotiationRound(BaseModel):
    """Single negotiation round."""
    round_number: int
    positions: List[NegotiationPosition]
    agreements: List[str]
    disagreements: List[str]
    progress_score: float


async def negotiation_protocol():
    """Multi-agent negotiation with protocol."""
    
    # Create negotiators with different interests
    buyer = SimpleAgent(
        name="buyer_agent",
        engine=AugLLMConfig(temperature=0.5),
        structured_output_model=NegotiationPosition,
        system_message="You represent the buyer. Minimize cost, maximize value."
    )
    
    seller = SimpleAgent(
        name="seller_agent",
        engine=AugLLMConfig(temperature=0.5),
        structured_output_model=NegotiationPosition,
        system_message="You represent the seller. Maximize revenue, maintain margins."
    )
    
    mediator = SimpleAgent(
        name="mediator_agent",
        engine=AugLLMConfig(temperature=0.4),
        structured_output_model=NegotiationRound,
        system_message="You are a neutral mediator. Find common ground and facilitate agreement."
    )
    
    class NegotiationProtocol(MultiAgent):
        """Structured negotiation protocol."""
        
        def __init__(self):
            agents = {
                "buyer": buyer,
                "seller": seller,
                "mediator": mediator
            }
            
            super().__init__(
                name="negotiation_protocol",
                agents=agents
            )
            
            self.round_count = 0
            self.max_rounds = 5
            self._setup_protocol()
        
        def _setup_protocol(self):
            """Setup negotiation rounds."""
            
            async def negotiation_round(state: Dict[str, Any]) -> Dict[str, Any]:
                """Execute one negotiation round."""
                self.round_count += 1
                
                # Get positions from both parties
                context = state.get("negotiation_context", {})
                
                buyer_position = await self.agents["buyer"].arun(context)
                seller_position = await self.agents["seller"].arun(context)
                
                # Mediate
                mediation_input = {
                    "round_number": self.round_count,
                    "buyer_position": buyer_position,
                    "seller_position": seller_position,
                    "previous_rounds": state.get("rounds", [])
                }
                
                round_result = await self.agents["mediator"].arun(mediation_input)
                
                # Update state
                state["rounds"] = state.get("rounds", []) + [round_result]
                state["current_round"] = round_result
                
                return state
            
            def should_continue(state: Dict[str, Any]) -> str:
                """Check if negotiation should continue."""
                current_round = state.get("current_round", {})
                progress = current_round.get("progress_score", 0)
                
                if progress > 0.8 or len(current_round.get("agreements", [])) > 5:
                    return "finalize"
                elif self.round_count >= self.max_rounds:
                    return "deadlock"
                else:
                    return "continue"
            
            self.add_node("negotiate", negotiation_round)
            self.add_conditional_edges(
                source="negotiate",
                path=should_continue,
                path_map={
                    "continue": "negotiate",  # Loop back
                    "finalize": "finalize_deal",
                    "deadlock": "handle_deadlock"
                }
            )
    
    protocol = NegotiationProtocol()
    result = await protocol.arun({
        "negotiation_context": {
            "item": "Enterprise software license",
            "initial_price": 100000,
            "quantity": 50
        }
    })
    
    return result


# === MAIN EXECUTION ===

async def main():
    """Demonstrate complex multi-agent workflows."""
    
    print("🚀 Complex Multi-Agent Workflows Demo\n")
    
    # 1. Recursive Problem Solver
    print("1️⃣ Recursive Problem Solving")
    print("-" * 50)
    recursive_solver = RecursiveProblemSolver(max_depth=3)
    result = await recursive_solver.arun(
        "Design a sustainable city that addresses climate change, "
        "economic growth, and social equity"
    )
    print(f"Recursive Solution: {result}\n")
    
    # 2. Self-Improving Workflow
    print("2️⃣ Self-Improving Workflow")
    print("-" * 50)
    self_improver = SelfImprovingWorkflow()
    # Run multiple times to trigger optimization
    for i in range(15):
        await self_improver.arun(f"Task iteration {i}")
    print("Workflow self-improvement completed\n")
    
    # 3. Competitive Racing
    print("3️⃣ Competitive Agent Racing")
    print("-" * 50)
    competitors = [
        SimpleAgent(name="speed_demon", engine=AugLLMConfig(temperature=0.9)),
        SimpleAgent(name="careful_thinker", engine=AugLLMConfig(temperature=0.1)),
        SimpleAgent(name="balanced_runner", engine=AugLLMConfig(temperature=0.5))
    ]
    race = CompetitiveAgentRace(competitors)
    race_result = await race.arun({
        "input": "Write a haiku about artificial intelligence"
    })
    print(f"Race Result: {race_result}\n")
    
    # 4. Swarm Intelligence
    print("4️⃣ Swarm Intelligence")
    print("-" * 50)
    swarm = SwarmIntelligence(swarm_size=8)
    swarm_result = await swarm.arun({
        "problem": "Find innovative uses for expired food waste"
    })
    print(f"Swarm Consensus: {swarm_result}\n")
    
    # 5. Negotiation Protocol
    print("5️⃣ Multi-Agent Negotiation")
    print("-" * 50)
    negotiation_result = await negotiation_protocol()
    print(f"Negotiation Result: {negotiation_result}\n")


if __name__ == "__main__":
    asyncio.run(main())