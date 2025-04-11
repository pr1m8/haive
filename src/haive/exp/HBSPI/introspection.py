# src/haive/agents/hbspi/introspection.py

from __future__ import annotations
import uuid
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
class CognitiveError(str, Enum):
    """Types of cognitive errors that can be detected by introspection."""
    CONFIRMATION_BIAS = "confirmation_bias"
    ANCHORING_BIAS = "anchoring_bias"
    AVAILABILITY_BIAS = "availability_bias"
    REPRESENTATIVENESS_BIAS = "representativeness_bias"
    OVERCONFIDENCE = "overconfidence"
    HINDSIGHT_BIAS = "hindsight_bias"
    ILLUSORY_CORRELATION = "illusory_correlation"
    SUNK_COST_FALLACY = "sunk_cost_fallacy"
    FRAMING_EFFECT = "framing_effect"
    AMBIGUITY_EFFECT = "ambiguity_effect"
    CIRCULAR_REASONING = "circular_reasoning"
    ARGUMENT_FROM_IGNORANCE = "argument_from_ignorance"
    FALSE_DICHOTOMY = "false_dichotomy"
    HASTY_GENERALIZATION = "hasty_generalization"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    CONJUNCTION_FALLACY = "conjunction_fallacy"
    BANDWAGON_FALLACY = "bandwagon_fallacy"
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    POST_HOC = "post_hoc"
    BURDEN_OF_PROOF_SHIFT = "burden_of_proof_shift"
    TEXAS_SHARPSHOOTER = "texas_sharpshooter"
    MIDDLE_GROUND_FALLACY = "middle_ground_fallacy"
    INCONSISTENCY = "inconsistency"
    IGNORING_COMPETING_HYPOTHESES = "ignoring_competing_hypotheses"
    INACCURATE_MENTAL_MODEL = "inaccurate_mental_model"

class IntrospectionTarget(str, Enum):
    """Types of targets for introspection."""
    BELIEF = "belief"
    REASONING_STEP = "reasoning_step"
    EVIDENCE = "evidence"
    INFERENCE_RULE = "inference_rule"
    BRANCH = "branch"
    PLAN = "plan"
    ENTIRE_PROCESS = "entire_process"

class ReasoningTechnique(str, Enum):
    """Reasoning techniques that can be suggested."""
    # Deductive reasoning
    MODUS_PONENS = "modus_ponens"
    MODUS_TOLLENS = "modus_tollens"
    
    # Inductive reasoning
    GENERALIZATION = "generalization"
    ANALOGICAL_REASONING = "analogical_reasoning"
    
    # Abductive reasoning
    INFERENCE_TO_BEST_EXPLANATION = "inference_to_best_explanation"
    HYPOTHESIS_TESTING = "hypothesis_testing"
    
    # Causal reasoning
    COUNTERFACTUAL_REASONING = "counterfactual_reasoning"
    CAUSAL_ANALYSIS = "causal_analysis"
    
    # Probabilistic reasoning
    BAYESIAN_REASONING = "bayesian_reasoning"
    MONTE_CARLO_SIMULATION = "monte_carlo_simulation"
    
    # Formal systems
    MODAL_LOGIC = "modal_logic"
    TEMPORAL_LOGIC = "temporal_logic"
    
    # Meta-reasoning
    METACOGNITIVE_SCAFFOLDING = "metacognitive_scaffolding"
    REFLECTION_LOOPS = "reflection_loops"
    
    # Other techniques
    CONSTRAINT_SATISFACTION = "constraint_satisfaction"
    COMMONSENSE_REASONING = "commonsense_reasoning"
    DOUBLE_LOOP_LEARNING = "double_loop_learning"

class IntrospectionInsight(BaseModel):
    """An insight gained from introspection."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    target_id: str = Field(..., description="ID of the target being evaluated")
    target_type: IntrospectionTarget = Field(...)
    
    # Analysis
    cognitive_errors: List[CognitiveError] = Field(default_factory=list)
    critique: str = Field(..., description="Critique of the reasoning")
    
    # Recommendations
    improvements: List[str] = Field(default_factory=list)
    suggested_techniques: List[ReasoningTechnique] = Field(default_factory=list)
    confidence_adjustment: float = Field(default=0.0, description="Suggested adjustment to confidence (-1 to 1)")
    
    # Metadata
    severity: float = Field(default=0.5, description="Severity of issues (0-1)")
    creation_time: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = Field(default_factory=dict)