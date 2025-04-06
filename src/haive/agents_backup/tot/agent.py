#from src.config.model_config import *

from src.haive.agents.tot.models import Problem,Candidate,ScoredCandidate

from langgraph.types import Command
# from.agents.tot.utils import generate_candidates,score_candidates,select_best_candidate
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from typing import List, Optional
import uuid
# Configuration schema
from pydantic import BaseModel,Field
from src.haive.core.engine.agent.agent import AgentArchitectureConfig,AgentArchitecture
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.agents.tot.state import ToTState
from src.haive.core.models.llm.base import AzureLLMConfig

class TOTAgentConfig(AgentArchitectureConfig):
    """Configuration for the ToT agent"""
    aug_llm_config: AugLLMConfig = Field(default=AugLLMConfig(name="solution_generator",llm_config=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})),description="The configuration for the LLM")
    #tree_config: TreeConfig = Field(default=TreeConfig())
    state_schema: ToTState = Field(default=ToTState)
    max_depth: int = Field(description="Maximum depth of the ToT tree",default=3)
    threshold: float = Field(description="Threshold for the ToT agent",default=0.5)
    k: int = Field(description="Number of candidates to consider",default=5)
# Tree of Thought Agent
class ToTAgent(AgentArchitecture):
    def __init__(self, config: TOTAgentConfig=TOTAgentConfig()):
        super().__init__(config)
        self.k = config.k
        self.max_depth = config.max_depth
        self.threshold = config.threshold
        #sek
        #self.llm = AzureChatOpenAI(model=model)
        #self.memory = MemorySaver()
        #self.graph = self._build_graph()
        #self.tot_config = ToTConfig()
        #self.config = config or {"configurable": {"thread_id": str(uuid.uuid4())}}

    def setup_workflow(self):
        #graph = StateGraph(state_schema=ToTState)

        # Define nodes  
        self.graph.add_node("generate_candidates", self._generate_candidates)
        self.graph.add_node("score_candidates", self._score_candidates)
        self.graph.add_node("select_best", self._select_best)

        # Define edges
        self.graph.add_conditional_edges(
            "generate_candidates", self._should_continue, ["score_candidates", END]
        )
        self.graph.add_edge("score_candidates", "select_best")
        self.graph.add_edge("select_best", END)
        self.graph.add_edge(START, "generate_candidates")

        return self.graph.compile(checkpointer=self.memory)

    def _generate_candidates(self, state: ToTState):
        prompt = f"Generate up to {self.k} solutions for the problem: {state.get('problem').description}"
        try:
            response = self.aug_llm_runnable.invoke([HumanMessage(content=prompt)])
            candidates = [
                Candidate(candidate=resp.strip()) for resp in response.content.split("\n") if resp.strip()
            ]
            return Command(update={"candidates": candidates, "depth": state.get('depth') + 1})
        except Exception as e:
            print(f"Error generating candidates: {e}")
            return Command(update={"candidates": [], "depth": state.get('depth')})

    def _score_candidates(self, state: ToTState):
        scored_candidates = []
        for candidate in state.get("candidates"):
            try:
                # Refined prompt explicitly requesting a numeric score
                prompt = (
                    f"Evaluate the following solution and provide a score between 0 and 1 (as a number only):\n\n"
                    f"{candidate.candidate}"
                )
                response = self.aug_llm_runnable.invoke([HumanMessage(content=prompt)])
                
                # Parse the score from the response
                score = self._parse_score(response.content)
                if score is not None:
                    scored_candidates.append(
                    ScoredCandidate(
                        candidate=candidate,
                        score=score,
                        feedback="Scored successfully"
                    )
                    )
                else:
                    print(f"Failed to parse score for candidate: {candidate.candidate}")
            except Exception as e:
                print(f"Unexpected error scoring candidate '{candidate.candidate}': {e}")
        return Command(update={"scored_candidates": scored_candidates})

    def _parse_score(self, response: str) -> Optional[float]:
        """Parse a numeric score from the LLM response."""
        try:
            # Attempt to convert response to float
            score = float(response.strip())
            if 0.0 <= score <= 1.0:
                return score
            else:
                print(f"Score out of bounds (0-1): {response}")
        except ValueError:
            print(f"Invalid score format: {response}")
            return None

    # Modified _select_best method
    def _select_best(self, state: ToTState):
        # Select the best candidate based on score
        if state.get('scored_candidates'):
            best_candidate = max(state.get('scored_candidates'), key=lambda x: x.score)
            return Command(update={"best_candidate": best_candidate})
        else:
            return Command(update={"best_candidate": None})

    def _should_continue(self, state: ToTState):
        # Check if we should continue generating candidates
        if state.get('depth') >= self.max_depth or not state.get('candidates'):
            return END
        return "score_candidates"

    def run(self, problem_description: str):
        # Initialize the state
        initial_state = ToTState(
            problem=Problem(description=problem_description),
            candidates=[],
            scored_candidates=[],
            depth=0,
        )
        # Execute the graph
        result = None
        for step in self.app.stream(initial_state, config=self.runnable_config):
            result = step
            print(step)
        return result

a = ToTAgent()
#a.run("What is the capital of France?")
#rom src.core.utils.visualize_graph_utils import render_and_display_graph
#render_and_display_graph(a.graph,output_name="tot_graph.png")       
a.run("What is the capital of France?")