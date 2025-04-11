# src/haive/agents/hbspi/parallel_plan_tree.py

from __future__ import annotations
import uuid
from typing import Dict, List, Any, Optional, Union, Set, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
class PlanNodeType(str, Enum):
    """Types of nodes in the planning tree."""
    ROOT = "root"                # Top-level node
    TASK = "task"                # Task decomposition node
    REASONING = "reasoning"      # Reasoning step node
    EVIDENCE = "evidence"        # Evidence node
    HYPOTHESIS = "hypothesis"    # Hypothesis node
    DECISION = "decision"        # Decision point node
    ACTION = "action"            # Action node

class EvidenceStatus(str, Enum):
    """Status of hypothetical evidence."""
    PENDING = "pending"          # Not yet validated
    VALIDATED = "validated"      # Confirmed as valid
    REFUTED = "refuted"          # Confirmed as invalid
    PARTIALLY_VALIDATED = "partially_validated"  # Partially confirmed
    UNOBTAINABLE = "unobtainable"  # Cannot be obtained

class PlanTreeNode(BaseModel):
    """Node in the parallel plan tree."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    type: PlanNodeType = Field(...)
    content: str = Field(..., description="Content/description of this node")
    
    # Tree structure
    parent_id: Optional[str] = Field(default=None)
    children_ids: List[str] = Field(default_factory=list)
    
    # Node metadata
    confidence: float = Field(default=0.5, description="Confidence in this node (0-1)")
    depth: int = Field(default=0, description="Depth in the tree")
    status: str = Field(default="pending", description="pending, in_progress, completed, or failed")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Parallel planning fields
    branch_id: Optional[str] = Field(default=None, description="ID of the branch this node belongs to")
    hypothesis_id: Optional[str] = Field(default=None, description="ID of associated hypothesis")
    
    # For hypothetical evidence nodes
    evidence_status: Optional[EvidenceStatus] = Field(default=None)
    validation_explanation: Optional[str] = Field(default=None)

class Branch(BaseModel):
    """A branch in the parallel planning tree representing an alternative reasoning path."""
    id: str = Field(default_factory=lambda: str(uuid4().hex[:8]))
    name: str = Field(..., description="Name of this branch")
    description: str = Field(..., description="Description of what this branch explores")
    root_node_id: str = Field(..., description="ID of the root node for this branch")
    status: str = Field(default="active", description="active, merged, or abandoned")
    confidence: float = Field(default=0.5, description="Confidence in this branch (0-1)")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Branch relationship fields
    parent_branch_id: Optional[str] = Field(default=None)
    child_branch_ids: List[str] = Field(default_factory=list)
    
    # Branch-specific metadata
    created_at: str = Field(default_factory=lambda: str(uuid.uuid4()))
    last_updated: str = Field(default_factory=lambda: str(uuid.uuid4()))
    update_count: int = Field(default=0)

class ParallelPlanTree(BaseModel):
    """
    A tree structure that supports parallel exploration of multiple reasoning paths.
    
    This structure allows:
    - Hierarchical decomposition of planning
    - Parallel exploration of alternative hypotheses
    - Tracking of hypothetical evidence and its validation status
    - Merging of insights from different branches
    """
    nodes: Dict[str, PlanTreeNode] = Field(default_factory=dict)
    branches: Dict[str, Branch] = Field(default_factory=dict)
    main_branch_id: str = Field(..., description="ID of the main branch")
    
    # Tree metadata
    name: str = Field(..., description="Name of this plan tree")
    description: str = Field(..., description="Description of the planning task")
    max_branch_count: int = Field(default=5, description="Maximum number of parallel branches")
    max_depth: int = Field(default=10, description="Maximum depth of the tree")
    
    # Control parameters
    confidence_threshold: float = Field(default=0.7, description="Confidence threshold for acceptance")
    branch_similarity_threshold: float = Field(default=0.8, description="Threshold for branch similarity")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # =============================================
    # Creation methods
    # =============================================
    
    @classmethod
    def create(cls, name: str, description: str, **kwargs) -> ParallelPlanTree:
        """Create a new parallel plan tree with an initial main branch."""
        # Create the main branch
        main_branch_id = str(uuid4().hex[:8])
        main_branch = Branch(
            id=main_branch_id,
            name="Main Branch",
            description="Primary reasoning path",
            root_node_id="",  # Will be set after root node creation
            status="active"
        )
        
        # Create the tree
        tree = cls(
            nodes={},
            branches={main_branch_id: main_branch},
            main_branch_id=main_branch_id,
            name=name,
            description=description,
            **kwargs
        )
        
        # Create root node
        root_node = tree.add_node(
            type=PlanNodeType.ROOT,
            content=f"Root node for: {description}",
            branch_id=main_branch_id
        )
        
        # Update the branch with root node reference
        main_branch.root_node_id = root_node.id
        tree.branches[main_branch_id] = main_branch
        
        return tree
    
    # =============================================
    # Node management methods
    # =============================================
    
    def add_node(self, type: PlanNodeType, content: str, 
                 parent_id: Optional[str] = None, branch_id: Optional[str] = None,
                 **kwargs) -> PlanTreeNode:
        """Add a node to the tree."""
        # Determine branch
        if branch_id is None and parent_id is not None:
            # Inherit branch from parent
            parent = self.nodes.get(parent_id)
            if parent:
                branch_id = parent.branch_id
        
        if branch_id is None:
            # Default to main branch
            branch_id = self.main_branch_id
        
        # Determine depth
        depth = 0
        if parent_id is not None:
            parent = self.nodes.get(parent_id)
            if parent:
                depth = parent.depth + 1
        
        # Create the node
        node = PlanTreeNode(
            type=type,
            content=content,
            parent_id=parent_id,
            branch_id=branch_id,
            depth=depth,
            **kwargs
        )
        
        # Add to tree
        self.nodes[node.id] = node
        
        # Update parent if applicable
        if parent_id is not None and parent_id in self.nodes:
            parent = self.nodes[parent_id]
            parent.children_ids.append(node.id)
            self.nodes[parent_id] = parent
        
        return node
    
    def get_children(self, node_id: str) -> List[PlanTreeNode]:
        """Get all children of a node."""
        if node_id not in self.nodes:
            return []
            
        node = self.nodes[node_id]
        return [self.nodes[child_id] for child_id in node.children_ids if child_id in self.nodes]
    
    def get_path_to_root(self, node_id: str) -> List[PlanTreeNode]:
        """Get the path from a node to the root."""
        path = []
        current_id = node_id
        
        while current_id is not None and current_id in self.nodes:
            node = self.nodes[current_id]
            path.append(node)
            current_id = node.parent_id
            
            # Safety check for cycles
            if len(path) > self.max_depth:
                break
                
        return path
    
    def find_nodes_by_type(self, node_type: PlanNodeType, branch_id: Optional[str] = None) -> List[PlanTreeNode]:
        """Find all nodes of a specific type, optionally filtered by branch."""
        matching_nodes = []
        
        for node in self.nodes.values():
            if node.type == node_type:
                if branch_id is None or node.branch_id == branch_id:
                    matching_nodes.append(node)
                    
        return matching_nodes
    
    def find_nodes_by_content(self, content_substring: str, branch_id: Optional[str] = None) -> List[PlanTreeNode]:
        """Find all nodes with content containing the given substring."""
        matching_nodes = []
        
        for node in self.nodes.values():
            if content_substring.lower() in node.content.lower():
                if branch_id is None or node.branch_id == branch_id:
                    matching_nodes.append(node)
                    
        return matching_nodes
    
    # =============================================
    # Branch management methods
    # =============================================
    
    def create_branch(self, name: str, description: str, 
                     parent_branch_id: Optional[str] = None,
                     hypothesis_id: Optional[str] = None) -> Branch:
        """Create a new branch for parallel exploration."""
        # Check if we've reached the maximum branch count
        if len(self.branches) >= self.max_branch_count:
            raise ValueError(f"Maximum branch count ({self.max_branch_count}) reached")
        
        # Create the branch
        branch_id = str(uuid4().hex[:8])
        branch = Branch(
            id=branch_id,
            name=name,
            description=description,
            root_node_id="",  # Will be set after root node creation
            parent_branch_id=parent_branch_id,
            status="active"
        )
        
        # Add to tree
        self.branches[branch_id] = branch
        
        # Update parent branch if applicable
        if parent_branch_id is not None and parent_branch_id in self.branches:
            parent_branch = self.branches[parent_branch_id]
            parent_branch.child_branch_ids.append(branch_id)
            self.branches[parent_branch_id] = parent_branch
        
        # Create root node for this branch
        root_node = self.add_node(
            type=PlanNodeType.ROOT,
            content=f"Root node for branch: {name}",
            branch_id=branch_id,
            hypothesis_id=hypothesis_id
        )
        
        # Update the branch with root node reference
        branch.root_node_id = root_node.id
        self.branches[branch_id] = branch
        
        return branch
    
    def get_branch_nodes(self, branch_id: str) -> List[PlanTreeNode]:
        """Get all nodes in a branch."""
        return [node for node in self.nodes.values() if node.branch_id == branch_id]
    
    def abandon_branch(self, branch_id: str, reason: str) -> None:
        """Mark a branch as abandoned."""
        if branch_id not in self.branches:
            raise ValueError(f"Branch {branch_id} not found")
            
        branch = self.branches[branch_id]
        branch.status = "abandoned"
        branch.metadata["abandonment_reason"] = reason
        self.branches[branch_id] = branch
    
    def merge_branches(self, source_branch_id: str, target_branch_id: str, 
                      merge_strategy: str = "selective") -> None:
        """
        Merge insights from one branch into another.
        
        Strategies:
        - selective: Merge only high-confidence nodes
        - complete: Merge all nodes
        - evidence_only: Merge only evidence nodes
        """
        if source_branch_id not in self.branches or target_branch_id not in self.branches:
            raise ValueError("Source or target branch not found")
            
        source_branch = self.branches[source_branch_id]
        target_branch = self.branches[target_branch_id]
        
        # Get nodes from source branch
        source_nodes = self.get_branch_nodes(source_branch_id)
        
        # Apply merge strategy
        nodes_to_merge = []
        
        if merge_strategy == "complete":
            # Merge all nodes
            nodes_to_merge = source_nodes
        elif merge_strategy == "selective":
            # Merge only high-confidence nodes
            nodes_to_merge = [node for node in source_nodes 
                             if node.confidence >= self.confidence_threshold]
        elif merge_strategy == "evidence_only":
            # Merge only evidence nodes
            nodes_to_merge = [node for node in source_nodes 
                             if node.type == PlanNodeType.EVIDENCE]
        else:
            raise ValueError(f"Unknown merge strategy: {merge_strategy}")
        
        # Create merged nodes in target branch
        target_root_id = target_branch.root_node_id
        
        for source_node in nodes_to_merge:
            # Skip the root node
            if source_node.id == source_branch.root_node_id:
                continue
                
            # Create a copy in the target branch
            merged_node = self.add_node(
                type=source_node.type,
                content=f"[Merged from {source_branch.name}] {source_node.content}",
                parent_id=target_root_id,  # Attach to target branch root
                branch_id=target_branch_id,
                confidence=source_node.confidence,
                metadata={
                    **source_node.metadata,
                    "merged_from_node": source_node.id,
                    "merged_from_branch": source_branch_id
                }
            )
            
            # Copy specific fields based on node type
            if source_node.type == PlanNodeType.EVIDENCE:
                merged_node.evidence_status = source_node.evidence_status
                merged_node.validation_explanation = source_node.validation_explanation
                self.nodes[merged_node.id] = merged_node
                
            if source_node.type == PlanNodeType.HYPOTHESIS:
                merged_node.hypothesis_id = source_node.hypothesis_id
                self.nodes[merged_node.id] = merged_node
        
        # Update branch statuses
        source_branch.status = "merged"
        source_branch.metadata["merged_into"] = target_branch_id
        self.branches[source_branch_id] = source_branch
        
        target_branch.metadata["merged_from"] = target_branch.metadata.get("merged_from", []) + [source_branch_id]
        self.branches[target_branch_id] = target_branch
    
    # =============================================
    # Hypothetical evidence methods
    # =============================================
    
    def add_evidence_node(self, content: str, parent_id: str, branch_id: Optional[str] = None, 
                          status: EvidenceStatus = EvidenceStatus.PENDING) -> PlanTreeNode:
        """Add a hypothetical evidence node."""
        return self.add_node(
            type=PlanNodeType.EVIDENCE,
            content=content,
            parent_id=parent_id,
            branch_id=branch_id,
            evidence_status=status
        )
    
    def update_evidence_status(self, node_id: str, status: EvidenceStatus, 
                              explanation: Optional[str] = None) -> None:
        """Update the status of hypothetical evidence."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
            
        node = self.nodes[node_id]
        if node.type != PlanNodeType.EVIDENCE:
            raise ValueError(f"Node {node_id} is not an evidence node")
            
        node.evidence_status = status
        if explanation:
            node.validation_explanation = explanation
        self.nodes[node_id] = node
    
    def get_evidence_nodes(self, status: Optional[EvidenceStatus] = None, 
                          branch_id: Optional[str] = None) -> List[PlanTreeNode]:
        """Get evidence nodes, optionally filtered by status and branch."""
        matching_nodes = []
        
        for node in self.nodes.values():
            if node.type == PlanNodeType.EVIDENCE:
                # Filter by status if specified
                if status is not None and node.evidence_status != status:
                    continue
                    
                # Filter by branch if specified
                if branch_id is not None and node.branch_id != branch_id:
                    continue
                    
                matching_nodes.append(node)
                
        return matching_nodes
    
    # =============================================
    # Analysis and utilities
    # =============================================
    
    def calculate_branch_confidence(self, branch_id: str) -> float:
        """Calculate the overall confidence of a branch based on its nodes."""
        if branch_id not in self.branches:
            raise ValueError(f"Branch {branch_id} not found")
            
        # Get all nodes in this branch
        branch_nodes = self.get_branch_nodes(branch_id)
        
        if not branch_nodes:
            return 0.0
            
        # Calculate weighted average confidence based on node type
        type_weights = {
            PlanNodeType.ROOT: 0.5,
            PlanNodeType.TASK: 0.7,
            PlanNodeType.REASONING: 0.8,
            PlanNodeType.EVIDENCE: 1.0,
            PlanNodeType.HYPOTHESIS: 0.6,
            PlanNodeType.DECISION: 0.9,
            PlanNodeType.ACTION: 0.7
        }
        
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for node in branch_nodes:
            weight = type_weights.get(node.type, 0.5)
            weighted_sum += node.confidence * weight
            weight_sum += weight
        
        if weight_sum == 0:
            return 0.0
            
        return weighted_sum / weight_sum
    
    def update_branch_confidence(self, branch_id: str) -> None:
        """Update the confidence of a branch based on its nodes."""
        if branch_id not in self.branches:
            raise ValueError(f"Branch {branch_id} not found")
            
        confidence = self.calculate_branch_confidence(branch_id)
        
        branch = self.branches[branch_id]
        branch.confidence = confidence
        branch.update_count += 1
        branch.last_updated = str(uuid.uuid4())
        self.branches[branch_id] = branch
    
    def get_tree_statistics(self) -> Dict[str, Any]:
        """Get statistics about the plan tree."""
        # Count nodes by type
        node_types = {node_type: 0 for node_type in PlanNodeType}
        for node in self.nodes.values():
            node_types[node.type] += 1
        
        # Count branches by status
        branch_statuses = {"active": 0, "merged": 0, "abandoned": 0}
        for branch in self.branches.values():
            branch_statuses[branch.status] += 1
        
        # Count evidence by status
        evidence_statuses = {status: 0 for status in EvidenceStatus}
        for node in self.nodes.values():
            if node.type == PlanNodeType.EVIDENCE and node.evidence_status:
                evidence_statuses[node.evidence_status] += 1
        
        # Calculate average confidence
        node_confidences = [node.confidence for node in self.nodes.values()]
        avg_node_confidence = sum(node_confidences) / len(node_confidences) if node_confidences else 0
        
        branch_confidences = [branch.confidence for branch in self.branches.values()]
        avg_branch_confidence = sum(branch_confidences) / len(branch_confidences) if branch_confidences else 0
        
        return {
            "total_nodes": len(self.nodes),
            "total_branches": len(self.branches),
            "nodes_by_type": node_types,
            "branches_by_status": branch_statuses,
            "evidence_by_status": evidence_statuses,
            "max_depth": max((node.depth for node in self.nodes.values()), default=0),
            "avg_node_confidence": avg_node_confidence,
            "avg_branch_confidence": avg_branch_confidence
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export the plan tree to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "main_branch_id": self.main_branch_id,
            "branches": {id: branch.model_dump() for id, branch in self.branches.items()},
            "nodes": {id: node.model_dump() for id, node in self.nodes.items()},
            "max_branch_count": self.max_branch_count,
            "max_depth": self.max_depth,
            "confidence_threshold": self.confidence_threshold,
            "branch_similarity_threshold": self.branch_similarity_threshold,
            "metadata": self.metadata,
            "statistics": self.get_tree_statistics()
        }