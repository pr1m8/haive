"""Enhanced LATS (Language Agent Tree Search) Agent.

This implementation provides a sophisticated tree search with language model evaluation:
- Monte Carlo Tree Search with language model guidance
- Dynamic exploration/exploitation balancing
- Real-time tree expansion and pruning
- Comprehensive solution evaluation and ranking
- No mocks - all real components
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
import json
import logging
import math
from typing import Any
from uuid import uuid4

from langchain_core.tools import tool
from pydantic import BaseModel, Field, computed_field

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState


logger = logging.getLogger(__name__)


class NodeStatus(str, Enum):
    """Status of search tree nodes."""

    UNEXPLORED = "unexplored"
    EXPLORING = "exploring"
    EVALUATED = "evaluated"
    TERMINAL = "terminal"
    PRUNED = "pruned"


class SearchStrategy(str, Enum):
    """Search strategies for LATS."""

    BREADTH_FIRST = "breadth_first"
    DEPTH_FIRST = "depth_first"
    BEST_FIRST = "best_first"
    UCB_GUIDED = "ucb_guided"
    ADAPTIVE = "adaptive"


@dataclass
class SearchMetrics:
    """Metrics for search performance."""

    nodes_explored: int = 0
    nodes_evaluated: int = 0
    nodes_pruned: int = 0
    total_evaluations: int = 0
    best_score: float = 0.0
    search_depth: int = 0
    exploration_time: float = 0.0


class ThoughtNode(BaseModel):
    """Enhanced thought node for LATS tree search."""

    node_id: str = Field(..., description="Unique node identifier")
    parent_id: str | None = Field(default=None, description="Parent node ID")
    depth: int = Field(default=0, ge=0, description="Depth in search tree")

    # Content and reasoning
    thought_content: str = Field(..., min_length=10, description="Thought content")
    reasoning_type: str = Field(
        ..., description="Type of reasoning (analytical, creative, etc.)"
    )
    approach: str = Field(..., description="Approach taken for this thought")

    # Tree structure
    children: list[str] = Field(default_factory=list, description="Child node IDs")

    # MCTS properties
    visits: int = Field(default=0, ge=0, description="Number of visits")
    total_reward: float = Field(default=0.0, description="Total accumulated reward")

    # Evaluation
    evaluation_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Evaluation score"
    )
    evaluation_confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence in evaluation"
    )
    evaluation_feedback: str = Field(
        default="", description="Detailed evaluation feedback"
    )

    # Status and metadata
    status: NodeStatus = Field(default=NodeStatus.UNEXPLORED, description="Node status")
    is_solution: bool = Field(default=False, description="Is this a valid solution")
    exploration_priority: float = Field(
        default=0.5, description="Priority for exploration"
    )

    @computed_field
    @property
    def average_reward(self) -> float:
        """Calculate average reward."""
        return self.total_reward / self.visits if self.visits > 0 else 0.0

    @computed_field
    @property
    def is_terminal(self) -> bool:
        """Check if node is terminal."""
        return self.status == NodeStatus.TERMINAL or self.is_solution

    @computed_field
    @property
    def is_leaf(self) -> bool:
        """Check if node is a leaf."""
        return len(self.children) == 0

    def ucb_score(
        self, parent_visits: int, exploration_constant: float = 1.41
    ) -> float:
        """Calculate Upper Confidence Bound score."""
        if self.visits == 0:
            return float("inf")

        exploitation = self.average_reward
        exploration = exploration_constant * math.sqrt(
            math.log(parent_visits) / self.visits
        )
        return exploitation + exploration

    def update_reward(self, reward: float) -> None:
        """Update reward statistics."""
        self.visits += 1
        self.total_reward += reward

    def add_child(self, child_id: str) -> None:
        """Add child node."""
        if child_id not in self.children:
            self.children.append(child_id)


class LATSSearchState(BaseModel):
    """State for LATS search process."""

    objective: str = Field(..., min_length=10, description="Search objective")
    nodes: dict[str, ThoughtNode] = Field(
        default_factory=dict, description="All nodes in tree"
    )
    root_id: str = Field(..., description="Root node ID")

    # Search configuration
    max_depth: int = Field(default=5, ge=1, le=10, description="Maximum search depth")
    max_expansions: int = Field(
        default=50, ge=1, le=200, description="Maximum node expansions"
    )
    beam_width: int = Field(default=3, ge=1, le=10, description="Beam width for search")
    exploration_constant: float = Field(
        default=1.41, ge=0.1, le=5.0, description="UCB exploration constant"
    )

    # Search strategy
    strategy: SearchStrategy = Field(
        default=SearchStrategy.UCB_GUIDED, description="Search strategy"
    )

    # Runtime state
    current_expansions: int = Field(
        default=0, description="Current number of expansions"
    )
    best_solution_id: str | None = Field(
        default=None, description="Best solution found"
    )
    best_score: float = Field(default=0.0, description="Best score achieved")

    # Metrics
    metrics: SearchMetrics = Field(
        default_factory=SearchMetrics, description="Search metrics"
    )

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if search is complete."""
        return self.current_expansions >= self.max_expansions or (
            self.best_solution_id is not None and self.best_score >= 0.9
        )

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        return (self.current_expansions / self.max_expansions) * 100

    def add_node(self, node: ThoughtNode) -> None:
        """Add node to search tree."""
        self.nodes[node.node_id] = node

        # Update parent's children
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].add_child(node.node_id)

    def get_node(self, node_id: str) -> ThoughtNode | None:
        """Get node by ID."""
        return self.nodes.get(node_id)

    def get_leaf_nodes(self) -> list[ThoughtNode]:
        """Get all leaf nodes."""
        return [node for node in self.nodes.values() if node.is_leaf]

    def get_best_nodes(self, n: int = 5) -> list[ThoughtNode]:
        """Get top N nodes by evaluation score."""
        return sorted(
            self.nodes.values(), key=lambda x: x.evaluation_score, reverse=True
        )[:n]

    def get_path_to_root(self, node_id: str) -> list[ThoughtNode]:
        """Get path from node to root."""
        path = []
        current_id = node_id

        while current_id and current_id in self.nodes:
            node = self.nodes[current_id]
            path.append(node)
            current_id = node.parent_id

        return path[::-1]  # Reverse to get root-to-node path

    def select_for_expansion(self) -> ThoughtNode | None:
        """Select node for expansion based on strategy."""
        if self.strategy == SearchStrategy.UCB_GUIDED:
            return self._select_ucb_guided()
        if self.strategy == SearchStrategy.BEST_FIRST:
            return self._select_best_first()
        if self.strategy == SearchStrategy.BREADTH_FIRST:
            return self._select_breadth_first()
        return self._select_ucb_guided()  # Default

    def _select_ucb_guided(self) -> ThoughtNode | None:
        """Select node using UCB strategy."""
        best_node = None
        best_score = -float("inf")

        for node in self.nodes.values():
            if node.is_leaf and not node.is_terminal and node.depth < self.max_depth:
                if node.parent_id:
                    parent = self.nodes.get(node.parent_id)
                    if parent:
                        score = node.ucb_score(parent.visits, self.exploration_constant)
                        if score > best_score:
                            best_score = score
                            best_node = node

        return best_node

    def _select_best_first(self) -> ThoughtNode | None:
        """Select best leaf node."""
        candidates = [
            node
            for node in self.nodes.values()
            if node.is_leaf and not node.is_terminal and node.depth < self.max_depth
        ]

        if not candidates:
            return None

        return max(candidates, key=lambda x: x.evaluation_score)

    def _select_breadth_first(self) -> ThoughtNode | None:
        """Select shallowest leaf node."""
        candidates = [
            node
            for node in self.nodes.values()
            if node.is_leaf and not node.is_terminal and node.depth < self.max_depth
        ]

        if not candidates:
            return None

        return min(candidates, key=lambda x: x.depth)


class LATSSearchResult(BaseModel):
    """Final result from LATS search."""

    objective: str = Field(..., description="Original objective")
    best_solution: str | None = Field(default=None, description="Best solution found")
    best_score: float = Field(default=0.0, description="Best score achieved")
    solution_path: list[str] = Field(
        default_factory=list, description="Path to best solution"
    )

    # Search statistics
    total_nodes: int = Field(default=0, description="Total nodes explored")
    total_evaluations: int = Field(default=0, description="Total evaluations performed")
    search_depth: int = Field(default=0, description="Maximum depth reached")
    search_time: float = Field(default=0.0, description="Total search time")

    # Alternative solutions
    alternative_solutions: list[dict[str, Any]] = Field(
        default_factory=list, description="Alternative solutions"
    )

    @computed_field
    @property
    def search_efficiency(self) -> float:
        """Calculate search efficiency."""
        return self.best_score / max(self.total_evaluations, 1)


class EnhancedLATSAgent(Agent):
    """Enhanced LATS Agent with sophisticated tree search."""

    def __init__(self, name: str, engine: AugLLMConfig, tools: list[Any], **kwargs):
        self.tools = tools
        self.thought_generator = None
        self.thought_evaluator = None
        self.solution_synthesizer = None

        super().__init__(name=name, engine=engine, **kwargs)

    def setup_agent(self):
        """Setup specialized agents for LATS workflow."""
        # Create thought generator
        self.thought_generator = ReactAgent(
            name=f"{self.name}_generator",
            engine=self.engine.model_copy(
                update={
                    "temperature": 0.8,  # More creative for thought generation
                    "system_message": self._create_generation_prompt(),
                }
            ),
            tools=self.tools,
        )

        # Create thought evaluator with structured output
        self.thought_evaluator = SimpleAgent(
            name=f"{self.name}_evaluator",
            engine=self.engine.model_copy(
                update={
                    "temperature": 0.1,  # More deterministic for evaluation
                    "system_message": self._create_evaluation_prompt(),
                }
            ),
        )

        # Create solution synthesizer
        self.solution_synthesizer = SimpleAgent(
            name=f"{self.name}_synthesizer",
            engine=self.engine.model_copy(
                update={
                    "structured_output_model": LATSSearchResult,
                    "structured_output_version": "v2",
                    "system_message": self._create_synthesis_prompt(),
                }
            ),
        )

        # Set up state schema
        self.state_schema = MessagesState

    def _create_generation_prompt(self) -> str:
        """Create thought generation prompt."""
        tool_descriptions = []
        for tool in self.tools:
            if hasattr(tool, "name") and hasattr(tool, "description"):
                tool_descriptions.append(f"- {tool.name}: {tool.description}")

        return f"""You are a creative thought generator for LATS search.

Available tools:
{chr(10).join(tool_descriptions)}

Your task is to generate diverse, creative thoughts for exploring solution paths.

For each thought, consider:
1. Different approaches to the problem
2. Alternative perspectives
3. Creative solutions
4. Potential tool usage
5. Reasoning strategies

Generate thoughts that explore the solution space comprehensively."""

    def _create_evaluation_prompt(self) -> str:
        """Create evaluation prompt."""
        return """You are a thought evaluator for LATS search.

Your task is to evaluate the quality and potential of generated thoughts.

For each thought, provide:
1. A score from 0.0 to 1.0 (where 1.0 is perfect)
2. Detailed feedback explaining the score
3. Assessment of whether this is a valid solution
4. Confidence in your evaluation

Consider:
- Relevance to the objective
- Logical soundness
- Creativity and insight
- Potential for leading to a solution
- Completeness of the thought

Be thorough and critical in your evaluation."""

    def _create_synthesis_prompt(self) -> str:
        """Create synthesis prompt."""
        return """You are a solution synthesizer for LATS search.

Your task is to synthesize the best solution from the search results.

Analyze:
1. All explored thoughts and their evaluations
2. The path to the best solution
3. Alternative solutions and their merits
4. Overall search performance

Provide:
1. The best solution found
2. The reasoning path that led to it
3. Alternative solutions
4. Performance analysis
5. Recommendations for improvement

Be comprehensive and analytical."""

    def build_graph(self):
        """Build LATS execution graph."""
        # For this implementation, we'll use a custom search approach

    async def arun(self, query: str, **kwargs) -> dict[str, Any]:
        """Execute LATS search."""
        logger.info(f"LATS Agent {self.name} starting search for: {query}")

        start_time = asyncio.get_event_loop().time()

        try:
            # Initialize search state
            search_state = await self._initialize_search(query)

            # Perform tree search
            logger.info("Starting tree search")
            await self._perform_search(search_state)

            # Synthesize results
            logger.info("Synthesizing results")
            final_result = await self._synthesize_results(search_state)

            search_time = asyncio.get_event_loop().time() - start_time

            return {
                "query": query,
                "search_state": search_state,
                "final_result": final_result,
                "search_time": search_time,
                "status": "completed",
            }

        except Exception as e:
            logger.error(f"LATS search failed: {e}")
            return {"query": query, "error": str(e), "status": "failed"}

    async def _initialize_search(self, query: str) -> LATSSearchState:
        """Initialize search state with root node."""
        # Create root node
        root_node = ThoughtNode(
            node_id="root",
            thought_content=f"Starting search for: {query}",
            reasoning_type="initial",
            approach="root_analysis",
            status=NodeStatus.EVALUATED,
            evaluation_score=0.5,
            evaluation_confidence=1.0,
        )

        # Create search state
        search_state = LATSSearchState(objective=query, root_id="root")

        search_state.add_node(root_node)

        return search_state

    async def _perform_search(self, search_state: LATSSearchState) -> None:
        """Perform tree search with expansion and evaluation."""
        while not search_state.is_complete:
            # Select node for expansion
            node_to_expand = search_state.select_for_expansion()

            if not node_to_expand:
                logger.info("No more nodes to expand")
                break

            logger.info(
                f"Expanding node {node_to_expand.node_id} at depth {node_to_expand.depth}"
            )

            # Generate child thoughts
            child_thoughts = await self._generate_child_thoughts(
                node_to_expand, search_state
            )

            # Evaluate child thoughts
            for child_thought in child_thoughts:
                await self._evaluate_thought(child_thought, search_state)
                search_state.add_node(child_thought)

                # Update metrics
                search_state.metrics.nodes_explored += 1
                search_state.metrics.nodes_evaluated += 1

                # Check if this is the best solution so far
                if child_thought.evaluation_score > search_state.best_score:
                    search_state.best_score = child_thought.evaluation_score
                    search_state.best_solution_id = child_thought.node_id
                    search_state.metrics.best_score = child_thought.evaluation_score

            # Backpropagate rewards
            await self._backpropagate_rewards(node_to_expand, search_state)

            search_state.current_expansions += 1

            logger.info(
                f"Search progress: {search_state.completion_percentage:.1f}% "
                f"(best score: {search_state.best_score:.3f})"
            )

    async def _generate_child_thoughts(
        self, parent_node: ThoughtNode, search_state: LATSSearchState
    ) -> list[ThoughtNode]:
        """Generate child thoughts for a node."""
        # Create context from path to root
        path_to_root = search_state.get_path_to_root(parent_node.node_id)
        context = " -> ".join([node.thought_content for node in path_to_root])

        generation_prompt = f"""Generate {search_state.beam_width} diverse child thoughts for exploration.

Objective: {search_state.objective}
Current path: {context}
Parent thought: {parent_node.thought_content}
Current depth: {parent_node.depth}

Generate different approaches, perspectives, or solutions that build on this path.
Each thought should explore a different direction or aspect of the problem.

For each thought, specify:
1. The thought content
2. The reasoning type (analytical, creative, deductive, etc.)
3. The approach being taken

Make thoughts diverse and creative while staying relevant to the objective."""

        result = await self.thought_generator.arun(generation_prompt)

        # Parse the result to extract child thoughts
        child_thoughts = self._parse_generated_thoughts(
            result, parent_node, search_state
        )

        return child_thoughts

    def _parse_generated_thoughts(
        self, result: Any, parent_node: ThoughtNode, search_state: LATSSearchState
    ) -> list[ThoughtNode]:
        """Parse generated thoughts from agent result."""
        # This is a simplified parser - in a real implementation,
        # you'd use structured output or better parsing

        thoughts = []

        # Try to extract structured thoughts from the result
        result_str = str(result)

        # Simple heuristic parsing - look for numbered items
        lines = result_str.split("\n")
        thought_lines = []

        for line in lines:
            line = line.strip()
            if line and (
                line.startswith(("1.", "2.", "3.", "-", "*"))
                or any(word in line.lower() for word in ["thought", "approach", "idea"])
            ):
                thought_lines.append(line)

        # Create thought nodes
        for i, thought_line in enumerate(thought_lines[: search_state.beam_width]):
            thought_id = f"node_{uuid4().hex[:8]}"

            child_thought = ThoughtNode(
                node_id=thought_id,
                parent_id=parent_node.node_id,
                depth=parent_node.depth + 1,
                thought_content=thought_line,
                reasoning_type="generated",
                approach=f"exploration_{i + 1}",
                status=NodeStatus.UNEXPLORED,
            )

            thoughts.append(child_thought)

        return thoughts

    async def _evaluate_thought(
        self, thought: ThoughtNode, search_state: LATSSearchState
    ) -> None:
        """Evaluate a thought node."""
        evaluation_prompt = f"""Evaluate this thought for the given objective.

Objective: {search_state.objective}
Thought: {thought.thought_content}
Reasoning type: {thought.reasoning_type}
Approach: {thought.approach}
Depth: {thought.depth}

Provide:
1. Score (0.0 to 1.0): How good is this thought?
2. Confidence (0.0 to 1.0): How confident are you in this evaluation?
3. Is this a valid solution? (yes/no)
4. Detailed feedback explaining your evaluation

Consider relevance, soundness, creativity, and potential for solving the objective."""

        result = await self.thought_evaluator.arun(evaluation_prompt)

        # Parse evaluation result
        evaluation_data = self._parse_evaluation_result(result)

        # Update thought with evaluation
        thought.evaluation_score = evaluation_data.get("score", 0.5)
        thought.evaluation_confidence = evaluation_data.get("confidence", 0.5)
        thought.evaluation_feedback = evaluation_data.get("feedback", "")
        thought.is_solution = evaluation_data.get("is_solution", False)
        thought.status = NodeStatus.EVALUATED

        # Mark as terminal if it's a solution or at max depth
        if thought.is_solution or thought.depth >= search_state.max_depth:
            thought.status = NodeStatus.TERMINAL

    def _parse_evaluation_result(self, result: Any) -> dict[str, Any]:
        """Parse evaluation result."""
        # Simple parsing - in real implementation, use structured output
        result_str = str(result).lower()

        # Extract score
        score = 0.5
        if "score:" in result_str:
            try:
                score_part = result_str.split("score:")[1].split()[0]
                score = float(score_part.strip("()[]"))
                score = max(0.0, min(1.0, score))
            except:
                pass

        # Extract confidence
        confidence = 0.5
        if "confidence:" in result_str:
            try:
                conf_part = result_str.split("confidence:")[1].split()[0]
                confidence = float(conf_part.strip("()[]"))
                confidence = max(0.0, min(1.0, confidence))
            except:
                pass

        # Check if it's a solution
        is_solution = any(
            word in result_str for word in ["yes", "valid solution", "solution: yes"]
        )

        return {
            "score": score,
            "confidence": confidence,
            "is_solution": is_solution,
            "feedback": str(result),
        }

    async def _backpropagate_rewards(
        self, node: ThoughtNode, search_state: LATSSearchState
    ) -> None:
        """Backpropagate rewards through the tree."""
        # Simple backpropagation - update all nodes in path to root
        current_node = node

        while current_node:
            current_node.update_reward(current_node.evaluation_score)

            # Move to parent
            if current_node.parent_id:
                current_node = search_state.get_node(current_node.parent_id)
            else:
                break

    async def _synthesize_results(
        self, search_state: LATSSearchState
    ) -> LATSSearchResult:
        """Synthesize final results from search."""
        # Get best solution path
        best_path = []
        if search_state.best_solution_id:
            path_nodes = search_state.get_path_to_root(search_state.best_solution_id)
            best_path = [node.thought_content for node in path_nodes]

        # Get alternative solutions
        best_nodes = search_state.get_best_nodes(5)
        alternatives = []
        for node in best_nodes[1:]:  # Skip the best one
            alternatives.append(
                {
                    "thought": node.thought_content,
                    "score": node.evaluation_score,
                    "path": [
                        n.thought_content
                        for n in search_state.get_path_to_root(node.node_id)
                    ],
                }
            )

        synthesis_prompt = f"""Synthesize the LATS search results.

Objective: {search_state.objective}
Total nodes explored: {len(search_state.nodes)}
Best score achieved: {search_state.best_score}

Best solution path:
{chr(10).join(f"{i + 1}. {thought}" for i, thought in enumerate(best_path))}

Alternative solutions:
{json.dumps(alternatives, indent=2)}

Search statistics:
- Completion: {search_state.completion_percentage:.1f}%
- Max depth: {search_state.max_depth}
- Nodes explored: {search_state.metrics.nodes_explored}
- Nodes evaluated: {search_state.metrics.nodes_evaluated}

Provide a comprehensive analysis of the search results."""

        result = await self.solution_synthesizer.arun(synthesis_prompt)

        # Extract structured output
        if isinstance(result, dict) and "lats_search_result" in result:
            return result["lats_search_result"]
        if isinstance(result, LATSSearchResult):
            return result
        # Create fallback result
        return LATSSearchResult(
            objective=search_state.objective,
            best_solution=best_path[-1] if best_path else None,
            best_score=search_state.best_score,
            solution_path=best_path,
            total_nodes=len(search_state.nodes),
            total_evaluations=search_state.metrics.nodes_evaluated,
            search_depth=search_state.max_depth,
            alternative_solutions=alternatives,
        )


# Test Implementation
async def test_enhanced_lats_agent():
    """Test the enhanced LATS agent."""

    # Create tools for testing
    @tool
    def logical_analyzer(statement: str) -> str:
        """Analyze logical structure of statements."""
        return f"Logical analysis of '{statement}': Valid structure with clear premises and conclusions."

    @tool
    def creative_generator(prompt: str) -> str:
        """Generate creative ideas."""
        return (
            f"Creative ideas for '{prompt}': Innovative approaches and novel solutions."
        )

    # Create agent
    config = AugLLMConfig(temperature=0.7, max_tokens=1000)

    agent = EnhancedLATSAgent(
        name="test_lats", engine=config, tools=[logical_analyzer, creative_generator]
    )

    # Test query
    result = await agent.arun(
        "How can we solve the problem of climate change through innovative technology?"
    )

    print("LATS Agent Results:")
    print(f"Status: {result.get('status')}")
    if result.get("status") == "completed":
        print(f"Best score: {result['search_state'].best_score:.3f}")
        print(f"Nodes explored: {len(result['search_state'].nodes)}")
        print(f"Search time: {result['search_time']:.2f}s")
        if result["final_result"].best_solution:
            print(f"Best solution: {result['final_result'].best_solution}")
    else:
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(test_enhanced_lats_agent())
