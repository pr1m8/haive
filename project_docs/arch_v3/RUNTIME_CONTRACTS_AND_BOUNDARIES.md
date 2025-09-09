# Runtime Contracts and Boundaries Design

**Created**: 2025-09-08
**Purpose**: Practical runtime solutions for contracts and boundaries
**Status**: Design Document
**Key Insight**: Keep runtime flexibility, add explicit contracts

## 🎯 Core Philosophy

**NOT**: Replace runtime with compile-time
**BUT**: Add contracts and boundaries to runtime system

The system NEEDS runtime flexibility for:

- Dynamic tool addition
- State-driven behavior
- Hot-swappable logic
- Adaptive workflows

The system LACKS:

- Explicit contracts
- Access boundaries
- Transformation layers
- State isolation

## 🏗️ Architecture Components

### 1. BoundedState - Controlled Access

````python
from typing import Any, Dict, List, Set, Optional, Protocol
from pydantic import BaseModel, Field
import copy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AccessPermissions(BaseModel):
    """Define what fields a component can access.

    Attributes:
        readable: Fields component can read
        writable: Fields component can write
        append_only: Fields component can append to but not overwrite
        compute_only: Fields component can derive from but not store
    """
    readable: Set[str] = Field(default_factory=set)
    writable: Set[str] = Field(default_factory=set)
    append_only: Set[str] = Field(default_factory=set)
    compute_only: Set[str] = Field(default_factory=set)


class StateView:
    """Filtered view of state with access control.

    This provides a component with controlled access to state,
    enforcing permissions at runtime while maintaining flexibility.
    """

    def __init__(self, state: Dict[str, Any], permissions: AccessPermissions):
        """Initialize state view with permissions.

        Args:
            state: Reference to actual state (not copied)
            permissions: Access permissions for this view
        """
        self._state = state
        self._permissions = permissions
        self._access_log: List[Dict] = []

    def get(self, field: str, default: Any = None) -> Any:
        """Get field value with permission check.

        Args:
            field: Field name to retrieve
            default: Default value if field not found or not accessible

        Returns:
            Field value or default

        Raises:
            PermissionError: If field not readable
        """
        if field not in self._permissions.readable:
            self._log_access_violation("read", field)
            raise PermissionError(f"Cannot read field '{field}'")

        self._log_access("read", field)
        return copy.deepcopy(self._state.get(field, default))

    def set(self, field: str, value: Any) -> None:
        """Set field value with permission check.

        Args:
            field: Field name to set
            value: Value to set

        Raises:
            PermissionError: If field not writable
        """
        if field not in self._permissions.writable:
            self._log_access_violation("write", field)
            raise PermissionError(f"Cannot write field '{field}'")

        self._log_access("write", field)
        self._state[field] = value

    def append(self, field: str, item: Any) -> None:
        """Append to list field with permission check.

        Args:
            field: Field name containing list
            item: Item to append

        Raises:
            PermissionError: If field not appendable
            TypeError: If field is not a list
        """
        if field not in self._permissions.append_only:
            self._log_access_violation("append", field)
            raise PermissionError(f"Cannot append to field '{field}'")

        if field not in self._state:
            self._state[field] = []

        if not isinstance(self._state[field], list):
            raise TypeError(f"Field '{field}' is not a list")

        self._log_access("append", field)
        self._state[field].append(item)

    def compute_from(self, fields: List[str]) -> Dict[str, Any]:
        """Get values for computation without storage permission.

        Args:
            fields: Fields to retrieve for computation

        Returns:
            Dictionary of field values

        Raises:
            PermissionError: If any field not compute_only
        """
        result = {}
        for field in fields:
            if field not in self._permissions.compute_only:
                self._log_access_violation("compute", field)
                raise PermissionError(f"Cannot compute from field '{field}'")

            self._log_access("compute", field)
            result[field] = copy.deepcopy(self._state.get(field))

        return result

    def _log_access(self, operation: str, field: str) -> None:
        """Log successful access."""
        self._access_log.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "field": field,
            "status": "success"
        })

    def _log_access_violation(self, operation: str, field: str) -> None:
        """Log access violation."""
        self._access_log.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "field": field,
            "status": "denied"
        })
        logger.warning(f"Access denied: {operation} on field '{field}'")


class BoundedState:
    """State container with access boundaries.

    This maintains the actual state and provides controlled views
    to different components based on their access permissions.
    """

    def __init__(self, initial_data: Dict[str, Any] = None):
        """Initialize bounded state.

        Args:
            initial_data: Initial state data
        """
        self._data = initial_data or {}
        self._access_rules: Dict[str, AccessPermissions] = {}
        self._version = 0
        self._history: List[Dict] = []

    def register_component(self, name: str, permissions: AccessPermissions) -> None:
        """Register component with access permissions.

        Args:
            name: Component identifier
            permissions: Access permissions for component
        """
        self._access_rules[name] = permissions
        logger.info(f"Registered component '{name}' with permissions")

    def get_view_for(self, component_name: str) -> StateView:
        """Get filtered state view for component.

        Args:
            component_name: Name of component requesting view

        Returns:
            StateView with appropriate permissions

        Raises:
            ValueError: If component not registered
        """
        if component_name not in self._access_rules:
            raise ValueError(f"Component '{component_name}' not registered")

        permissions = self._access_rules[component_name]
        return StateView(self._data, permissions)

    def snapshot(self) -> Dict[str, Any]:
        """Get immutable snapshot of current state.

        Returns:
            Deep copy of current state
        """
        return copy.deepcopy(self._data)

    def checkpoint(self, description: str = "") -> None:
        """Create checkpoint in history.

        Args:
            description: Optional checkpoint description
        """
        self._version += 1
        self._history.append({
            "version": self._version,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "state": copy.deepcopy(self._data)
        })

    def rollback(self, version: int) -> None:
        """Rollback to previous version.

        Args:
            version: Version number to rollback to

        Raises:
            ValueError: If version not found
        """
        for checkpoint in self._history:
            if checkpoint["version"] == version:
                self._data = copy.deepcopy(checkpoint["state"])
                self._version = version
                logger.info(f"Rolled back to version {version}")
                return

        raise ValueError(f"Version {version} not found in history")


### 2. EngineInterface - Explicit Contracts

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel


class FieldContract(BaseModel):
    """Contract for a single field.

    Attributes:
        name: Field identifier
        type: Expected type
        required: Whether field is required
        default: Default value if not required
        description: Field purpose
        validator: Optional validation function
    """
    name: str
    type: Type
    required: bool = True
    default: Any = None
    description: str = ""
    validator: Optional[callable] = None


class EngineContract(BaseModel):
    """Complete contract for an engine.

    Attributes:
        inputs: Input field contracts
        outputs: Output field contracts
        side_effects: Fields modified as side effects
        preconditions: Conditions that must be true before execution
        postconditions: Conditions guaranteed after execution
    """
    inputs: List[FieldContract] = Field(default_factory=list)
    outputs: List[FieldContract] = Field(default_factory=list)
    side_effects: List[str] = Field(default_factory=list)
    preconditions: List[str] = Field(default_factory=list)
    postconditions: List[str] = Field(default_factory=list)


class EngineInterface(ABC):
    """Interface all engines must implement for contracts.

    This ensures every engine explicitly declares its contract,
    making dependencies and effects clear at runtime.
    """

    @abstractmethod
    def get_contract(self) -> EngineContract:
        """Get engine's contract.

        Returns:
            Complete contract specification
        """
        pass

    @abstractmethod
    def validate_input(self, state: Dict[str, Any]) -> bool:
        """Validate state meets input requirements.

        Args:
            state: Current state

        Returns:
            True if state is valid for execution
        """
        pass

    @abstractmethod
    def validate_output(self, result: Any) -> bool:
        """Validate output meets contract.

        Args:
            result: Execution result

        Returns:
            True if output is valid
        """
        pass

    def check_preconditions(self, state: Dict[str, Any]) -> List[str]:
        """Check which preconditions are not met.

        Args:
            state: Current state

        Returns:
            List of unmet preconditions
        """
        contract = self.get_contract()
        unmet = []

        for condition in contract.preconditions:
            # Evaluate condition (simplified - real impl would be more robust)
            if not self._evaluate_condition(condition, state):
                unmet.append(condition)

        return unmet

    def check_postconditions(self, state: Dict[str, Any]) -> List[str]:
        """Check which postconditions are not met.

        Args:
            state: State after execution

        Returns:
            List of unmet postconditions
        """
        contract = self.get_contract()
        unmet = []

        for condition in contract.postconditions:
            if not self._evaluate_condition(condition, state):
                unmet.append(condition)

        return unmet

    def _evaluate_condition(self, condition: str, state: Dict[str, Any]) -> bool:
        """Evaluate a condition against state.

        Args:
            condition: Condition expression
            state: Current state

        Returns:
            True if condition is met
        """
        # Simplified - real implementation would parse and evaluate safely
        try:
            # This is a placeholder - real impl would use safe evaluation
            return True
        except:
            return False


### 3. ContractualNode - Nodes with Contracts

```python
class NodeContract(BaseModel):
    """Contract for a graph node.

    Attributes:
        inputs: Required input fields
        outputs: Produced output fields
        transforms: How fields are transformed
        dependencies: Other nodes this depends on
        guarantees: What this node guarantees
    """
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    transforms: Dict[str, str] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    guarantees: List[str] = Field(default_factory=list)


class ContractualNode:
    """Node that declares and enforces its contract.

    This ensures nodes explicitly declare their behavior,
    making graph composition predictable and debuggable.
    """

    def __init__(self, name: str, contract: NodeContract, execute_fn: callable):
        """Initialize contractual node.

        Args:
            name: Node identifier
            contract: Node's contract
            execute_fn: Function to execute
        """
        self.name = name
        self.contract = contract
        self.execute_fn = execute_fn
        self._execution_count = 0
        self._contract_violations: List[Dict] = []

    def __call__(self, state_view: StateView) -> Dict[str, Any]:
        """Execute node with contract enforcement.

        Args:
            state_view: Bounded view of state

        Returns:
            Execution results

        Raises:
            ContractViolation: If contract is violated
        """
        # Validate inputs
        if not self._validate_inputs(state_view):
            violation = {
                "node": self.name,
                "type": "input",
                "details": f"Missing required inputs: {self.contract.inputs}"
            }
            self._contract_violations.append(violation)
            raise ContractViolation(violation)

        # Execute
        try:
            result = self.execute_fn(state_view)
            self._execution_count += 1
        except Exception as e:
            violation = {
                "node": self.name,
                "type": "execution",
                "details": str(e)
            }
            self._contract_violations.append(violation)
            raise ContractViolation(violation)

        # Validate outputs
        if not self._validate_outputs(result):
            violation = {
                "node": self.name,
                "type": "output",
                "details": f"Missing required outputs: {self.contract.outputs}"
            }
            self._contract_violations.append(violation)
            raise ContractViolation(violation)

        return result

    def _validate_inputs(self, state_view: StateView) -> bool:
        """Validate all required inputs are available.

        Args:
            state_view: State view to validate

        Returns:
            True if all inputs available
        """
        for field in self.contract.inputs:
            try:
                state_view.get(field)
            except PermissionError:
                return False
        return True

    def _validate_outputs(self, result: Dict[str, Any]) -> bool:
        """Validate all required outputs are produced.

        Args:
            result: Execution result

        Returns:
            True if all outputs produced
        """
        if not isinstance(result, dict):
            return False

        for field in self.contract.outputs:
            if field not in result:
                return False

        return True

    def get_contract_summary(self) -> Dict[str, Any]:
        """Get human-readable contract summary.

        Returns:
            Contract details
        """
        return {
            "name": self.name,
            "inputs": self.contract.inputs,
            "outputs": self.contract.outputs,
            "transforms": self.contract.transforms,
            "dependencies": self.contract.dependencies,
            "guarantees": self.contract.guarantees,
            "executions": self._execution_count,
            "violations": len(self._contract_violations)
        }


class ContractViolation(Exception):
    """Exception raised when contract is violated."""

    def __init__(self, violation: Dict[str, Any]):
        self.violation = violation
        super().__init__(f"Contract violation: {violation}")


### 4. Orchestrator - Contract Enforcement

```python
class Orchestrator:
    """Orchestrates execution with contract enforcement.

    This is the central coordinator that ensures all contracts
    are respected during execution, providing the control layer
    over the dynamic runtime system.
    """

    def __init__(self):
        """Initialize orchestrator."""
        self.components: Dict[str, Any] = {}
        self.contracts: Dict[str, Any] = {}
        self.access_rules: Dict[str, AccessPermissions] = {}
        self.execution_log: List[Dict] = []

    def register_engine(self, name: str, engine: EngineInterface) -> None:
        """Register engine with its contract.

        Args:
            name: Engine identifier
            engine: Engine implementing EngineInterface
        """
        self.components[name] = engine
        self.contracts[name] = engine.get_contract()

        # Derive access rules from contract
        permissions = self._derive_permissions_from_contract(engine.get_contract())
        self.access_rules[name] = permissions

        logger.info(f"Registered engine '{name}' with contract")

    def register_node(self, node: ContractualNode) -> None:
        """Register node with its contract.

        Args:
            node: Node with contract
        """
        self.components[node.name] = node
        self.contracts[node.name] = node.contract

        # Derive access rules from node contract
        permissions = self._derive_permissions_from_node_contract(node.contract)
        self.access_rules[node.name] = permissions

        logger.info(f"Registered node '{node.name}' with contract")

    def execute(self, component_name: str, state: BoundedState) -> Any:
        """Execute component with full contract enforcement.

        Args:
            component_name: Component to execute
            state: Bounded state container

        Returns:
            Execution result

        Raises:
            ContractViolation: If any contract violated
            ValueError: If component not found
        """
        if component_name not in self.components:
            raise ValueError(f"Component '{component_name}' not registered")

        component = self.components[component_name]
        contract = self.contracts[component_name]

        # Get bounded view for component
        state_view = state.get_view_for(component_name)

        # Pre-execution validation
        if isinstance(component, EngineInterface):
            if not component.validate_input(state.snapshot()):
                raise ContractViolation({
                    "component": component_name,
                    "phase": "pre-execution",
                    "details": "Input validation failed"
                })

            unmet_preconditions = component.check_preconditions(state.snapshot())
            if unmet_preconditions:
                raise ContractViolation({
                    "component": component_name,
                    "phase": "preconditions",
                    "details": f"Unmet preconditions: {unmet_preconditions}"
                })

        # Execute with monitoring
        start_time = datetime.now()
        try:
            if isinstance(component, ContractualNode):
                result = component(state_view)
            else:
                result = component.execute(state_view)

            execution_time = (datetime.now() - start_time).total_seconds()

            # Post-execution validation
            if isinstance(component, EngineInterface):
                if not component.validate_output(result):
                    raise ContractViolation({
                        "component": component_name,
                        "phase": "post-execution",
                        "details": "Output validation failed"
                    })

                unmet_postconditions = component.check_postconditions(state.snapshot())
                if unmet_postconditions:
                    raise ContractViolation({
                        "component": component_name,
                        "phase": "postconditions",
                        "details": f"Unmet postconditions: {unmet_postconditions}"
                    })

            # Log successful execution
            self.execution_log.append({
                "timestamp": datetime.now().isoformat(),
                "component": component_name,
                "duration": execution_time,
                "status": "success"
            })

            return result

        except Exception as e:
            # Log failed execution
            self.execution_log.append({
                "timestamp": datetime.now().isoformat(),
                "component": component_name,
                "duration": (datetime.now() - start_time).total_seconds(),
                "status": "failed",
                "error": str(e)
            })
            raise

    def validate_composition(self, components: List[str]) -> List[str]:
        """Validate that components can be composed.

        Args:
            components: List of component names in execution order

        Returns:
            List of compatibility issues
        """
        issues = []

        for i in range(len(components) - 1):
            current = components[i]
            next_comp = components[i + 1]

            if current not in self.contracts or next_comp not in self.contracts:
                issues.append(f"Component not registered: {current} or {next_comp}")
                continue

            current_contract = self.contracts[current]
            next_contract = self.contracts[next_comp]

            # Check output-input compatibility
            if hasattr(current_contract, 'outputs') and hasattr(next_contract, 'inputs'):
                current_outputs = set(current_contract.outputs)
                next_inputs = set(next_contract.inputs)

                missing = next_inputs - current_outputs
                if missing:
                    issues.append(
                        f"Component '{next_comp}' requires {missing} "
                        f"but '{current}' doesn't provide them"
                    )

        return issues

    def _derive_permissions_from_contract(self, contract: EngineContract) -> AccessPermissions:
        """Derive access permissions from engine contract.

        Args:
            contract: Engine contract

        Returns:
            Access permissions
        """
        permissions = AccessPermissions()

        # Inputs are readable
        for field in contract.inputs:
            permissions.readable.add(field.name)

        # Outputs are writable
        for field in contract.outputs:
            permissions.writable.add(field.name)

        # Side effects need write access
        for field in contract.side_effects:
            permissions.writable.add(field)

        return permissions

    def _derive_permissions_from_node_contract(self, contract: NodeContract) -> AccessPermissions:
        """Derive access permissions from node contract.

        Args:
            contract: Node contract

        Returns:
            Access permissions
        """
        permissions = AccessPermissions()

        # Inputs are readable
        permissions.readable.update(contract.inputs)

        # Outputs are writable
        permissions.writable.update(contract.outputs)

        # Transforms need both read and write
        for source, target in contract.transforms.items():
            permissions.readable.add(source)
            permissions.writable.add(target)

        return permissions

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executions.

        Returns:
            Execution statistics
        """
        total = len(self.execution_log)
        successful = sum(1 for e in self.execution_log if e["status"] == "success")
        failed = total - successful

        avg_duration = 0
        if successful > 0:
            durations = [e["duration"] for e in self.execution_log if e["status"] == "success"]
            avg_duration = sum(durations) / len(durations)

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "average_duration": avg_duration,
            "registered_components": len(self.components),
            "contract_violations": failed
        }


## 🔄 Integration Examples

### Example 1: LLM Engine with Contract

```python
class ContractualLLMEngine(EngineInterface):
    """LLM engine with explicit contract."""

    def __init__(self, config: AugLLMConfig):
        self.config = config

    def get_contract(self) -> EngineContract:
        return EngineContract(
            inputs=[
                FieldContract(name="messages", type=list, required=True),
                FieldContract(name="temperature", type=float, required=False, default=0.7)
            ],
            outputs=[
                FieldContract(name="response", type=str, required=True),
                FieldContract(name="token_usage", type=dict, required=False)
            ],
            side_effects=["conversation_history"],
            preconditions=["len(messages) > 0"],
            postconditions=["response is not None", "len(response) > 0"]
        )

    def validate_input(self, state: Dict[str, Any]) -> bool:
        return "messages" in state and isinstance(state["messages"], list)

    def validate_output(self, result: Any) -> bool:
        return isinstance(result, dict) and "response" in result

    def execute(self, state_view: StateView) -> Dict[str, Any]:
        messages = state_view.get("messages")
        temperature = state_view.get("temperature", 0.7)

        # Execute LLM
        response = self.config.create_runnable().invoke({
            "messages": messages,
            "temperature": temperature
        })

        # Update conversation history
        state_view.append("conversation_history", {
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "response": response
        })

        return {"response": response, "token_usage": {"total": 100}}


### Example 2: Complete Workflow with Contracts

```python
# Create bounded state
state = BoundedState(initial_data={
    "messages": [{"role": "user", "content": "Hello"}],
    "context": {},
    "conversation_history": []
})

# Create orchestrator
orchestrator = Orchestrator()

# Register LLM engine with contract
llm_engine = ContractualLLMEngine(AugLLMConfig())
orchestrator.register_engine("llm", llm_engine)

# Register validation node with contract
validation_contract = NodeContract(
    inputs=["response"],
    outputs=["validated_response", "validation_score"],
    transforms={"response": "validated_response"}
)

def validate_response(state_view: StateView) -> Dict[str, Any]:
    response = state_view.get("response")
    # Validation logic
    return {
        "validated_response": response,
        "validation_score": 0.95
    }

validation_node = ContractualNode("validator", validation_contract, validate_response)
orchestrator.register_node(validation_node)

# Register components with bounded state
state.register_component("llm", orchestrator.access_rules["llm"])
state.register_component("validator", orchestrator.access_rules["validator"])

# Validate composition
issues = orchestrator.validate_composition(["llm", "validator"])
if issues:
    print(f"Composition issues: {issues}")

# Execute with contract enforcement
try:
    # Execute LLM
    llm_result = orchestrator.execute("llm", state)

    # Update state with result
    state._data.update(llm_result)

    # Execute validator
    validation_result = orchestrator.execute("validator", state)

    print(f"Success! Result: {validation_result}")

except ContractViolation as e:
    print(f"Contract violation: {e.violation}")

# Get execution summary
summary = orchestrator.get_execution_summary()
print(f"Execution summary: {summary}")


## 💡 Key Benefits

### 1. Runtime Flexibility Preserved
- Dynamic tool addition still works
- State-driven behavior maintained
- Hot-swappable logic supported
- Adaptive workflows enabled

### 2. Explicit Contracts Added
- Clear input/output specifications
- Preconditions and postconditions
- Side effects documented
- Dependencies explicit

### 3. Controlled Access
- Field-level permissions
- Access logging and auditing
- Permission violations tracked
- State isolation enforced

### 4. Transformation Layer
- State views instead of direct mutation
- Controlled updates through orchestrator
- Rollback and checkpointing
- History tracking

### 5. Single Responsibility
- Engines do one thing
- Nodes have clear contracts
- Orchestrator enforces contracts
- State manages data only

## 📊 Complexity Reduction

### Current: 30🔥 from Engine-Schema
- Unrestricted state access
- No contracts
- Mixed responsibilities
- Implicit behavior
- Runtime chaos

### With Runtime Contracts: <10🔥
- Controlled access through views
- Explicit contracts at runtime
- Single responsibilities enforced
- Explicit behavior documented
- Runtime order from chaos

## 🎯 Implementation Strategy

### Phase 1: Core Infrastructure
1. Implement BoundedState with access control
2. Create EngineInterface protocol
3. Build ContractualNode pattern
4. Develop Orchestrator for enforcement

### Phase 2: Engine Migration
1. Add EngineInterface to existing engines
2. Define contracts for each engine type
3. Implement validation methods
4. Test contract enforcement

### Phase 3: Node Migration
1. Convert nodes to ContractualNode
2. Define node contracts explicitly
3. Update graph composition
4. Validate node chains

### Phase 4: Integration
1. Update Agent to use Orchestrator
2. Migrate MultiAgent to contracts
3. Add contract validation to graphs
4. Performance optimization

## 🔑 Success Metrics

1. **Contract Coverage**: 100% of engines/nodes have contracts
2. **Access Violations**: <1% of executions have violations
3. **Composition Validation**: 95% of compositions valid first try
4. **Performance Impact**: <5ms overhead per execution
5. **Developer Experience**: Contract definition in <20 lines

## 🚀 Next Steps

1. **Prototype BoundedState** - Test access control patterns
2. **Define Core Contracts** - Start with LLM and Tool engines
3. **Build Orchestrator** - Implement contract enforcement
4. **Migrate One Agent** - Prove the pattern works
5. **Performance Testing** - Ensure acceptable overhead

---

**The Way Forward**: Add contracts and boundaries to the runtime system without removing its flexibility. This gives us the best of both worlds - dynamic adaptation with explicit guarantees.
````
