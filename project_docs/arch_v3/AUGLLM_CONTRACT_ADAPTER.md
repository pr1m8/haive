# AugLLMConfig Contract Adapter - Concrete Implementation

**Created**: 2025-09-08
**Purpose**: Show how to add contracts to existing AugLLMConfig
**Status**: Implementation Example
**Key Pattern**: Adapter that adds contracts without modifying original

## 🎯 The Problem

AugLLMConfig has 2,647 lines doing everything:

- LLM configuration
- Tool management
- Structured output
- Validation
- Caching
- Routing
- State management

No explicit contracts about what it needs or produces!

## 🏗️ The Solution: Contract Adapter

````python
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.common.message import BaseMessage

logger = logging.getLogger(__name__)


class AugLLMContract(BaseModel):
    """Contract specification for AugLLMConfig.

    This defines what the LLM engine needs and guarantees,
    making its behavior explicit and verifiable.
    """

    # Required inputs
    required_inputs: Set[str] = Field(
        default={"messages"},
        description="Fields that must be present"
    )

    # Optional inputs with defaults
    optional_inputs: Dict[str, Any] = Field(
        default={
            "temperature": 0.7,
            "max_tokens": None,
            "tools": [],
            "tool_choice": "auto"
        },
        description="Optional fields with defaults"
    )

    # Guaranteed outputs
    guaranteed_outputs: Set[str] = Field(
        default={"response", "message_added"},
        description="Fields guaranteed to be produced"
    )

    # Possible outputs (conditional)
    possible_outputs: Dict[str, str] = Field(
        default={
            "tool_calls": "if tools provided",
            "structured_output": "if structured_output_model set",
            "token_usage": "if tracking enabled"
        },
        description="Conditional outputs"
    )

    # Side effects
    side_effects: List[str] = Field(
        default=[
            "appends to messages",
            "may call tools",
            "updates conversation_history if present"
        ],
        description="State modifications"
    )

    # Preconditions
    preconditions: List[str] = Field(
        default=[
            "messages must be list of BaseMessage or dicts",
            "if tools provided, they must be callable",
            "temperature must be between 0 and 2"
        ],
        description="Conditions that must be true before execution"
    )

    # Postconditions
    postconditions: List[str] = Field(
        default=[
            "response will be non-empty string",
            "messages will have new assistant message",
            "if tool_calls made, tool_messages will be added"
        ],
        description="Conditions guaranteed after execution"
    )


class ContractualAugLLMConfig:
    """AugLLMConfig with explicit contracts.

    This adapter wraps AugLLMConfig to add contract enforcement
    without modifying the original implementation.
    """

    def __init__(self, config: Optional[AugLLMConfig] = None, **kwargs):
        """Initialize with config or create new one.

        Args:
            config: Existing AugLLMConfig to wrap
            **kwargs: Arguments to create new AugLLMConfig
        """
        self.config = config or AugLLMConfig(**kwargs)
        self.contract = self._build_contract()
        self._execution_log: List[Dict] = []
        self._contract_violations: List[Dict] = []

    def _build_contract(self) -> AugLLMContract:
        """Build contract based on configuration.

        Returns:
            Contract specification
        """
        contract = AugLLMContract()

        # Adjust contract based on configuration
        if self.config.tools:
            contract.required_inputs.add("tools")
            contract.guaranteed_outputs.add("tool_calls")

        if self.config.structured_output_model:
            contract.guaranteed_outputs.add("structured_output")
            contract.postconditions.append(
                f"structured_output will match {self.config.structured_output_model}"
            )

        if self.config.streaming:
            contract.possible_outputs["stream_chunks"] = "if streaming enabled"

        return contract

    def validate_input(self, state: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate state meets input contract.

        Args:
            state: Input state to validate

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check required inputs
        for field in self.contract.required_inputs:
            if field not in state:
                issues.append(f"Missing required field: {field}")

        # Validate messages format
        if "messages" in state:
            messages = state["messages"]
            if not isinstance(messages, list):
                issues.append("messages must be a list")
            elif messages:
                for i, msg in enumerate(messages):
                    if not isinstance(msg, (dict, BaseMessage)):
                        issues.append(f"messages[{i}] must be dict or BaseMessage")

        # Validate temperature if provided
        if "temperature" in state:
            temp = state["temperature"]
            if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
                issues.append("temperature must be between 0 and 2")

        # Validate tools if provided
        if "tools" in state:
            tools = state["tools"]
            if not isinstance(tools, list):
                issues.append("tools must be a list")
            else:
                for i, tool in enumerate(tools):
                    if not callable(tool) and not hasattr(tool, "__call__"):
                        issues.append(f"tools[{i}] must be callable")

        return len(issues) == 0, issues

    def validate_output(self, result: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate output meets contract.

        Args:
            result: Execution result to validate

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check guaranteed outputs
        for field in self.contract.guaranteed_outputs:
            if field not in result:
                issues.append(f"Missing guaranteed output: {field}")

        # Validate response
        if "response" in result:
            if not isinstance(result["response"], str) or not result["response"]:
                issues.append("response must be non-empty string")

        # Validate structured output if expected
        if self.config.structured_output_model and "structured_output" in result:
            try:
                # Validate against model
                self.config.structured_output_model.model_validate(result["structured_output"])
            except Exception as e:
                issues.append(f"structured_output validation failed: {e}")

        # Validate tool calls if present
        if "tool_calls" in result:
            tool_calls = result["tool_calls"]
            if not isinstance(tool_calls, list):
                issues.append("tool_calls must be a list")

        return len(issues) == 0, issues

    def check_preconditions(self, state: Dict[str, Any]) -> List[str]:
        """Check which preconditions are not met.

        Args:
            state: Current state

        Returns:
            List of unmet preconditions
        """
        unmet = []

        # Check messages format
        if "messages" in state:
            messages = state["messages"]
            if not isinstance(messages, list):
                unmet.append("messages must be list of BaseMessage or dicts")
            elif not all(isinstance(m, (dict, BaseMessage)) for m in messages):
                unmet.append("messages must be list of BaseMessage or dicts")

        # Check tools are callable
        if "tools" in state and self.config.tools:
            tools = state["tools"]
            if not all(callable(t) or hasattr(t, "__call__") for t in tools):
                unmet.append("if tools provided, they must be callable")

        # Check temperature range
        if "temperature" in state:
            temp = state["temperature"]
            if not (0 <= temp <= 2):
                unmet.append("temperature must be between 0 and 2")

        return unmet

    def check_postconditions(self, state: Dict[str, Any], result: Dict[str, Any]) -> List[str]:
        """Check which postconditions are not met.

        Args:
            state: State after execution
            result: Execution result

        Returns:
            List of unmet postconditions
        """
        unmet = []

        # Check response is non-empty
        if "response" in result:
            if not result["response"] or not isinstance(result["response"], str):
                unmet.append("response will be non-empty string")

        # Check messages updated
        if "messages" in state and "message_added" in result:
            if not result["message_added"]:
                unmet.append("messages will have new assistant message")

        # Check tool messages if tools called
        if "tool_calls" in result and result["tool_calls"]:
            if "tool_messages" not in state or not state["tool_messages"]:
                unmet.append("if tool_calls made, tool_messages will be added")

        return unmet

    def execute_with_contract(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with full contract enforcement.

        Args:
            state: Input state

        Returns:
            Execution result with contract validation

        Raises:
            ContractViolation: If contract is violated
        """
        start_time = datetime.now()

        # Pre-execution validation
        valid, issues = self.validate_input(state)
        if not valid:
            violation = {
                "phase": "input_validation",
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
            self._contract_violations.append(violation)
            raise ContractViolation(f"Input validation failed: {issues}")

        # Check preconditions
        unmet_pre = self.check_preconditions(state)
        if unmet_pre:
            violation = {
                "phase": "preconditions",
                "unmet": unmet_pre,
                "timestamp": datetime.now().isoformat()
            }
            self._contract_violations.append(violation)
            raise ContractViolation(f"Preconditions not met: {unmet_pre}")

        # Execute
        try:
            # Create runnable and execute
            runnable = self.config.create_runnable()
            raw_result = runnable.invoke(state)

            # Transform to expected format
            result = self._transform_result(raw_result, state)

        except Exception as e:
            violation = {
                "phase": "execution",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self._contract_violations.append(violation)
            raise ContractViolation(f"Execution failed: {e}")

        # Post-execution validation
        valid, issues = self.validate_output(result)
        if not valid:
            violation = {
                "phase": "output_validation",
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
            self._contract_violations.append(violation)
            raise ContractViolation(f"Output validation failed: {issues}")

        # Check postconditions
        unmet_post = self.check_postconditions(state, result)
        if unmet_post:
            violation = {
                "phase": "postconditions",
                "unmet": unmet_post,
                "timestamp": datetime.now().isoformat()
            }
            self._contract_violations.append(violation)
            raise ContractViolation(f"Postconditions not met: {unmet_post}")

        # Log successful execution
        self._execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "duration": (datetime.now() - start_time).total_seconds(),
            "status": "success",
            "input_size": len(str(state)),
            "output_size": len(str(result))
        })

        return result

    def _transform_result(self, raw_result: Any, state: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw result to contract format.

        Args:
            raw_result: Raw execution result
            state: Input state

        Returns:
            Transformed result matching contract
        """
        result = {}

        # Extract response
        if isinstance(raw_result, str):
            result["response"] = raw_result
        elif isinstance(raw_result, dict):
            result["response"] = raw_result.get("content", str(raw_result))
        elif hasattr(raw_result, "content"):
            result["response"] = raw_result.content
        else:
            result["response"] = str(raw_result)

        # Track message addition
        result["message_added"] = True

        # Add tool calls if present
        if hasattr(raw_result, "tool_calls"):
            result["tool_calls"] = raw_result.tool_calls

        # Add structured output if present
        if self.config.structured_output_model and hasattr(raw_result, "structured_output"):
            result["structured_output"] = raw_result.structured_output

        # Add token usage if available
        if hasattr(raw_result, "usage"):
            result["token_usage"] = {
                "total": raw_result.usage.total_tokens,
                "prompt": raw_result.usage.prompt_tokens,
                "completion": raw_result.usage.completion_tokens
            }

        return result

    def get_contract_summary(self) -> Dict[str, Any]:
        """Get human-readable contract summary.

        Returns:
            Contract details and statistics
        """
        total_executions = len(self._execution_log)
        successful = sum(1 for e in self._execution_log if e["status"] == "success")
        violations = len(self._contract_violations)

        return {
            "contract": {
                "required_inputs": list(self.contract.required_inputs),
                "optional_inputs": list(self.contract.optional_inputs.keys()),
                "guaranteed_outputs": list(self.contract.guaranteed_outputs),
                "possible_outputs": list(self.contract.possible_outputs.keys()),
                "side_effects": self.contract.side_effects,
                "preconditions": self.contract.preconditions,
                "postconditions": self.contract.postconditions
            },
            "statistics": {
                "total_executions": total_executions,
                "successful": successful,
                "violations": violations,
                "success_rate": successful / total_executions if total_executions > 0 else 0
            },
            "recent_violations": self._contract_violations[-5:] if self._contract_violations else []
        }

    def add_tool_with_contract(self, tool: Any, contract: Dict[str, Any]) -> None:
        """Add tool with its contract.

        Args:
            tool: Tool to add
            contract: Tool's contract specification
        """
        # Add to config
        self.config.add_tool(tool)

        # Update our contract
        self.contract.possible_outputs[f"tool_{tool.__name__}_result"] = "if tool is called"
        self.contract.side_effects.append(f"may call {tool.__name__}")

        # Store tool contract for validation
        if not hasattr(self, "_tool_contracts"):
            self._tool_contracts = {}
        self._tool_contracts[tool.__name__] = contract

        logger.info(f"Added tool '{tool.__name__}' with contract")


class ContractViolation(Exception):
    """Exception raised when contract is violated."""
    pass


## 🔄 Usage Examples

### Example 1: Basic Usage with Contract Enforcement

```python
# Create contractual config
config = ContractualAugLLMConfig(
    temperature=0.7,
    max_tokens=1000,
    system_message="You are a helpful assistant"
)

# Get contract details
contract_summary = config.get_contract_summary()
print(f"Contract: {contract_summary['contract']}")

# Prepare state
state = {
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.8
}

# Execute with contract enforcement
try:
    result = config.execute_with_contract(state)
    print(f"Success! Response: {result['response']}")

except ContractViolation as e:
    print(f"Contract violation: {e}")

# Check execution statistics
stats = config.get_contract_summary()["statistics"]
print(f"Success rate: {stats['success_rate']:.2%}")


### Example 2: Tool Integration with Contracts

```python
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expression."""
    return str(eval(expression))

# Create config with tools
config = ContractualAugLLMConfig(
    tools=[calculator],
    tool_choice="auto"
)

# Add tool with its contract
config.add_tool_with_contract(
    calculator,
    contract={
        "inputs": ["expression: str"],
        "outputs": ["result: str"],
        "preconditions": ["expression must be valid Python"],
        "postconditions": ["result is string representation of number"]
    }
)

# Execute with tool usage
state = {
    "messages": [
        {"role": "user", "content": "What is 15 * 23?"}
    ]
}

result = config.execute_with_contract(state)
print(f"Response: {result['response']}")
print(f"Tool calls: {result.get('tool_calls', [])}")


### Example 3: Structured Output with Contract

```python
class MovieReview(BaseModel):
    title: str
    rating: float
    review: str

# Create config with structured output
config = ContractualAugLLMConfig(
    structured_output_model=MovieReview
)

# Contract automatically includes structured output guarantee
print(f"Guaranteed outputs: {config.contract.guaranteed_outputs}")

# Execute with structured output
state = {
    "messages": [
        {"role": "user", "content": "Review the movie Inception"}
    ]
}

result = config.execute_with_contract(state)
print(f"Response: {result['response']}")
print(f"Structured output: {result['structured_output']}")

# Validate structured output matches model
review = MovieReview.model_validate(result['structured_output'])
print(f"Valid review: {review.title} - {review.rating}/10")


## 💡 Integration with Bounded State

```python
# Create bounded state with AugLLM permissions
state = BoundedState(initial_data={
    "messages": [],
    "conversation_history": [],
    "tools": []
})

# Register AugLLM with derived permissions
permissions = AccessPermissions(
    readable={"messages", "tools", "temperature"},
    writable={"response", "tool_calls"},
    append_only={"conversation_history"}
)

state.register_component("llm", permissions)

# Create contractual config
llm_config = ContractualAugLLMConfig()

# Get bounded view for LLM
llm_view = state.get_view_for("llm")

# Execute with bounded view (pseudo-code for integration)
def execute_with_view(config: ContractualAugLLMConfig, view: StateView):
    # Extract needed fields through view
    messages = view.get("messages")
    tools = view.get("tools", [])

    # Execute with contract
    result = config.execute_with_contract({
        "messages": messages,
        "tools": tools
    })

    # Update through view
    view.set("response", result["response"])
    if "tool_calls" in result:
        view.set("tool_calls", result["tool_calls"])

    # Append to history
    view.append("conversation_history", {
        "timestamp": datetime.now().isoformat(),
        "messages": messages,
        "response": result["response"]
    })

    return result


## 📊 Benefits of Contract Adapter

### 1. No Modification Required
- Original AugLLMConfig unchanged
- Adapter pattern preserves functionality
- Gradual migration possible

### 2. Explicit Behavior
- Clear input requirements
- Guaranteed outputs documented
- Side effects tracked
- Pre/post conditions verified

### 3. Runtime Validation
- Input validation before execution
- Output validation after execution
- Contract violations tracked
- Success metrics available

### 4. Tool Contract Integration
- Tools can have their own contracts
- Composition validation possible
- Tool usage tracked

### 5. Debugging Support
- Execution logs maintained
- Contract violations recorded
- Statistics available
- Clear error messages

## 🚀 Migration Path

### Phase 1: Create Adapters
```python
# Wrap existing configs
config = AugLLMConfig(...)
contractual_config = ContractualAugLLMConfig(config=config)
````

### Phase 2: Use in New Code

```python
# New code uses contractual version
agent = SimpleAgent(
    engine=contractual_config,
    ...
)
```

### Phase 3: Add Validation

```python
# Validate before execution
valid, issues = contractual_config.validate_input(state)
if not valid:
    handle_validation_errors(issues)
```

### Phase 4: Track Metrics

```python
# Monitor contract compliance
stats = contractual_config.get_contract_summary()
if stats["statistics"]["success_rate"] < 0.95:
    investigate_violations()
```

## 🎯 Next Steps

1. **Implement for other engines** - VectorStore, Retriever, etc.
2. **Create contract registry** - Central place for all contracts
3. **Build validation tools** - Automated contract testing
4. **Add to CI/CD** - Contract compliance checks
5. **Create documentation** - Auto-generate from contracts

---

**Key Takeaway**: We can add contracts to existing components using the adapter pattern, gaining all the benefits of explicit contracts without modifying the original implementations. This allows gradual migration while immediately improving visibility and debugging.
