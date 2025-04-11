# src/haive/agents/hbspi/rewoo_reasoner.py

from __future__ import annotations
import asyncio
import uuid
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from enum import Enum
from pydantic import BaseModel, Field
import logging
from uuid import uuid4
# Import components
from src.haive.agents.HBSPI.parallel_plan_tree import ParallelPlanTree, PlanTreeNode, PlanNodeType, Branch
from src.haive.agents.HBSPI.belief_space import BeliefSpaceManager, Belief, BeliefType, Evidence, EvidenceType
from src.haive.agents.HBSPI.introspection import IntrospectionEngine, IntrospectionInsight, IntrospectionTarget
from src.haive.core.engine.aug_llm import AugLLMConfig

# Set up logging
logger = logging.getLogger(__name__)

class ReasoningStrategy(str, Enum):
    """Reasoning strategies that can be employed."""
    REWOO = "rewoo"  # Reasoning Without Observation
    FORWARD_CHAINING = "forward_chaining"
    BACKWARD_CHAINING = "backward_chaining"
    ABDUCTIVE = "abductive"
    COUNTERFACTUAL = "counterfactual"
    SOCRATIC = "socratic"
    CONSTRAINT_SATISFACTION = "constraint_satisfaction"

class HypotheticalEvidence(BaseModel):
    """Structured representation of hypothetical evidence."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    description: str = Field(..., description="Description of the evidence")
    hypothesis_id: str = Field(..., description="ID of the associated hypothesis")
    supports_confidence: float = Field(default=0.5, description="How strongly it would support the hypothesis if true")
    ease_of_validation: float = Field(default=0.5, description="How easy it would be to validate this evidence")
    validation_status: str = Field(default="pending", description="pending, validated, refuted")
    validation_explanation: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReWOOReasoner(BaseModel):
    """
    ReWOO (Reasoning Without Observation) reasoner with hypothetical evidence.
    
    This component implements:
    - Hypothetical evidence generation and validation
    - Parallel exploration of multiple reasoning paths
    - Structured belief space tracking
    - Introspective evaluation of reasoning
    """
    # Main components
    plan_tree: ParallelPlanTree
    belief_space: BeliefSpaceManager
    introspection: IntrospectionEngine
    
    # ReWOO-specific structures
    hypothetical_evidence: Dict[str, HypotheticalEvidence] = Field(default_factory=dict)
    
    # Configuration
    name: str = Field(..., description="Name of this reasoner")
    description: str = Field(..., description="Description of the reasoner's purpose")
    primary_strategy: ReasoningStrategy = Field(default=ReasoningStrategy.REWOO)
    alternate_strategies: List[ReasoningStrategy] = Field(default_factory=list)
    max_hypothetical_evidence: int = Field(default=10, description="Maximum pieces of hypothetical evidence to track")
    introspection_frequency: float = Field(default=0.3, description="How often to perform introspection (0-1)")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # State tracking
    reasoning_steps: List[Dict[str, Any]] = Field(default_factory=list)
    current_phase: str = Field(default="initialization")
    
    # Engine references
    planning_engine: Optional[AugLLMConfig] = Field(default=None)
    evidence_engine: Optional[AugLLMConfig] = Field(default=None)
    belief_engine: Optional[AugLLMConfig] = Field(default=None)
    introspection_engine: Optional[AugLLMConfig] = Field(default=None)
    
    # =============================================
    # Creation and initialization
    # =============================================
    
    @classmethod
    def create(cls, name: str, description: str, 
              planning_engine: Optional[AugLLMConfig] = None,
              evidence_engine: Optional[AugLLMConfig] = None,
              belief_engine: Optional[AugLLMConfig] = None,
              introspection_engine: Optional[AugLLMConfig] = None,
              **kwargs) -> ReWOOReasoner:
        """Create a new ReWOO reasoner with all components."""
        # Create plan tree
        plan_tree = ParallelPlanTree.create(
            name=f"{name}_plan_tree",
            description=f"Planning tree for {name}"
        )
        
        # Create belief space
        belief_space = BeliefSpaceManager.create(
            name=f"{name}_belief_space",
            description=f"Belief space for {name}"
        )
        
        # Create introspection engine
        introspection = IntrospectionEngine.create(
            name=f"{name}_introspection",
            description=f"Introspection engine for {name}"
        )
        
        # Create the reasoner
        return cls(
            name=name,
            description=description,
            plan_tree=plan_tree,
            belief_space=belief_space,
            introspection=introspection,
            planning_engine=planning_engine,
            evidence_engine=evidence_engine,
            belief_engine=belief_engine,
            introspection_engine=introspection_engine,
            **kwargs
        )
    
    # =============================================
    # ReWOO reasoning methods
    # =============================================
    
    def generate_hypothetical_evidence(self, hypothesis_content: str, count: int = 3) -> List[HypotheticalEvidence]:
        """
        Generate hypothetical evidence that would support or refute a hypothesis.
        
        This is the core ReWOO mechanism: imagining evidence that would be observable
        if a hypothesis were true, and then validating that evidence.
        """
        # Create a hypothesis in the belief space
        hypothesis = self.belief_space.add_belief(
            content=hypothesis_content,
            type=BeliefType.HYPOTHESIS,
            confidence=0.5
        )
        
        # Track a description of this step
        self.reasoning_steps.append({
            "phase": "hypothesis_generation",
            "description": f"Generated hypothesis: {hypothesis_content}",
            "hypothesis_id": hypothesis.id
        })
        
        # In a real implementation, this would use the evidence engine
        # For this example, we'll generate simple hypothetical evidence
        evidence_list = []
        
        for i in range(count):
            evidence = HypotheticalEvidence(
                description=f"Hypothetical evidence {i+1} related to: {hypothesis_content[:30]}...",
                hypothesis_id=hypothesis.id,
                supports_confidence=0.6 + (i * 0.1),  # Varying confidence
                ease_of_validation=0.7 - (i * 0.15)   # Varying ease of validation
            )
            
            # Store in our tracking structure
            self.hypothetical_evidence[evidence.id] = evidence
            
            # Create corresponding evidence in belief space
            belief_evidence = self.belief_space.add_hypothetical_evidence(
                content=evidence.description,
                type=EvidenceType.COUNTERFACTUAL,
                strength=evidence.supports_confidence,
                related_belief_ids=[hypothesis.id],
                metadata={
                    "hypothetical_evidence_id": evidence.id,
                    "ease_of_validation": evidence.ease_of_validation
                }
            )
            
            # Create evidence node in plan tree
            evidence_node = self.plan_tree.add_evidence_node(
                content=evidence.description,
                parent_id=self.plan_tree.branches[self.plan_tree.main_branch_id].root_node_id,
                status="pending"
            )
            
            # Add to response list
            evidence_list.append(evidence)
            
            # Track step
            self.reasoning_steps.append({
                "phase": "evidence_generation",
                "description": f"Generated hypothetical evidence: {evidence.description}",
                "evidence_id": evidence.id,
                "evidence_node_id": evidence_node.id
            })
        
        return evidence_list
    
    def validate_hypothetical_evidence(self, evidence_id: str, 
                                      is_valid: bool, 
                                      explanation: Optional[str] = None) -> Tuple[HypotheticalEvidence, Belief]:
        """
        Validate or refute a piece of hypothetical evidence.
        
        This is the second part of ReWOO: determining if the hypothetical evidence
        is actually true, which in turn supports or refutes the hypothesis.
        """
        if evidence_id not in self.hypothetical_evidence:
            raise ValueError(f"Evidence {evidence_id} not found")
            
        # Update our tracking structure
        evidence = self.hypothetical_evidence[evidence_id]
        evidence.validation_status = "validated" if is_valid else "refuted"
        if explanation:
            evidence.validation_explanation = explanation
        self.hypothetical_evidence[evidence_id] = evidence
        
        # Update corresponding evidence in belief space
        # Find the evidence in belief space
        belief_evidence_id = None
        for e_id, e in self.belief_space.evidence.items():
            if e.metadata.get("hypothetical_evidence_id") == evidence_id:
                belief_evidence_id = e_id
                break
                
        if not belief_evidence_id:
            raise ValueError(f"Corresponding evidence not found in belief space")
            
        # Update in belief space
        belief_evidence = self.belief_space.validate_hypothetical_evidence(
            belief_evidence_id,
            is_valid,
            explanation
        )
        
        # Update in plan tree
        # Find evidence node in plan tree
        evidence_node_id = None
        for node_id, node in self.plan_tree.nodes.items():
            if node.type == PlanNodeType.EVIDENCE and node.content == evidence.description:
                evidence_node_id = node_id
                break
                
        if evidence_node_id:
            self.plan_tree.update_evidence_status(
                evidence_node_id,
                "validated" if is_valid else "refuted",
                explanation
            )
        
        # Update associated hypothesis belief
        hypothesis = None
        if evidence.hypothesis_id in self.belief_space.beliefs:
            hypothesis = self.belief_space.beliefs[evidence.hypothesis_id]
            
            # Adjust confidence based on validation
            adjustment = 0.0
            if is_valid:
                # Evidence supports hypothesis
                adjustment = evidence.supports_confidence * 0.2  # Scale the adjustment
            else:
                # Evidence refutes hypothesis  
                adjustment = -evidence.supports_confidence * 0.2  # Negative adjustment
                
            hypothesis = self.belief_space.update_belief_confidence(
                evidence.hypothesis_id,
                adjustment=adjustment
            )
        
        # Track this step
        self.reasoning_steps.append({
            "phase": "evidence_validation",
            "description": f"Validated evidence: {evidence.description} - {'VALID' if is_valid else 'REFUTED'}",
            "evidence_id": evidence.id,
            "is_valid": is_valid,
            "explanation": explanation,
            "confidence_adjustment": adjustment if hypothesis else 0.0
        })
        
        return evidence, hypothesis
    
    def create_parallel_reasoning_branches(self, 
                                         base_hypothesis: str, 
                                         alternatives: List[str]) -> List[Branch]:
        """
        Create parallel branches to explore multiple hypotheses simultaneously.
        
        This enables exploring different possibilities in parallel and later 
        merging the insights gained from each branch.
        """
        branches = []
        
        # First create the base branch if it doesn't exist
        if len(self.plan_tree.branches) == 0:
            base_branch = self.plan_tree.branches[self.plan_tree.main_branch_id]
        else:
            # Create a branch for the base hypothesis
            base_branch = self.plan_tree.create_branch(
                name=f"Branch for: {base_hypothesis[:30]}...",
                description=f"Exploration of hypothesis: {base_hypothesis}"
            )
            
            # Create hypothesis in belief space
            base_belief = self.belief_space.add_belief(
                content=base_hypothesis,
                type=BeliefType.HYPOTHESIS,
                confidence=0.5
            )
            
            # Create hypothesis node
            hypothesis_node = self.plan_tree.add_node(
                type=PlanNodeType.HYPOTHESIS,
                content=base_hypothesis,
                branch_id=base_branch.id,
                hypothesis_id=base_belief.id
            )
            
            branches.append(base_branch)
            
            # Track step
            self.reasoning_steps.append({
                "phase": "branch_creation",
                "description": f"Created branch for hypothesis: {base_hypothesis}",
                "branch_id": base_branch.id,
                "hypothesis_id": base_belief.id
            })
        
        # Create branches for alternative hypotheses
        for alt_hypothesis in alternatives:
            # Create branch in plan tree
            branch = self.plan_tree.create_branch(
                name=f"Alternative: {alt_hypothesis[:30]}...",
                description=f"Exploration of alternative hypothesis: {alt_hypothesis}"
            )
            
            # Create hypothesis in belief space
            belief = self.belief_space.add_belief(
                content=alt_hypothesis,
                type=BeliefType.HYPOTHESIS,
                confidence=0.5
            )
            
            # Create hypothesis node
            hypothesis_node = self.plan_tree.add_node(
                type=PlanNodeType.HYPOTHESIS,
                content=alt_hypothesis,
                branch_id=branch.id,
                hypothesis_id=belief.id
            )
            
            branches.append(branch)
            
            # Track step
            self.reasoning_steps.append({
                "phase": "branch_creation",
                "description": f"Created branch for alternative hypothesis: {alt_hypothesis}",
                "branch_id": branch.id,
                "hypothesis_id": belief.id
            })
        
        return branches
    
    def merge_branches(self, source_branch_id: str, target_branch_id: str) -> None:
        """
        Merge insights from one reasoning branch into another.
        
        This allows combining the valuable discoveries from parallel explorations.
        """
        # First merge in the plan tree
        self.plan_tree.merge_branches(source_branch_id, target_branch_id, "selective")
        
        # Track step
        self.reasoning_steps.append({
            "phase": "branch_merging",
            "description": f"Merged branch {source_branch_id} into {target_branch_id}",
            "source_branch_id": source_branch_id,
            "target_branch_id": target_branch_id
        })
        
        # Then synthesize beliefs
        # In a real implementation, we would merge beliefs and update confidence
        # For this example, we'll just log the merge
        logger.info(f"Merged branch {source_branch_id} into {target_branch_id}")
    
    # =============================================
    # Introspection methods
    # =============================================
    
    def perform_introspection(self) -> List[IntrospectionInsight]:
        """
        Perform introspective evaluation of current reasoning processes.
        
        Analyzes beliefs, reasoning steps, branches, and evidence to identify
        cognitive biases, logical fallacies, and other reasoning issues.
        """
        insights = []
        
        # 1. Select items to evaluate
        # In a real implementation, this would be more sophisticated
        # For this example, we'll evaluate a sample of beliefs and plan nodes
        
        # Evaluate a sample of beliefs
        sample_beliefs = list(self.belief_space.beliefs.values())[:3]
        for belief in sample_beliefs:
            insight = self.introspection.evaluate_belief(belief)
            insights.append(insight)
            
            # Track step
            self.reasoning_steps.append({
                "phase": "introspection",
                "description": f"Evaluated belief: {belief.content[:30]}...",
                "belief_id": belief.id,
                "insight_id": insight.id
            })
        
        # Evaluate a sample of plan tree nodes
        sample_nodes = list(self.plan_tree.nodes.values())[:3]
        for node in sample_nodes:
            if node.type == PlanNodeType.REASONING:
                insight = self.introspection.evaluate_reasoning_step(node)
            elif node.type == PlanNodeType.EVIDENCE:
                insight = self.introspection.evaluate_evidence(node)
            else:
                insight = self.introspection.evaluate_plan(node)
                
            insights.append(insight)
            
            # Track step
            self.reasoning_steps.append({
                "phase": "introspection",
                "description": f"Evaluated {node.type} node: {node.content[:30]}...",
                "node_id": node.id,
                "insight_id": insight.id
            })
        
        # 2. Evaluate overall process
        process_data = {
            "id": "entire_process",
            "reasoning_steps": self.reasoning_steps,
            "current_phase": self.current_phase
        }
        
        process_insight = self.introspection.evaluate_entire_process(process_data)
        insights.append(process_insight)
        
        # Track step
        self.reasoning_steps.append({
            "phase": "introspection",
            "description": "Evaluated entire reasoning process",
            "insight_id": process_insight.id
        })
        
        return insights
    
    def apply_introspection_insights(self, insights: List[IntrospectionInsight]) -> None:
        """
        Apply insights from introspection to improve reasoning.
        
        Updates beliefs, plans, and strategies based on introspective evaluation.
        """
        for insight in insights:
            # Apply based on target type
            if insight.target_type == IntrospectionTarget.BELIEF:
                # Find the belief
                if insight.target_id in self.belief_space.beliefs:
                    belief = self.belief_space.beliefs[insight.target_id]
                    
                    # Apply the insight
                    updated_belief = self.introspection.apply_insights_to_belief(
                        belief, [insight]
                    )
                    
                    # Update in belief space
                    self.belief_space.beliefs[insight.target_id] = updated_belief
                    
                    # Track step
                    self.reasoning_steps.append({
                        "phase": "insight_application",
                        "description": f"Applied insight to belief: {belief.content[:30]}...",
                        "belief_id": belief.id,
                        "insight_id": insight.id,
                        "confidence_adjustment": insight.confidence_adjustment
                    })
            
            elif insight.target_type == IntrospectionTarget.REASONING_STEP:
                # Find the plan node
                for node_id, node in self.plan_tree.nodes.items():
                    if node_id == insight.target_id and node.type == PlanNodeType.REASONING:
                        # Apply confidence adjustment
                        node.confidence = max(0.01, min(0.99, node.confidence + insight.confidence_adjustment))
                        
                        # Add metadata
                        node.metadata["introspection"] = {
                            "insight_id": insight.id,
                            "critique": insight.critique,
                            "suggested_techniques": [t.value for t in insight.suggested_techniques]
                        }
                        
                        # Update in plan tree
                        self.plan_tree.nodes[node_id] = node
                        
                        # Track step
                        self.reasoning_steps.append({
                            "phase": "insight_application",
                            "description": f"Applied insight to reasoning step: {node.content[:30]}...",
                            "node_id": node.id,
                            "insight_id": insight.id
                        })
                        
                        break
            
            elif insight.target_type == IntrospectionTarget.PLAN:
                # Find the plan node
                if insight.target_id in self.plan_tree.nodes:
                    node = self.plan_tree.nodes[insight.target_id]
                    
                    # Apply the insight
                    updated_node = self.introspection.apply_insights_to_plan(
                        node, [insight]
                    )
                    
                    # Update in plan tree
                    self.plan_tree.nodes[insight.target_id] = updated_node
                    
                    # Track step
                    self.reasoning_steps.append({
                        "phase": "insight_application",
                        "description": f"Applied insight to plan: {node.content[:30]}...",
                        "node_id": node.id,
                        "insight_id": insight.id
                    })
            
            elif insight.target_type == IntrospectionTarget.BRANCH:
                # Find the branch
                if insight.target_id in self.plan_tree.branches:
                    branch = self.plan_tree.branches[insight.target_id]
                    
                    # Apply metadata
                    branch.metadata["introspection"] = {
                        "insight_id": insight.id,
                        "critique": insight.critique,
                        "suggested_techniques": [t.value for t in insight.suggested_techniques]
                    }
                    
                    # Adjust confidence
                    branch.confidence = max(0.01, min(0.99, branch.confidence + insight.confidence_adjustment))
                    
                    # Update in plan tree
                    self.plan_tree.branches[insight.target_id] = branch
                    
                    # Track step
                    self.reasoning_steps.append({
                        "phase": "insight_application",
                        "description": f"Applied insight to branch: {branch.name}",
                        "branch_id": branch.id,
                        "insight_id": insight.id
                    })
            
            elif insight.target_type == IntrospectionTarget.ENTIRE_PROCESS:
                # Apply to overall strategy
                # In a real implementation, this would update reasoning strategies
                
                # For this example, just track that we applied it
                self.metadata["process_insights"] = self.metadata.get("process_insights", []) + [insight.id]
                
                # Track step
                self.reasoning_steps.append({
                    "phase": "insight_application",
                    "description": "Applied insight to entire reasoning process",
                    "insight_id": insight.id
                })
    
    # =============================================
    # High-level reasoning workflow
    # =============================================
    
    def reason_about_query(self, query: str) -> Dict[str, Any]:
        """
        Perform complete reasoning about a query using the ReWOO approach.
        
        This is the main entry point for reasoning, coordinating the entire process.
        """
        # 1. Initialize
        self.current_phase = "initialization"
        self.reasoning_steps.append({
            "phase": "initialization",
            "description": f"Started reasoning about query: {query}",
            "query": query
        })
        
        # 2. Generate hypotheses
        self.current_phase = "hypothesis_generation"
        
        # In a real implementation, we would use the planning engine to generate hypotheses
        # For this example, we'll use hardcoded hypotheses
        main_hypothesis = f"Main hypothesis for: {query}"
        alternative_hypotheses = [
            f"Alternative 1 for: {query}",
            f"Alternative 2 for: {query}"
        ]
        
        # Track step
        self.reasoning_steps.append({
            "phase": "hypothesis_generation",
            "description": f"Generated main hypothesis: {main_hypothesis}",
            "main_hypothesis": main_hypothesis,
            "alternatives": alternative_hypotheses
        })
        
        # 3. Create parallel branches
        self.current_phase = "branch_creation"
        branches = self.create_parallel_reasoning_branches(
            main_hypothesis,
            alternative_hypotheses
        )
        
        # 4. Generate hypothetical evidence
        self.current_phase = "evidence_generation"
        
        # Generate evidence for main hypothesis
        main_hypothesis_id = None
        for belief in self.belief_space.beliefs.values():
            if belief.content == main_hypothesis:
                main_hypothesis_id = belief.id
                break
                
        if main_hypothesis_id:
            hypothetical_evidence = self.generate_hypothetical_evidence(
                main_hypothesis,
                count=3
            )
        
        # 5. Validate evidence (ReWOO core mechanism)
        self.current_phase = "evidence_validation"
        
        # In a real implementation, we would use real validation
        # For this example, we'll simulate some validation results
        if len(self.hypothetical_evidence) > 0:
            # Validate first evidence as true
            first_evidence_id = list(self.hypothetical_evidence.keys())[0]
            self.validate_hypothetical_evidence(
                first_evidence_id,
                True,
                "This evidence was confirmed through analysis."
            )
            
            # Validate second evidence as false
            if len(self.hypothetical_evidence) > 1:
                second_evidence_id = list(self.hypothetical_evidence.keys())[1]
                self.validate_hypothetical_evidence(
                    second_evidence_id,
                    False,
                    "This evidence was refuted through analysis."
                )
        
        # 6. Perform introspection
        self.current_phase = "introspection"
        insights = self.perform_introspection()
        
        # 7. Apply introspection insights
        self.current_phase = "insight_application"
        self.apply_introspection_insights(insights)
        
        # 8. Merge branches and synthesize conclusions
        self.current_phase = "branch_merging"
        
        # Merge alternative branches into main branch
        branch_ids = list(self.plan_tree.branches.keys())
        if len(branch_ids) > 2:  # Main + at least 2 alternatives
            # Merge first alternative into main
            self.merge_branches(
                branch_ids[1],  # First alternative
                self.plan_tree.main_branch_id
            )
            
            # Merge second alternative into main
            self.merge_branches(
                branch_ids[2],  # Second alternative
                self.plan_tree.main_branch_id
            )
        
        # 9. Generate final conclusion
        self.current_phase = "conclusion_generation"
        
        # In a real implementation, this would synthesize from all the reasoning
        # For this example, we'll create a simple conclusion
        conclusion = f"""
        Final conclusion about: {query}
        
        Based on our hierarchical belief-space planning with introspection:
        
        1. We explored the main hypothesis: {main_hypothesis}
        2. We also considered {len(alternative_hypotheses)} alternative hypotheses
        3. We generated and validated hypothetical evidence
        4. We performed introspective evaluation to improve our reasoning
        5. We merged insights from parallel reasoning paths
        
        The confidence in our main hypothesis is now: {self.belief_space.beliefs[main_hypothesis_id].confidence if main_hypothesis_id else 'unknown'}
        
        [Full detailed conclusion would be generated here in a real implementation]
        """
        
        # Track step
        self.reasoning_steps.append({
            "phase": "conclusion",
            "description": "Generated final conclusion",
            "conclusion": conclusion
        })
        
        # 10. Return results
        return {
            "query": query,
            "conclusion": conclusion,
            "reasoning_steps": self.reasoning_steps,
            "plan_tree_statistics": self.plan_tree.get_tree_statistics(),
            "belief_space_statistics": self.belief_space.get_belief_space_statistics(),
            "introspection_statistics": self.introspection.get_statistics()
        }
    
    async def async_reason_about_query(self, query: str) -> Dict[str, Any]:
        """
        Asynchronous version of the reasoning process.
        
        Allows for parallel processing of multiple components.
        """
        # Initialize
        self.current_phase = "initialization"
        self.reasoning_steps.append({
            "phase": "initialization",
            "description": f"Started reasoning about query: {query}",
            "query": query
        })
        
        # In a real implementation, we would do much of this in parallel
        # For this example, we'll just call the synchronous version
        return self.reason_about_query(query)
    
    # =============================================
    # Utilities and analysis
    # =============================================
    
    def get_reasoning_trace(self) -> List[Dict[str, Any]]:
        """Get the full trace of reasoning steps."""
        return self.reasoning_steps
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about the reasoning process."""
        return {
            "total_reasoning_steps": len(self.reasoning_steps),
            "hypothetical_evidence_count": len(self.hypothetical_evidence),
            "validated_evidence_count": sum(
                1 for e in self.hypothetical_evidence.values() 
                if e.validation_status == "validated"
            ),
            "refuted_evidence_count": sum(
                1 for e in self.hypothetical_evidence.values() 
                if e.validation_status == "refuted"
            ),
            "branch_count": len(self.plan_tree.branches),
            "plan_tree_statistics": self.plan_tree.get_tree_statistics(),
            "belief_space_statistics": self.belief_space.get_belief_space_statistics(),
            "introspection_statistics": self.introspection.get_statistics(),
            "current_phase": self.current_phase
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export the reasoner's state to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "hypothetical_evidence": {id: e.model_dump() for id, e in self.hypothetical_evidence.items()},
            "primary_strategy": self.primary_strategy,
            "alternate_strategies": self.alternate_strategies,
            "max_hypothetical_evidence": self.max_hypothetical_evidence,
            "introspection_frequency": self.introspection_frequency,
            "metadata": self.metadata,
            "reasoning_steps": self.reasoning_steps,
            "current_phase": self.current_phase,
            "statistics": self.get_statistics(),
            "plan_tree": self.plan_tree.export_to_dict(),
            "belief_space": self.belief_space.export_to_dict(),
            "introspection": self.introspection.export_to_dict()
        }