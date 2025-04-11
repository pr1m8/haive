# src/haive/agents/hbspi/belief_space.py

from __future__ import annotations
import uuid
import math
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
class BeliefType(str, Enum):
    """Types of beliefs in the belief space."""
    FACT = "fact"               # Known fact or assumption
    HYPOTHESIS = "hypothesis"   # Speculative hypothesis
    INFERENCE = "inference"     # Inference from other beliefs
    CONSTRAINT = "constraint"   # Logical constraint
    UNCERTAINTY = "uncertainty" # Explicitly modeled uncertainty

class ConflictResolution(str, Enum):
    """Strategies for resolving conflicts between beliefs."""
    KEEP_HIGHER_CONFIDENCE = "keep_higher_confidence"
    KEEP_NEWER = "keep_newer"
    MERGE = "merge"
    KEEP_BOTH = "keep_both"

class EvidenceType(str, Enum):
    """Types of evidence for beliefs."""
    DIRECT = "direct"           # Direct evidence
    INDIRECT = "indirect"       # Indirect or circumstantial evidence
    COUNTERFACTUAL = "counterfactual" # Hypothetical counterfactual
    LOGICAL = "logical"         # Logical deduction

class Belief(BaseModel):
    """Representation of a belief in the belief space."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    content: str = Field(..., description="Statement of the belief")
    type: BeliefType = Field(...)
    confidence: float = Field(default=0.5, description="Confidence score (0-1)")
    
    # Relational fields
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    related_belief_ids: List[str] = Field(default_factory=list)
    
    # Metadata
    creation_time: str = Field(default_factory=lambda: str(uuid.uuid4()))
    last_updated: str = Field(default_factory=lambda: str(uuid.uuid4()))
    update_count: int = Field(default=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Evidence(BaseModel):
    """Evidence that supports or contradicts beliefs."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    content: str = Field(..., description="Description of the evidence")
    type: EvidenceType = Field(...)
    strength: float = Field(default=0.5, description="Strength of evidence (0-1)")
    
    # For hypothetical evidence
    is_hypothetical: bool = Field(default=False)
    validation_status: Optional[str] = Field(default=None)
    
    # Relation to beliefs
    supporting_belief_ids: List[str] = Field(default_factory=list)
    contradicting_belief_ids: List[str] = Field(default_factory=list)
    
    # Metadata
    creation_time: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: Optional[str] = Field(default=None, description="Source of evidence")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BeliefRelation(BaseModel):
    """Relation between beliefs."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    belief_id_1: str
    belief_id_2: str
    relation_type: str = Field(..., description="e.g., 'supports', 'contradicts', 'implies'")
    strength: float = Field(default=0.5, description="Strength of relation (0-1)")
    description: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BeliefSpaceManager(BaseModel):
    """
    Manager for a probabilistic belief space.
    
    Tracks beliefs, evidence, and their relationships in a structured space that
    supports uncertainty and belief updating based on evidence.
    """
    beliefs: Dict[str, Belief] = Field(default_factory=dict)
    evidence: Dict[str, Evidence] = Field(default_factory=dict)
    relations: Dict[str, BeliefRelation] = Field(default_factory=dict)
    
    # Configuration
    name: str = Field(..., description="Name of this belief space")
    description: str = Field(..., description="Description of the belief space's purpose")
    conflict_resolution: ConflictResolution = Field(default=ConflictResolution.MERGE)
    confidence_threshold: float = Field(default=0.7, description="Threshold for accepting beliefs")
    entropy_threshold: float = Field(default=0.3, description="Threshold for acceptable belief entropy")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # =============================================
    # Creation and management
    # =============================================
    
    @classmethod
    def create(cls, name: str, description: str, **kwargs) -> BeliefSpaceManager:
        """Create a new belief space manager."""
        return cls(
            name=name,
            description=description,
            **kwargs
        )
    
    # =============================================
    # Belief methods
    # =============================================
    
    def add_belief(self, content: str, type: BeliefType, confidence: float = 0.5, 
                  **kwargs) -> Belief:
        """Add a new belief to the space."""
        belief = Belief(
            content=content,
            type=type,
            confidence=confidence,
            **kwargs
        )
        
        # Check for conflicts
        conflicts = self.find_conflicting_beliefs(belief)
        if conflicts:
            self._resolve_conflicts(belief, conflicts)
        
        # Add to belief space
        self.beliefs[belief.id] = belief
        return belief
    
    def update_belief_confidence(self, belief_id: str, 
                                new_confidence: Optional[float] = None,
                                adjustment: Optional[float] = None) -> Belief:
        """
        Update a belief's confidence based on new information.
        
        Args:
            belief_id: ID of the belief to update
            new_confidence: New absolute confidence value (0-1)
            adjustment: Relative adjustment to confidence (-1 to 1)
        
        Returns:
            Updated belief
        """
        if belief_id not in self.beliefs:
            raise ValueError(f"Belief {belief_id} not found")
            
        belief = self.beliefs[belief_id]
        
        # Apply update
        if new_confidence is not None:
            belief.confidence = max(0.0, min(1.0, new_confidence))
        elif adjustment is not None:
            belief.confidence = max(0.0, min(1.0, belief.confidence + adjustment))
        
        # Update metadata
        belief.update_count += 1
        belief.last_updated = str(uuid.uuid4())
        
        # Store updated belief
        self.beliefs[belief_id] = belief
        return belief
    
    def find_conflicting_beliefs(self, belief: Belief) -> List[Belief]:
        """Find existing beliefs that potentially conflict with this one."""
        # This would typically use NLP/semantic analysis
        # For this example, we'll use a simple string comparison
        conflicting_beliefs = []
        
        for existing_belief in self.beliefs.values():
            # Skip if same belief
            if existing_belief.id == belief.id:
                continue
                
            # Check for semantic similarity
            # This is a placeholder for more sophisticated conflict detection
            if self._beliefs_conflict(existing_belief, belief):
                conflicting_beliefs.append(existing_belief)
                
        return conflicting_beliefs
    
    def _beliefs_conflict(self, belief1: Belief, belief2: Belief) -> bool:
        """Determine if two beliefs conflict."""
        # This would typically use NLP/semantic analysis
        # For this example, we'll just use a simple check for opposite statements
        # e.g., "X is true" conflicts with "X is not true"
        
        # Placeholder implementation - in a real system, this would be more sophisticated
        negation_prefixes = ["not ", "no ", "never ", "doesn't ", "don't ", "isn't ", "aren't ", "cannot "]
        
        # Check if one belief is the negation of the other
        for prefix in negation_prefixes:
            if belief1.content.lower().startswith(prefix):
                stripped = belief1.content.lower()[len(prefix):]
                if stripped == belief2.content.lower():
                    return True
                    
            if belief2.content.lower().startswith(prefix):
                stripped = belief2.content.lower()[len(prefix):]
                if stripped == belief1.content.lower():
                    return True
        
        return False
    
    def _resolve_conflicts(self, new_belief: Belief, conflicts: List[Belief]) -> None:
        """Resolve conflicts between beliefs based on strategy."""
        for conflict in conflicts:
            # Apply resolution strategy
            if self.conflict_resolution == ConflictResolution.KEEP_HIGHER_CONFIDENCE:
                if new_belief.confidence > conflict.confidence:
                    # Remove conflicting belief
                    if conflict.id in self.beliefs:
                        del self.beliefs[conflict.id]
                        
                        # We'd also need to update any relations or evidence
                        self._cleanup_relations(conflict.id)
                else:
                    # Don't add the new belief
                    return
                    
            elif self.conflict_resolution == ConflictResolution.KEEP_NEWER:
                # Remove the older belief
                if conflict.id in self.beliefs:
                    del self.beliefs[conflict.id]
                    self._cleanup_relations(conflict.id)
                    
            elif self.conflict_resolution == ConflictResolution.MERGE:
                # Merge the beliefs by averaging confidence and joining content
                merged_content = f"{conflict.content} (MERGED WITH: {new_belief.content})"
                merged_confidence = (conflict.confidence + new_belief.confidence) / 2
                
                # Update existing belief
                conflict.content = merged_content
                conflict.confidence = merged_confidence
                conflict.update_count += 1
                conflict.last_updated = str(uuid.uuid4())
                conflict.metadata["merged_with"] = new_belief.id
                
                self.beliefs[conflict.id] = conflict
                
                # Don't add the new belief separately
                return
                
            elif self.conflict_resolution == ConflictResolution.KEEP_BOTH:
                # Keep both, but add a relation noting the conflict
                self.add_relation(
                    belief_id_1=conflict.id,
                    belief_id_2=new_belief.id,
                    relation_type="contradicts",
                    strength=1.0,
                    description="Contradicting beliefs"
                )
    
    def _cleanup_relations(self, belief_id: str) -> None:
        """Clean up relations when a belief is removed."""
        # Remove relations involving this belief
        relations_to_remove = []
        
        for relation_id, relation in self.relations.items():
            if relation.belief_id_1 == belief_id or relation.belief_id_2 == belief_id:
                relations_to_remove.append(relation_id)
                
        for relation_id in relations_to_remove:
            if relation_id in self.relations:
                del self.relations[relation_id]
        
        # Update evidence that references this belief
        for evidence_id, evidence in self.evidence.items():
            if belief_id in evidence.supporting_belief_ids:
                evidence.supporting_belief_ids.remove(belief_id)
                
            if belief_id in evidence.contradicting_belief_ids:
                evidence.contradicting_belief_ids.remove(belief_id)
                
            self.evidence[evidence_id] = evidence
    
    # =============================================
    # Evidence methods
    # =============================================
    
    def add_evidence(self, content: str, type: EvidenceType, strength: float = 0.5,
                    supporting_belief_ids: Optional[List[str]] = None,
                    contradicting_belief_ids: Optional[List[str]] = None,
                    **kwargs) -> Evidence:
        """Add evidence to the belief space."""
        evidence = Evidence(
            content=content,
            type=type,
            strength=strength,
            supporting_belief_ids=supporting_belief_ids or [],
            contradicting_belief_ids=contradicting_belief_ids or [],
            **kwargs
        )
        
        self.evidence[evidence.id] = evidence
        
        # Update the related beliefs
        for belief_id in evidence.supporting_belief_ids:
            if belief_id in self.beliefs:
                belief = self.beliefs[belief_id]
                belief.supporting_evidence_ids.append(evidence.id)
                self.beliefs[belief_id] = belief
                
                # Update belief confidence
                self.update_belief_based_on_evidence(belief_id)
        
        for belief_id in evidence.contradicting_belief_ids:
            if belief_id in self.beliefs:
                belief = self.beliefs[belief_id]
                belief.contradicting_evidence_ids.append(evidence.id)
                self.beliefs[belief_id] = belief
                
                # Update belief confidence
                self.update_belief_based_on_evidence(belief_id)
        
        return evidence
    
    def add_hypothetical_evidence(self, content: str, type: EvidenceType, strength: float = 0.5,
                                 related_belief_ids: Optional[List[str]] = None,
                                 **kwargs) -> Evidence:
        """Add hypothetical evidence that could potentially be validated."""
        return self.add_evidence(
            content=content,
            type=type,
            strength=strength,
            supporting_belief_ids=[],
            contradicting_belief_ids=[],
            is_hypothetical=True,
            validation_status="pending",
            metadata={"related_belief_ids": related_belief_ids or []},
            **kwargs
        )
    
    def validate_hypothetical_evidence(self, evidence_id: str, 
                                      is_valid: bool, 
                                      explanation: Optional[str] = None) -> Evidence:
        """Validate or refute hypothetical evidence."""
        if evidence_id not in self.evidence:
            raise ValueError(f"Evidence {evidence_id} not found")
            
        evidence = self.evidence[evidence_id]
        if not evidence.is_hypothetical:
            raise ValueError(f"Evidence {evidence_id} is not hypothetical")
            
        # Update validation status
        evidence.validation_status = "validated" if is_valid else "refuted"
        if explanation:
            evidence.metadata["validation_explanation"] = explanation
        
        # If validated, add connections to beliefs
        if is_valid and "related_belief_ids" in evidence.metadata:
            for belief_id in evidence.metadata["related_belief_ids"]:
                if belief_id in self.beliefs:
                    # Determine if supporting or contradicting based on belief type
                    # This is a simplified approach - in a real system, you'd use NLP
                    belief = self.beliefs[belief_id]
                    
                    if belief.type == BeliefType.HYPOTHESIS:
                        # Support hypotheses
                        evidence.supporting_belief_ids.append(belief_id)
                        belief.supporting_evidence_ids.append(evidence.id)
                        self.beliefs[belief_id] = belief
                    elif belief.type == BeliefType.UNCERTAINTY:
                        # Reduce uncertainty
                        evidence.contradicting_belief_ids.append(belief_id)
                        belief.contradicting_evidence_ids.append(evidence.id)
                        self.beliefs[belief_id] = belief
                    else:
                        # For other types, just support
                        evidence.supporting_belief_ids.append(belief_id)
                        belief.supporting_evidence_ids.append(evidence.id)
                        self.beliefs[belief_id] = belief
                    
                    # Update belief confidence
                    self.update_belief_based_on_evidence(belief_id)
        
        self.evidence[evidence_id] = evidence
        return evidence
    
    def update_belief_based_on_evidence(self, belief_id: str) -> Belief:
        """Update a belief's confidence based on supporting/contradicting evidence."""
        if belief_id not in self.beliefs:
            raise ValueError(f"Belief {belief_id} not found")
            
        belief = self.beliefs[belief_id]
        
        # Get supporting and contradicting evidence
        supporting_evidence = [
            self.evidence[e_id] for e_id in belief.supporting_evidence_ids 
            if e_id in self.evidence
        ]
        
        contradicting_evidence = [
            self.evidence[e_id] for e_id in belief.contradicting_evidence_ids 
            if e_id in self.evidence
        ]
        
        # Calculate evidence adjustments
        if not supporting_evidence and not contradicting_evidence:
            return belief  # No change if no evidence
            
        # Bayesian update approach - simplified version
        # Start with prior confidence
        prior = belief.confidence
        
        # Calculate likelihood ratio
        supporting_strength = sum(e.strength for e in supporting_evidence)
        contradicting_strength = sum(e.strength for e in contradicting_evidence)
        
        # Normalize to ensure we don't exceed bounds
        total_strength = supporting_strength + contradicting_strength
        if total_strength > 0:
            supporting_ratio = supporting_strength / total_strength
            
            # Apply Bayesian update (simplified)
            posterior = (prior * supporting_ratio) / (prior * supporting_ratio + (1-prior) * (1-supporting_ratio))
            
            # Ensure bounds
            posterior = max(0.01, min(0.99, posterior))
            
            # Update confidence
            belief.confidence = posterior
            belief.update_count += 1
            belief.last_updated = str(uuid.uuid4())
            
            self.beliefs[belief_id] = belief
            
        return belief
    
    # =============================================
    # Relation methods
    # =============================================
    
    def add_relation(self, belief_id_1: str, belief_id_2: str, relation_type: str,
                    strength: float = 0.5, description: Optional[str] = None, 
                    **kwargs) -> BeliefRelation:
        """Add a relation between beliefs."""
        # Validate beliefs exist
        if belief_id_1 not in self.beliefs:
            raise ValueError(f"Belief {belief_id_1} not found")
        if belief_id_2 not in self.beliefs:
            raise ValueError(f"Belief {belief_id_2} not found")
            
        # Create relation
        relation = BeliefRelation(
            belief_id_1=belief_id_1,
            belief_id_2=belief_id_2,
            relation_type=relation_type,
            strength=strength,
            description=description,
            metadata=kwargs.get("metadata", {})
        )
        
        # Add to relations
        self.relations[relation.id] = relation
        
        # Update related_belief_ids in both beliefs
        belief1 = self.beliefs[belief_id_1]
        belief2 = self.beliefs[belief_id_2]
        
        if belief_id_2 not in belief1.related_belief_ids:
            belief1.related_belief_ids.append(belief_id_2)
            self.beliefs[belief_id_1] = belief1
            
        if belief_id_1 not in belief2.related_belief_ids:
            belief2.related_belief_ids.append(belief_id_1)
            self.beliefs[belief_id_2] = belief2
            
        return relation
    
    def get_relations_for_belief(self, belief_id: str) -> List[BeliefRelation]:
        """Get all relations for a belief."""
        if belief_id not in self.beliefs:
            raise ValueError(f"Belief {belief_id} not found")
            
        return [
            relation for relation in self.relations.values()
            if relation.belief_id_1 == belief_id or relation.belief_id_2 == belief_id
        ]
    
    def get_related_beliefs(self, belief_id: str, relation_type: Optional[str] = None) -> List[Belief]:
        """Get beliefs related to the given belief."""
        if belief_id not in self.beliefs:
            raise ValueError(f"Belief {belief_id} not found")
            
        related_belief_ids = set()
        
        for relation in self.relations.values():
            if relation_type and relation.relation_type != relation_type:
                continue
                
            if relation.belief_id_1 == belief_id:
                related_belief_ids.add(relation.belief_id_2)
            elif relation.belief_id_2 == belief_id:
                related_belief_ids.add(relation.belief_id_1)
                
        return [
            self.beliefs[bid] for bid in related_belief_ids 
            if bid in self.beliefs
        ]
    
    # =============================================
    # Belief space analysis
    # =============================================
    
    def calculate_belief_entropy(self) -> float:
        """
        Calculate the entropy of the belief space.
        
        Higher entropy indicates more uncertainty in the belief space.
        """
        if not self.beliefs:
            return 0.0
            
        # Calculate entropy based on belief confidences
        entropy = 0.0
        for belief in self.beliefs.values():
            # We use confidence and uncertainty (1-confidence)
            p = belief.confidence
            q = 1 - p
            
            # Binary entropy of each belief
            if p > 0 and q > 0:
                belief_entropy = -p * math.log2(p) - q * math.log2(q)
                entropy += belief_entropy
                
        # Normalize
        return entropy / len(self.beliefs)
    
    def get_most_uncertain_beliefs(self, limit: int = 5) -> List[Belief]:
        """Get the most uncertain beliefs (closest to 0.5 confidence)."""
        if not self.beliefs:
            return []
            
        sorted_beliefs = sorted(
            self.beliefs.values(),
            key=lambda b: abs(b.confidence - 0.5)
        )
        
        return sorted_beliefs[:limit]
    
    def get_most_confident_beliefs(self, limit: int = 5) -> List[Belief]:
        """Get the beliefs with highest confidence."""
        if not self.beliefs:
            return []
            
        sorted_beliefs = sorted(
            self.beliefs.values(),
            key=lambda b: b.confidence,
            reverse=True
        )
        
        return sorted_beliefs[:limit]
    
    def get_belief_space_statistics(self) -> Dict[str, Any]:
        """Get statistics about the belief space."""
        belief_types = {belief_type: 0 for belief_type in BeliefType}
        for belief in self.beliefs.values():
            belief_types[belief.type] += 1
            
        evidence_types = {evidence_type: 0 for evidence_type in EvidenceType}
        for evidence in self.evidence.values():
            evidence_types[evidence.type] += 1
            
        relation_types = {}
        for relation in self.relations.values():
            relation_types[relation.relation_type] = relation_types.get(relation.relation_type, 0) + 1
            
        return {
            "total_beliefs": len(self.beliefs),
            "total_evidence": len(self.evidence),
            "total_relations": len(self.relations),
            "belief_types": belief_types,
            "evidence_types": evidence_types,
            "relation_types": relation_types,
            "entropy": self.calculate_belief_entropy(),
            "average_confidence": sum(b.confidence for b in self.beliefs.values()) / len(self.beliefs) if self.beliefs else 0,
            "hypothetical_evidence_count": sum(1 for e in self.evidence.values() if e.is_hypothetical),
            "validated_evidence_count": sum(1 for e in self.evidence.values() if e.is_hypothetical and e.validation_status == "validated"),
            "refuted_evidence_count": sum(1 for e in self.evidence.values() if e.is_hypothetical and e.validation_status == "refuted")
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export the belief space to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "beliefs": {id: belief.model_dump() for id, belief in self.beliefs.items()},
            "evidence": {id: evidence.model_dump() for id, evidence in self.evidence.items()},
            "relations": {id: relation.model_dump() for id, relation in self.relations.items()},
            "conflict_resolution": self.conflict_resolution,
            "confidence_threshold": self.confidence_threshold,
            "entropy_threshold": self.entropy_threshold,
            "metadata": self.metadata,
            "statistics": self.get_belief_space_statistics()
        }